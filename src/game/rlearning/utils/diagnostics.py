import faulthandler
import json
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import pickle
import sys
import time
import traceback
from collections import deque

from game.rlearning.utils.common import CHECKPOINT_ROOT_PATH


def failure_directory(config):
    if config.get("diagnostics_dir"):
        return str(Path(config["diagnostics_dir"]).expanduser().resolve())
    from initinal_file import ORGPATH
    from game.rlearning.utils.file import read_yaml
    agent = read_yaml(str(Path(ORGPATH) / config["agent_config"]))
    stamp = time.strftime("%Y%m%d-%H%M%S")
    return str(Path(CHECKPOINT_ROOT_PATH) / agent["log_dir"] / "failures" / f"{stamp}-{os.getpid()}")


def fatal_cuda_error(error):
    message = str(error).lower()
    markers = ("unspecified launch failure", "illegal memory access", "device-side assert", "context is destroyed", "cuda error: unknown error", "cuda failure 719", "cuda failure 700", "cuda failure 710")
    return any(marker in message for marker in markers)


def describe_state(state):
    try:
        source = state.get("action_embedding_state", state)
        zones = {}
        for group in ("card_zones", "board_zones"):
            for name, zone in source.get(group, {}).items():
                names = zone.get("card_names", ())
                zones[name] = [str(value) for value in names if str(value)]
        candidates = state.get("candidate_actions", ())
        return {"zones": zones, "candidate_indices": [int(item["index"]) for item in candidates]}
    except Exception as error:
        return {"summary_error": repr(error)}


def describe_room(room):
    def card_info(card):
        info = {"class": type(card).__name__}
        for name in ("name", "card_id", "mana_cost", "content", "effect_params", "flag_dict", "counter_dict"):
            info[name] = getattr(card, name, None)
        try:
            info["state"] = getattr(card, "state", None)
        except Exception as error:
            info["state_error"] = repr(error)
        info["buffs"] = [{"class": type(buff).__name__, **{name: getattr(buff, name, None) for name in ("card_type", "content", "power", "live", "turn_counter")}} for buff in getattr(card, "buffs", ())]
        return info
    result = {"flags": room.flag_dict.copy(), "counters": room.counter_dict.copy(), "players": {}, "stack": []}
    result["active_player"] = getattr(getattr(room, "active_player", None), "name", None)
    for name, player in room.players.items():
        info = {"life": player.life, "mana": player.mana.copy(), "flags": player.flag_dict.copy(), "counters": player.counter_dict.copy()}
        for zone in ("hand", "battlefield", "land_area", "graveyard", "library", "exile_area"):
            info[zone] = [card_info(card) for card in getattr(player, zone, ())]
        result["players"][name] = info
    result["stack"] = [{"card": card_info(item["card"]), "message": item.get("message")} for item in room.stack]
    return result


def describe_action(agent, action):
    action = int(action)
    card = None
    if action >= 32:
        slot = (action - 32) // 33
        if slot < len(agent.hand):
            card = agent.hand[slot]
    elif 2 <= action <= 11 and action - 2 < len(agent.battlefield):
        card = agent.battlefield[action - 2]
    elif 12 <= action <= 21 and action - 12 < len(agent.battlefield):
        card = agent.battlefield[action - 12]
    elif 22 <= action <= 31 and action - 22 < len(agent.land_area):
        card = agent.land_area[action - 22]
    return {"agent": agent.name, "action": action, "card_class": type(card).__name__ if card is not None else None, "card_name": getattr(card, "name", None), "card_id": getattr(card, "card_id", None)}


def validate_cpu_batch(batch):
    import torch
    def check(value, path):
        if isinstance(value, dict):
            for key, item in value.items():
                check(item, f"{path}.{key}")
        elif torch.is_tensor(value):
            if value.device.type != "cpu":
                raise ValueError(f"Expected CPU input before device transfer: {path} on {value.device}")
            if value.is_floating_point() and not torch.isfinite(value).all().item():
                raise ValueError(f"Non-finite model input: {path}, shape={tuple(value.shape)}")
    check(batch, "batch")
    candidates = batch.get("candidates")
    if candidates is not None and "lengths" in batch:
        mask = candidates["mask"].bool()
        valid = torch.arange(mask.shape[1])[None] < batch["lengths"][:, None]
        empty = valid & ~mask.any(dim=-1)
        if empty.any().item():
            raise ValueError(f"No legal candidates at batch/time indices: {empty.nonzero().tolist()}")
        indices = candidates["indices"][mask]
        actions = candidates["actions"][mask]
        if ((indices < 0) | (indices >= 362)).any().item():
            raise ValueError(f"Invalid environment action indices: {indices.tolist()}")
        if ((actions < -1) | (actions > 35)).any().item():
            raise ValueError(f"Invalid action embedding indices: {actions.tolist()}")


