import torch
import numpy as np
from pathlib import Path
import json
import random

from game.rlearning.utils.baseDataset import BaseDataset
from game.rlearning.utils.data import batch_to_cuda, detach_cuda, to_cpu, to_cuda
import game.rlearning.utils.log as log
from game.rlearning.data_preprocess.spec_render import render_candidate_card
from game.rlearning.data_preprocess.candidate import (
    prepare_candidate_binding,
    validate_candidate_spec,
)

# ============================================================
# Basic path utils
# ============================================================

def get_by_path(data, path: str):
    """
    path example:
        "self_life"
        "stack&stack_cards&card_types"
    """
    value = data
    for k in path.split("&"):
        value = value[k]
    return value

def nested_get(d, keys):
    for k in keys:
        if not isinstance(d, dict) or k not in d:
            return None
        d = d[k]
    return d


def nested_set(d, keys, value):
    cur = d
    for k in keys[:-1]:
        if k not in cur:
            cur[k] = {}
        cur = cur[k]
    cur[keys[-1]] = value


def collate_paths(batch, string_keys=None, tensor_keys=None):
    """
    batch: list[sample dict]

    string_keys:
        保持为 list[str]，比如 card_used&description

    tensor_keys:
        转成 torch.Tensor，比如 card_used&mana_cost
    """
    string_keys = string_keys or []
    tensor_keys = tensor_keys or []

    result = {}

    for path in string_keys:
        keys = path.split("&")
        values = [nested_get(sample, keys) for sample in batch]
        nested_set(result, keys, values)

    for path in tensor_keys:
        keys = path.split("&")
        values = [nested_get(sample, keys) for sample in batch]

        # 如果是 None，跳过
        if values[0] is None:
            continue

        # 如果误传了字符串字段，就保持 list，不强转 Tensor
        if isinstance(values[0], str):
            nested_set(result, keys, values)
            continue

        arr = np.stack(
            [np.asarray(v) for v in values],
            axis=0,
        )

        nested_set(result, keys, torch.as_tensor(arr))

    return result
def stack_path_numpy(batch, path: str, dtype=np.float32):
    """
    batch: list[dict]
    return: np.ndarray, stacked on axis=0
    """
    values = []

    for sample in batch:
        value = get_by_path(sample, path)
        value = np.asarray(value, dtype=dtype)
        values.append(value)

    return np.stack(values, axis=0)


def ensure_list(x):
    """
    你的原始 get_state(data) 假设 data 是 list。
    这里兼容一下：
        data 是 dict  -> 包成 [data]
        data 是 list  -> 原样使用
    """
    if isinstance(x, (list, tuple)):
        return x
    return [x]


def recursive_stack_to_tensor(items):
    """
    把 list[nested_dict] stack 成 nested tensor dict。

    example:
        items = [
            {"a": np.array([1, 2]), "b": {"c": np.array([3])}},
            {"a": np.array([4, 5]), "b": {"c": np.array([6])}},
        ]

        return:
            {
                "a": Tensor [2, 2],
                "b": {
                    "c": Tensor [2, 1]
                }
            }
    """
    first = items[0]

    if isinstance(first, dict):
        return {
            k: recursive_stack_to_tensor([item[k] for item in items])
            for k in first.keys()
        }

    arr = np.stack(items, axis=0)
    return torch.as_tensor(arr)


# ============================================================
# Raw state -> structured numpy state
# ============================================================

def collate_card_zone_numpy(batch, prefix: str):
    """
    prefix:
        "card_hand"
        "card_library"
        "card_graveyard"
        "stack&stack_cards"

    return shape usually:
        card_types:         [T, N]
        card_costs:         [T, N, 6]
        card_special_types: [T, N, S]
        card_atks:          [T, N]
        card_hps:           [T, N]
        card_has_state:     [T, N]
        card_mask:          [T, N]
    """
    return {
        "card_types": stack_path_numpy(
            batch,
            f"{prefix}&card_types",
            dtype=np.int64,
        ),
        "card_costs": stack_path_numpy(
            batch,
            f"{prefix}&card_costs",
            dtype=np.float32,
        ),
        "card_special_types": stack_path_numpy(
            batch,
            f"{prefix}&card_special_types",
            dtype=np.float32,
        ),
        "card_atks": stack_path_numpy(
            batch,
            f"{prefix}&card_atks",
            dtype=np.float32,
        ),
        "card_hps": stack_path_numpy(
            batch,
            f"{prefix}&card_hps",
            dtype=np.float32,
        ),
        "card_has_state": stack_path_numpy(
            batch,
            f"{prefix}&card_has_state",
            dtype=np.float32,
        ),
        "card_mask": stack_path_numpy(
            batch,
            f"{prefix}&card_mask",
            dtype=np.float32,
        ),
    }


