from __future__ import annotations

import asyncio
import importlib.util
import random
import sys
import time
import types
import unittest
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

# Lightweight fallbacks so tests can run in minimal env.
try:
    import pydantic  # noqa: F401
except ModuleNotFoundError:
    fake_pydantic = types.ModuleType("pydantic")

    def _validate_call(func=None, **_kwargs):
        if func is None:
            def _decorator(inner):
                return inner
            return _decorator
        return func

    class _BaseModel:
        pass

    fake_pydantic.validate_call = _validate_call
    fake_pydantic.BaseModel = _BaseModel
    sys.modules["pydantic"] = fake_pydantic

try:
    import typing_extensions  # noqa: F401
except ModuleNotFoundError:
    from typing import Literal as _Literal

    fake_typing_extensions = types.ModuleType("typing_extensions")
    fake_typing_extensions.Literal = _Literal
    sys.modules["typing_extensions"] = fake_typing_extensions

try:
    import starlette.websockets  # noqa: F401
except ModuleNotFoundError:
    fake_starlette = types.ModuleType("starlette")
    fake_starlette_websockets = types.ModuleType("starlette.websockets")

    class WebSocketDisconnect(Exception):
        pass

    fake_starlette_websockets.WebSocketDisconnect = WebSocketDisconnect
    fake_starlette.websockets = fake_starlette_websockets
    sys.modules["starlette"] = fake_starlette
    sys.modules["starlette.websockets"] = fake_starlette_websockets

try:
    import aiofiles  # noqa: F401
except ModuleNotFoundError:
    fake_aiofiles = types.ModuleType("aiofiles")

    class _AsyncFile:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def write(self, _data):
            return 0

    def _aio_open(*_args, **_kwargs):
        return _AsyncFile()

    fake_aiofiles.open = _aio_open
    sys.modules["aiofiles"] = fake_aiofiles

# Patch optional buff names before importing player/cards.
import game.buffs as buffs

if not hasattr(buffs, "Hexproof"):
    class Hexproof(buffs.KeyBuff):
        def __init__(self, card, selected_card) -> None:
            super().__init__(card, selected_card, "Hexproof")

    buffs.Hexproof = Hexproof

if not hasattr(buffs, "Lifelink"):
    class Lifelink(buffs.KeyBuff):
        def __init__(self, card, selected_card) -> None:
            super().__init__(card, selected_card, "lifelink")

    buffs.Lifelink = Lifelink

if not hasattr(buffs, "DoubleStrike"):
    class DoubleStrike(buffs.KeyBuff):
        def __init__(self, card, selected_card) -> None:
            super().__init__(card, selected_card, "Double strike")

    buffs.DoubleStrike = DoubleStrike

from game.room import Room
from game.player import Player
from game.card import Card
from game.type_cards.creature import Creature
from game.type_action import actions

if not hasattr(Card, "apply_runtime_balance"):
    def _noop_apply_runtime_balance(self):
        return None
    Card.apply_runtime_balance = _noop_apply_runtime_balance


class _DummyRoomServer:
    async def settle_player(self, *_args, **_kwargs):
        return

    async def update_task(self, *_args, **_kwargs):
        return


class TestRoom(Room):
    """Reuses Room + Player logic without background tasks."""

    def __init__(self, players: list[tuple[str, str]]) -> None:
        self.room_server = _DummyRoomServer()
        self.gamming = True

        self.action_store_list_cache_condition = asyncio.Condition()
        self.action_store_list_cache: list[actions.List_Action] = []
        self.action_processor = actions.List_Action_Processor(
            self.action_store_list_cache, self.action_store_list_cache_condition
        )
        self.action_store_list: list[actions.Action] = []

        self.turn_timer = 0
        self.max_turn_time = 120
        self.bullet_timer = 0
        self.max_bullet_time = 10
        self.initinal_turn_timer = time.perf_counter()
        self.initinal_bullet_timer = time.perf_counter()
        self._elapsed_time = time.perf_counter()
        self.flag_dict: dict[str, Any] = {"bullet_time": False, "attacker_defenders": False}
        self.counter_dict: dict[str, int] = {}
        self.stack: list[tuple] = []
        self.attacker = None

        self.initinal_player(players)
        self.action_processor.set_game_recorder(self.game_recorder)
        self.active_player: Player = self.player_1
        self.non_active_player: Player = self.player_2

        self.message_process_dict = {}
        self.message_process_condition = asyncio.Condition()
        self.message_process_queue = []
        self.tasks = []
        self.task_close = None

    async def start_bullet_time(self):
        self.flag_dict["bullet_time"] = True
        self.initinal_bullet_timer = time.perf_counter()
        self._elapsed_time = time.perf_counter()
        return

    async def action_sender(self):
        return

    async def message_process(self):
        return


