"""Simulate pending spells and combat in a cloned room with both players passing."""

from __future__ import annotations

import asyncio
import random
import time
from functools import partial
from types import CellType, FunctionType, MethodType, ModuleType
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from game.player import Player
    from game.room import Room


class _SilentActions:
    """Keep the action-recording interface without storing replays or sending notifications."""

    def start_record(self):
        pass

    def end_record(self):
        pass

    def add_action(self, action):
        pass


class _PreviewStack(list):
    """Bound stack pops, including entries removed by counterspells."""

    def __init__(self, max_effects: int):
        super().__init__()
        self.remaining = max_effects

    def pop(self, index: int = -1):
        if self.remaining <= 0:
            raise RuntimeError("Stack simulation exceeded max_effects")
        self.remaining -= 1
        return super().pop(index)


class _StateCloner:
    """Clone game objects while preserving callback, bound-method, and buff references."""

    def __init__(self, memo: dict[int, Any]):
        self.memo = memo
        self.empty_list_fields = ("pedding_store_task", "action_history", "opponent_history")
        self.skipped_fields = {"agent", "future_function", "socket_select_object", *self.empty_list_fields}
        self.atomic_types = (bool, int, float, complex, str, bytes, type, ModuleType)

    def copy(self, obj: Any) -> Any:
        key = id(obj)
        if key in self.memo:
            return self.memo[key]
        if obj is None or obj is Ellipsis or isinstance(obj, self.atomic_types):
            return obj
        if isinstance(obj, FunctionType):
            return self.copy_function(obj)
        if isinstance(obj, list):
            result = self.memo[key] = []
            result.extend(self.copy(item) for item in obj)
        elif isinstance(obj, dict):
            result = self.memo[key] = {}
            result.update((self.copy(k), self.copy(v)) for k, v in obj.items())
        elif isinstance(obj, (tuple, set, frozenset)):
            items = [self.copy(item) for item in obj]
            result = self.memo.get(key, type(obj)(items))
        elif isinstance(obj, MethodType):
            result = MethodType(self.copy(obj.__func__), self.copy(obj.__self__))
        elif isinstance(obj, partial):
            result = partial(self.copy(obj.func), *self.copy(obj.args), **self.copy(obj.keywords))
        elif isinstance(obj, asyncio.Lock):
            result = asyncio.Lock()
        elif isinstance(obj, asyncio.Condition):
            result = asyncio.Condition()
        elif isinstance(obj, asyncio.Event):
            result = asyncio.Event()
            if obj.is_set():
                result.set()
        elif type(obj).__module__.startswith(("game.", "pycards.", "pytreasures.")):
            return self.copy_object(obj)
        else:
            raise TypeError(f"Unsupported stack simulation object: {type(obj).__name__}")
        self.memo[key] = result
        return result

    def copy_function(self, function: FunctionType) -> FunctionType:
        if not (function.__closure__ or function.__defaults__ or function.__kwdefaults__):
            return function
        source_cells = function.__closure__ or ()
        cells = tuple(self.memo.setdefault(id(cell), CellType()) for cell in source_cells)
        result = FunctionType(function.__code__, function.__globals__, function.__name__, None, cells or None)
        self.memo[id(function)] = result
        for source, target in zip(source_cells, cells):
            try:
                value = source.cell_contents
            except ValueError:  # Leave uninitialized closure cells empty.
                continue
            target.cell_contents = self.copy(value)
        result.__defaults__ = self.copy(function.__defaults__)
        result.__kwdefaults__ = self.copy(function.__kwdefaults__)
        result.__dict__.update(self.copy(function.__dict__))
        result.__qualname__ = function.__qualname__
        return result

    def copy_object(self, obj: Any) -> Any:
        result = self.memo[id(obj)] = object.__new__(type(obj))
        result.__dict__.update(
            {name: self.copy(value) for name, value in vars(obj).items() if name not in self.skipped_fields}
        )
        for name in self.empty_list_fields:
            if hasattr(obj, name):
                setattr(result, name, [])
        if hasattr(obj, "future_function"):
            result.future_function = None
        return result


async def _finish_preview(room: Room, died_players: list[Player]) -> None:
    room.gamming = False


def _has_pending_effects(room: Room) -> bool:
    return bool(room.stack or room.get_flag("bullet_time") or room.get_flag("attacker_defenders"))


def clone_preview_room(room: Room, max_effects: int = 256) -> Room:
    """Clone game state without models, training data, process communication, or background tasks."""
    if max_effects < 1:
        raise ValueError("max_effects must be positive")
    fields = (
        "players",
        "player_1",
        "player_2",
        "active_player",
        "non_active_player",
        "stack",
        "attacker",
        "flag_dict",
        "counter_dict",
        "gamming",
        "config",
    )
    shadow = object.__new__(type(room))
    cloner = _StateCloner(
        {
            id(room): shadow,
            id(room.action_processor): _SilentActions(),
            id(room.stack): _PreviewStack(max_effects),
        }
    )
    for name in fields:
        if hasattr(room, name):
            setattr(shadow, name, cloner.copy(getattr(room, name)))
    shadow.stack.extend(cloner.copy(item) for item in room.stack)
    shadow.action_processor = cloner.copy(room.action_processor)
    shadow.players_socket = {name: None for name in shadow.players}
    shadow.game_recorder = {}
    shadow.room_server = None
    shadow.bullet_timer = 0
    shadow.max_bullet_time = getattr(room, "max_bullet_time", 10)
    shadow.initinal_turn_timer = shadow._elapsed_time = time.perf_counter()
    shadow.game_end = MethodType(_finish_preview, shadow)
    return shadow


async def simulate_stack(room: Room, seed: int = 0, max_rounds: int = 16, max_effects: int = 256) -> Room:
    """Resolve a cloned room with a fixed random seed and no further model decisions.

    Call from the worker's single-room flow; do not advance the live game concurrently.
    Simulations in one event loop run sequentially and restore Python's RNG state on exit.
    """
    from game.room import Room

    if max_rounds < 1:
        raise ValueError("max_rounds must be positive")
    shadow = clone_preview_room(room, max_effects)
    loop = asyncio.get_running_loop()
    lock = getattr(loop, "_stack_simulation_lock", None)
    if lock is None:
        lock = asyncio.Lock()
        setattr(loop, "_stack_simulation_lock", lock)
    async with lock:
        rng_state = random.getstate()
        try:
            random.seed(seed)
            for _ in range(max_rounds):
                if not shadow.gamming or not _has_pending_effects(shadow):
                    return shadow
                await Room.end_bullet_time(shadow)
            if shadow.gamming and _has_pending_effects(shadow):
                raise RuntimeError("Stack simulation exceeded max_rounds")
            return shadow
        finally:
            random.setstate(rng_state)


async def get_stack_reward(room: Room, agent: Player, weight: float = 0.25, seed: int = 0) -> dict:
    """Blend current and projected scores using the configured synchronous scorer.

    Call this async helper from the room, not through the YAML reward_function setting.
    Preserve existing score fields and add reward_actual and reward_preview.
    """
    if not 0 <= weight <= 1:
        raise ValueError("weight must be between 0 and 1")
    score_fn = room.basic_func[agent.name]["get_reward"]
    result = dict(score_fn(agent))
    actual = predicted = result["reward"]
    if weight and room.gamming and _has_pending_effects(room):
        shadow = await simulate_stack(room, seed=seed)
        predicted = score_fn.func(shadow, shadow.players[agent.name], **score_fn.keywords)["reward"]
    result.update(
        reward_actual=actual, reward_preview=predicted, reward=(1 - weight) * actual + weight * predicted
    )
    return result