def collate_board_zone_numpy(batch, prefix: str):
    """
    prefix:
        "self_board"
        "oppo_board"

    这里先按你现有数据结构写。
    如果 board 里也有 card_types / card_costs，建议加进去。
    """
    return {
        "card_special_types": stack_path_numpy(
            batch,
            f"{prefix}&card_special_types",
            dtype=np.float32,
        ),
        "card_atks": stack_path_numpy(
            batch,
            f"{prefix}&card_atks",
            dtype=np.float32,
        ),
        "card_hps": stack_path_numpy(
            batch,
            f"{prefix}&card_hps",
            dtype=np.float32,
        ),
        "card_has_state": stack_path_numpy(
            batch,
            f"{prefix}&card_has_state",
            dtype=np.float32,
        ),
        "card_mask": stack_path_numpy(
            batch,
            f"{prefix}&card_mask",
            dtype=np.float32,
        ),
    }


def get_state(data):
    """
    把原始 state 转成适合 Transformer Encoder 使用的结构。

    return:
        {
            "global_state": [T, G],
            "card_zones": {
                "hand": {...},
                "library": {...},
                "graveyard": {...},
                "stack_cards": {...},
            },
            "stack_extra": {
                "player_one_hot": [T, P],
                "action_number": [T] or [T, 1],
            },
            "board_zones": {
                "self_board": {...},
                "oppo_board": {...},
            },
        }

    T 是你原始 data["state"] 里的时间步 / 状态数量。
    如果 data["state"] 本来就是单个 dict，则 T=1。
    """
    data = ensure_list(data)
    T = len(data)

    self_life = stack_path_numpy(
        data,
        "self_life",
        dtype=np.float32,
    ).reshape(T, -1)

    oppo_life = stack_path_numpy(
        data,
        "oppo_life",
        dtype=np.float32,
    ).reshape(T, -1)

    self_mana = stack_path_numpy(
        data,
        "self_mana",
        dtype=np.float32,
    ).reshape(T, -1)

    global_state = np.concatenate(
        [
            self_life,
            oppo_life,
            self_mana,
        ],
        axis=-1,
    ).astype(np.float32)

    card_zones = {
        "hand": collate_card_zone_numpy(
            data,
            "card_hand",
        ),
        "library": collate_card_zone_numpy(
            data,
            "card_library",
        ),
        "graveyard": collate_card_zone_numpy(
            data,
            "card_graveyard",
        ),
        "stack_cards": collate_card_zone_numpy(
            data,
            "stack&stack_cards",
        ),
    }

    stack_extra = {
        "player_one_hot": stack_path_numpy(
            data,
            "stack&player_one_hot",
            dtype=np.float32,
        ),
        "action_number": stack_path_numpy(
            data,
            "stack&action_number",
            dtype=np.int64,
        ),
    }

    board_zones = {
        "self_board": collate_board_zone_numpy(
            data,
            "self_board",
        ),
        "oppo_board": collate_board_zone_numpy(
            data,
            "oppo_board",
        ),
    }

    return {
        "global_state": global_state,
        "card_zones": card_zones,
        "stack_extra": stack_extra,
        "board_zones": board_zones,
    }


def _normalize_description(text):
    return " ".join(str(text).split())

def _load_jsonl(path):
    with path.open("r", encoding="utf-8") as stream:
        return [
            json.loads(line)
            for line in stream
            if line.strip()
        ]
def bindings_by_description_dict(config):
    default_path = (
        Path(__file__).resolve().parents[2]
        / "data/retrieval/parsed_cards.jsonl"
    )
    cards_path = Path(config.get("bindings_index_path", default_path))

    return {
        _normalize_description(description): card.get("bindings", [])
        for card in _load_jsonl(cards_path)
        if (description := card.get("ability") or card.get("index_text"))
    }



def render_library_dict(config):
    default_path = (
        Path(__file__).resolve().parents[2]
        / "data/retrieval/libraries"
    )
    library_path = Path(
        config.get("binding_library_path", default_path)
    )

    return {
        name: json.loads(
            (library_path / f"{name}.json").read_text(encoding="utf-8")
        )
        for name in ["amounts", "durations", "effects", "statics", "targets", "triggers"]
    }

def render_exact_description(bindings, library):
    candidate_bindings = [
        prepare_candidate_binding(binding)
        for binding in bindings
    ]

    for binding in candidate_bindings:
        validate_candidate_spec(binding, library)

    return render_candidate_card(candidate_bindings, library)
# ============================================================
# Dataset
# ============================================================