class CardTestEnv:
    DEFAULT_DECK = "Forest+Land+1|Island+Land+1|Mountain+Land+1|Plains+Land+1|Swamp+Land+1"

    def __init__(self, deck_1: str | None = None, deck_2: str | None = None) -> None:
        self.room = TestRoom(
            [
                (deck_1 or self.DEFAULT_DECK, "p1"),
                (deck_2 or self.DEFAULT_DECK, "p2"),
            ]
        )
        self.p1 = self.room.player_1
        self.p2 = self.room.player_2
        self.room.players = {"p1": self.p1, "p2": self.p2}
        self._selection_script: dict[str, list[Any]] = {"p1": [], "p2": []}

        async def _auto_select_cards(_player: Player, selected_cards, selection_random=False):
            if not selected_cards:
                return "cancel"
            scripted = self._selection_script.get(_player.name, [])
            if scripted:
                forced = scripted.pop(0)
                if isinstance(forced, int) and 0 <= forced < len(selected_cards):
                    return selected_cards[forced]
                if forced in selected_cards:
                    return forced
            if selection_random:
                return random.choice(selected_cards)
            return selected_cards[0]

        async def _dummy_send_text(_player: Player, _message: str):
            return

        async def _dummy_receive_text(_player: Player):
            return "cancel"

        self.p1.send_selection_cards = _auto_select_cards.__get__(self.p1, Player)
        self.p2.send_selection_cards = _auto_select_cards.__get__(self.p2, Player)
        self.p1.send_text = _dummy_send_text.__get__(self.p1, Player)
        self.p2.send_text = _dummy_send_text.__get__(self.p2, Player)
        self.p1.receive_text = _dummy_receive_text.__get__(self.p1, Player)
        self.p2.receive_text = _dummy_receive_text.__get__(self.p2, Player)

        for p in (self.p1, self.p2):
            p.mana = {"colorless": 20, "U": 20, "W": 20, "B": 20, "R": 20, "G": 20}

    def snapshot(self) -> dict[str, Any]:
        def _state(player: Player) -> dict[str, Any]:
            return {
                "life": player.life,
                "hand": [c.name for c in player.hand],
                "battlefield": [c.name for c in player.battlefield],
                "graveyard": [c.name for c in player.graveyard],
                "land_area": [c.name for c in player.land_area],
                "exile_area": [c.name for c in player.exile_area],
                "library_count": len(player.library),
                "exile_count": len(player.exile_area),
            }

        return {"p1": _state(self.p1), "p2": _state(self.p2)}

    def put_in_hand(self, card, player: Player | None = None) -> None:
        owner = player or card.player
        owner.action_store.start_record()
        owner.append_card(card, "hand")
        owner.action_store.end_record()

    def put_on_battlefield(self, card, player: Player | None = None) -> None:
        owner = player or card.player
        owner.action_store.start_record()
        owner.append_card(card, "battlefield")
        owner.action_store.end_record()

    def put_in_land_area(self, card, player: Player | None = None) -> None:
        """
        Move a land into `land_area` the way older land tests do manually:
        strip from battlefield/hand, append to land_area (records wrapped).
        """
        owner = player or card.player
        owner.action_store.start_record()
        for zone in ("battlefield", "hand"):
            if card in getattr(owner, zone):
                owner.remove_card(card, zone)
        if card not in owner.land_area:
            owner.land_area.append(card)
        owner.action_store.end_record()

    def script_selection(self, player: Player, selections: list[Any]) -> None:
        """
        Queue forced selections for later select() calls.
        Each item can be either:
        - index in current selectable list (int)
        - exact selectable object instance
        """
        self._selection_script[player.name].extend(selections)

    async def play_card(
        self,
        card,
        player: Player | None = None,
        selections: list[Any] | None = None,
    ) -> tuple[bool, str]:
        owner = player or card.player
        if selections:
            self.script_selection(owner, selections)
        if card not in owner.hand:
            owner.action_store.start_record()
            owner.append_card(card, "hand")
            owner.action_store.end_record()
        return await owner.auto_play_card(card, start_bullet_time=False)

    def create_creature(
        self,
        player: Player,
        name: str = "Test Creature",
        power: int = 2,
        life: int = 2,
        **flags: bool,
    ) -> Creature:
        """
        Create an in-memory creature with arbitrary stats/keywords.
        Usage: env.create_creature(env.p1, "A", 4, 5, flying=True)
        """

        class _TestCreature(Creature):
            def __init__(self, owner: Player) -> None:
                super().__init__(owner)
                self.name = name
                self.live = life
                self.power = power
                self.actual_live = life
                self.actual_power = power
                self.type_creature = "Test Creature"
                self.type = "Creature"
                self.mana_cost = "0"
                self.color = "colorless"
                self.type_card = "Test Creature"
                self.rarity = "Token"
                self.content = "CardTestEnv custom creature"
                self.image_path = "cards/test/creature.jpg"
                for key, value in flags.items():
                    if value:
                        self.flag_dict[key] = True

        return _TestCreature(player)

    def put_creatures(
        self,
        player: Player,
        name: str = "Test Creature",
        power: int = 2,
        life: int = 2,
        count: int = 1,
        **flags: bool,
    ) -> list[Creature]:
        creatures: list[Creature] = []
        for _ in range(count):
            creature = self.create_creature(player, name, power, life, **flags)
            self.put_on_battlefield(creature, player)
            creatures.append(creature)
        return creatures

    def get_battlefield_creature(self, player: Player, name: str) -> Creature:
        for creature in player.battlefield:
            if creature.name == name:
                return creature
        raise ValueError(f"Creature '{name}' not found on battlefield for {player.name}")

    def card_zone(self, card) -> str:
        owner = card.player
        zone_map = {
            "hand": owner.hand,
            "battlefield": owner.battlefield,
            "land_area": owner.land_area,
            "graveyard": owner.graveyard,
            "library": owner.library,
            "exile_area": owner.exile_area,
        }
        for zone, cards in zone_map.items():
            if card in cards:
                return zone
        return "unknown"

    def find_card_by_name(
        self,
        player: Player,
        card_name: str,
        zones: tuple[str, ...] = ("battlefield", "graveyard", "exile_area", "hand"),
    ):
        zone_map = {
            "hand": player.hand,
            "battlefield": player.battlefield,
            "land_area": player.land_area,
            "graveyard": player.graveyard,
            "library": player.library,
            "exile_area": player.exile_area,
        }
        for zone in zones:
            cards = zone_map.get(zone, [])
            for card in cards:
                if getattr(card, "name", "") == card_name:
                    return card
        return None

    def _battlefield_index(self, player: Player, creature: Creature) -> int:
        try:
            return player.battlefield.index(creature)
        except ValueError as exc:
            raise ValueError(f"{creature.name} is not on {player.name} battlefield") from exc

    def set_active_player(self, player: Player) -> None:
        self.room.active_player = player
        self.room.non_active_player = player.opponent

    def ready_attacker(self, attacker: Creature, ignore_summoning_sickness: bool = True) -> None:
        """
        Make an attacker pass room.select_attacker() checks in tests.
        """
        attacker.flag_dict["tap"] = False
        if ignore_summoning_sickness:
            attacker.flag_dict["summoning_sickness"] = False
        if attacker.get_counter_from_dict("attack_counter") <= 0:
            attacker.set_counter_dict("attack_counter", 1)

    async def select_attacker(self, attacker: Creature) -> tuple[bool, str]:
        self.set_active_player(attacker.player)
        self.ready_attacker(attacker)
        idx = self._battlefield_index(attacker.player, attacker)
        return await self.room.select_attacker(attacker.player.name, str(idx))

    def ready_defender(self, defender: Creature, attacker: Creature | None = None) -> None:
        """
        Make a defender pass room.select_defender() checks in tests.
        """
        defender.flag_dict["tap"] = False
        if attacker and attacker.get_flag("flying"):
            if not (defender.get_flag("flying") or defender.get_flag("reach")):
                # Test convenience: allow deterministic block setup.
                defender.flag_dict["reach"] = True

    async def select_defender(
        self,
        defender: Creature,
        attacker: Creature | None = None,
    ) -> tuple[bool, str]:
        self.ready_defender(defender, attacker=attacker)
        idx = self._battlefield_index(defender.player, defender)
        return await self.room.select_defender(defender.player.name, str(idx))

    async def end_bullet_time(self) -> None:
        """
        Resolve combat/stack through room.end_bullet_time() instead of resolve_stack().
        """
        await self.room.end_bullet_time()

    async def simulate_combat(
        self,
        attacker: Creature,
        defender: Creature | Player | None = None,
    ) -> None:
        """
        Simulate combat by:
        1) selecting attacker
        2) optionally selecting defender
        3) resolving via end_bullet_time()
        """
        attacker_result = await self.select_attacker(attacker)
        if not attacker_result[0]:
            raise RuntimeError(f"select_attacker failed: {attacker_result[1]}")

        if isinstance(defender, Creature):
            defender_result = await self.select_defender(defender, attacker=attacker)
            if not defender_result[0]:
                raise RuntimeError(f"select_defender failed: {defender_result[1]}")

        await self.end_bullet_time()

    async def resolve_stack(self, max_steps: int = 50) -> None:
        """
        Keep test semantics aligned with real game resolution path.
        `max_steps` is kept for backward API compatibility.
        """
        await self.end_bullet_time()

    async def advance_turns(self, turns: int = 1) -> None:
        for _ in range(turns):
            await self.p1.beginning_phase()
            await self.p1.ending_phase()
            await self.p2.beginning_phase()
            await self.p2.ending_phase()

    async def trigger(self, card, hook_name: str, *args):
        hook = getattr(card, hook_name)
        card.player.action_store.start_record()
        try:
            return await hook(*args)
        finally:
            card.player.action_store.end_record()

    async def move_to_graveyard(self, creature: Creature) -> None:
        """
        Move a battlefield creature to graveyard with proper action record scope.
        """
        owner = creature.player
        owner.action_store.start_record()
        await creature.when_move_to_graveyard(owner, owner.opponent)
        owner.action_store.end_record()