class FailureRecorder:
    def __init__(self, directory, role):
        self.directory = Path(directory or Path(CHECKPOINT_ROOT_PATH) / "failures")
        self.directory.mkdir(parents=True, exist_ok=True)
        self.role = role
        self.prefix = self.directory / f"{role}-{os.getpid()}"
        self.context = {}
        self.history = deque(maxlen=12)
        self.inputs = None
        self.report = None
        self.logger = logging.Logger(f"magic-failure-{role}-{os.getpid()}")
        handler = RotatingFileHandler(str(self.prefix) + ".events.jsonl", maxBytes=2 * 1024 * 1024, backupCount=1, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(message)s"))
        self.logger.addHandler(handler)
        self.fault_file = open(str(self.prefix) + ".fault.log", "a", buffering=1)
        faulthandler.enable(file=self.fault_file, all_threads=True)
        self.mark("process_started", role=role, pid=os.getpid())

    def mark(self, stage, **details):
        self.context.update(details)
        self.context["stage"] = stage
        event = {"time": time.time(), "stage": stage, **details}
        self.history.append(event)
        self.logger.info(json.dumps(event, ensure_ascii=False, default=str))

    def capture(self, error, inputs=None):
        existing = getattr(error, "_magic_failure_report", None)
        if existing:
            self.report = existing
            return existing
        report = {"time": time.time(), "pid": os.getpid(), "role": self.role, "exception": type(error).__name__, "message": str(error), "fatal_cuda": fatal_cuda_error(error), "context": self.context.copy(), "recent_events": list(self.history), "traceback": "".join(traceback.format_exception(type(error), error, error.__traceback__))}
        event_prefix = str(self.prefix) + f"-{time.time_ns()}"
        path = event_prefix + ".error.json"
        payload = self.inputs if inputs is None else inputs
        try:
            if payload is not None:
                self._check_cpu_snapshot(payload)
                snapshot = event_prefix + ".inputs.pkl"
                with open(snapshot, "wb") as file:
                    pickle.dump(payload, file, protocol=pickle.HIGHEST_PROTOCOL)
                report["input_snapshot"] = snapshot
        except Exception as snapshot_error:
            report["snapshot_error"] = repr(snapshot_error)
        try:
            content = json.dumps(report, ensure_ascii=False, indent=2, default=str)
            Path(path).write_text(content, encoding="utf-8")
            Path(str(self.prefix) + ".error.json").write_text(content, encoding="utf-8")
            self.logger.error(json.dumps({"stage": "exception", "report": path, "message": str(error)}, ensure_ascii=False))
            self.report = path
            try:
                error._magic_failure_report = path
            except Exception:
                pass
            sys.stderr.write(f"\n[{self.role}] Failure report: {path}\n")
            sys.stderr.flush()
        except Exception as log_error:
            sys.stderr.write(f"\nFailure logging failed: {log_error!r}\n{report['traceback']}\n")
            path = None
        return path

    def _check_cpu_snapshot(self, value):
        if isinstance(value, dict):
            for item in value.values():
                self._check_cpu_snapshot(item)
        elif isinstance(value, (list, tuple)):
            for item in value:
                self._check_cpu_snapshot(item)
        elif type(value).__module__.startswith("torch") and hasattr(value, "device"):
            if value.device.type != "cpu":
                raise ValueError(f"Refusing to copy a {value.device} tensor after failure")

    @staticmethod
    def failure_hint(directory, role, pid):
        prefix = Path(directory) / f"{role}-{pid}"
        path = Path(str(prefix) + ".error.json")
        if path.exists():
            try:
                report = json.loads(path.read_text(encoding="utf-8"))
                return f"{report['exception']}: {report['message']}\nFailure report: {path}"
            except Exception:
                return f"Failure report: {path}"
        return f"Process logs: {prefix}.events.jsonl and {prefix}.fault.log"