class CVAEDataset(BaseDataset):
    def __init__(self, config):
        super().__init__(config)
        self.set_extra()

    def __getitem__(self, idx):
        idx = idx % len(self.datas)
        return self.get_sample(self.datas[idx])
        
    def set_extra(self):
        self.extra = {
            "description_to_bindings": bindings_by_description_dict(self.config),
            "library": render_library_dict(self.config),
        }

    def encode_descriptions(self, descriptions):
        return {
            "input": descriptions,
            "attention_mask": None,
        }

    def augment_description(self, description):
        bindings = self.extra["description_to_bindings"].get(_normalize_description(description))
        if bindings and random.random() < self.config.get("binding_augmentation_probability",0.0):
            try:
                augmented_description = render_exact_description(
                    bindings,
                    self.extra["library"],
                )
            except (KeyError, TypeError, ValueError):
                pass
            else:
                return augmented_description
        return description

    def get_sample(self, data):
        """
        单个样本结构：

        return:
            {
                "state": nested numpy dict,
                "next_state": nested numpy dict,
                "action": one-hot np.ndarray,
                "card_used": raw card_used dict,
            }
        """
        result = {}
       
        result["state"] = get_state(data["state"])
        result["next_state"] = get_state(data["next_state"])

        action = int(data["action"])

        action_one_hot = np.zeros(
            self.config.get("action_space",362),
            dtype=np.float32,
        )
        action_one_hot[action] = 1.0

        result["action"] = action_one_hot
        result["action_index"] = np.asarray(action, dtype=np.int64)

        card_used = dict(data["state"]["card_used"])
        description = card_used["description"]
        card_used["description"] = self.augment_description(description)
        result["card_used"] = card_used
        return result

    def collate_state(self, batch, key: str):
        """
        key:
            "state"
            "next_state"

        return nested tensor dict.
        """
        states = [sample[key] for sample in batch]
        return recursive_stack_to_tensor(states)

    def collate_action(self, batch):
        action = np.stack(
            [sample["action"] for sample in batch],
            axis=0,
        ).astype(np.float32)

        action_index = np.stack(
            [sample["action_index"] for sample in batch],
            axis=0,
        ).astype(np.int64)

        return {
            "action": torch.as_tensor(action),
            "action_index": torch.as_tensor(action_index),
        }

    def collate_card_used_part(self, batch):
        """
        这里继续复用你 BaseDataset 里的 collate_card_used。
        我只把 action 从这里拿掉，action 单独 collate。
        """
        batch_card_used = self.collate_card_used(
            batch,
            [
                "card_used&description",
            ],
            [
                "card_used&similar_description",
                "card_used&special_type",
                "card_used&mana_cost",
                "card_used&color_identity",
                "card_used&attack",
                "card_used&defend",
                "card_used&has_state",
                "card_used&card_type",
            ],
        )

        descriptions = batch_card_used["card_used"]["description"]

        tokens = self.encode_descriptions(descriptions)

        batch_card_used["card_used"]["description"] = tokens["input"]
        if tokens["attention_mask"] is not None:
            batch_card_used["card_used"]["attention_mask"] = tokens["attention_mask"]

        return batch_card_used

    def collate_card_used_part(self, batch):
        """
        collate card_used，不依赖 BaseDataset.collate_card_used。

        输出:
            {
                "card_used": {
                    "description": LongTensor [B, L],
                    "attention_mask": LongTensor [B, L],
                    "similar_description":  LongTensor [B, L],
                    "special_type": Tensor,
                    "mana_cost": Tensor,
                    "attack": Tensor,
                    "defend": Tensor,
                    "has_state": Tensor,
                    "card_type": Tensor,
                }
            }
        """

        batch_card_used = collate_paths(
            batch,
            string_keys=[
                "card_used&description",
                "card_used&similar_description",
            ],
            tensor_keys=[
                
                "card_used&special_type",
                "card_used&mana_cost",
                "card_used&color_identity",
                "card_used&attack",
                "card_used&defend",
                "card_used&has_state",
                "card_used&card_type",
            ],
        )

        descriptions = batch_card_used["card_used"]["description"]
        similar_descriptions = batch_card_used["card_used"]["similar_description"]

        tokens = self.encode_descriptions(descriptions)
        similar_tokens = self.encode_descriptions(similar_descriptions)

        batch_card_used["card_used"]["description"] = tokens["input"]
        if tokens["attention_mask"] is not None:
            batch_card_used["card_used"]["attention_mask"] = tokens["attention_mask"]

        batch_card_used["card_used"]["similar_description"] = similar_tokens["input"]
        if similar_tokens["attention_mask"] is not None:
            batch_card_used["card_used"]["similar_attention_mask"] = similar_tokens["attention_mask"]

        return batch_card_used

    def collate_fn(self, batch):
        """
        最终返回：

        result["state"]
        result["next_state"]
        result["action"]
        result["action_index"]
        result["card_used"]

        其中 state / next_state 是 nested tensor dict，适合直接送入 Transformer Encoder。
        """
        result = {}

        result["state"] = self.collate_state(
            batch,
            key="state",
        )

        result["next_state"] = self.collate_state(
            batch,
            key="next_state",
        )

        result.update(
            self.collate_action(batch)
        )

        result.update(
            self.collate_card_used_part(batch)
        )

        return result