class CardTestCaseBase(unittest.IsolatedAsyncioTestCase):
    def make_env(self) -> CardTestEnv:
        return CardTestEnv()

    def assert_partial_state(self, actual: dict[str, Any], expected: dict[str, Any]) -> None:
        for key, value in expected.items():
            self.assertIn(key, actual)
            if isinstance(value, dict):
                self.assertIsInstance(actual[key], dict)
                self.assert_partial_state(actual[key], value)
            else:
                self.assertEqual(actual[key], value)

    def _card_zone(self, card) -> str:
        owner = card.player
        zone_map = {
            "hand": owner.hand,
            "battlefield": owner.battlefield,
            "land_area": owner.land_area,
            "graveyard": owner.graveyard,
            "library": owner.library,
            "exile_area": owner.exile_area,
        }
        for zone, cards in zone_map.items():
            if card in cards:
                return zone
        return "unknown"

    def assert_state(self, target, expected: dict[str, Any]) -> None:
        """
        Unified state assertion for Player/Card.
        Supports partial checks via `expected`.
        Examples:
          self.assert_state(player, {"life": 18, "mana": {"U": 2}})
          self.assert_state(card, {"zone": "battlefield", "state": (5, 3)})
          self.assert_state(card, {"buffs_contains": ["Hexproof"]})
        """
        if isinstance(target, Player):
            actual = {
                "name": target.name,
                "life": target.life,
                "mana": dict(target.mana),
                "flags": dict(target.flag_dict),
                "counters": dict(target.counter_dict),
                "hand_count": len(target.hand),
                "battlefield_count": len(target.battlefield),
                "land_count": len(target.land_area),
                "graveyard_count": len(target.graveyard),
                "exile_count": len(target.exile_area),
                "library_count": len(target.library),
            }
            self.assert_partial_state(actual, expected)
            return

        actual = {
            "name": getattr(target, "name", ""),
            "type": getattr(target, "type", ""),
            "owner": target.player.name,
            "zone": self._card_zone(target),
            "flags": dict(getattr(target, "flag_dict", {})),
            "counters": dict(getattr(target, "counter_dict", {})),
            "buffs": [type(buff).__name__ for buff in getattr(target, "buffs", [])],
        }
        if hasattr(target, "state"):
            actual["state"] = tuple(target.state)
        if hasattr(target, "actual_power"):
            actual["actual_power"] = target.actual_power
        if hasattr(target, "actual_live"):
            actual["actual_live"] = target.actual_live
        if hasattr(target, "power"):
            actual["power"] = target.power
        if hasattr(target, "live"):
            actual["live"] = target.live

        expected_copy = dict(expected)
        buffs_contains = expected_copy.pop("buffs_contains", None)
        if buffs_contains is not None:
            for buff_name in buffs_contains:
                self.assertIn(buff_name, actual["buffs"])

        self.assert_partial_state(actual, expected_copy)


def load_card_class_from_path(relative_model_path: str, class_name: str):
    model_path = SRC_ROOT / relative_model_path
    module_name = f"card_test_{relative_model_path.replace('/', '_').replace('.', '_')}"
    spec = importlib.util.spec_from_file_location(module_name, model_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {model_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, class_name)
