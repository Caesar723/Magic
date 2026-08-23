import json
import random
from pathlib import Path
from typing import Any, Mapping

from candidate import (
    build_valid_binding_pool, generate_exact_spec, generate_hard_spec,
    generate_near_spec, generate_random_spec, get_random_bindings,
    normalize_candidate_spec, validate_candidate_spec,
)
from query_render import render_query_card
from similarity import compute_binding_relevance
from spec_render import render_candidate_card


def load_library():
    library_dir = Path(__file__).resolve().parents[1] / "data/retrieval/libraries"
    names = "triggers durations statics amounts effects targets query_templates".split()
    return {name: json.loads((library_dir / f"{name}.json").read_text(encoding="utf-8")) for name in names}


def load_cards() -> list[dict]:
    """读取已解析卡牌，作为生成 query 的合法 binding 来源。"""
    cards_path = Path(__file__).resolve().parents[1] / "data/retrieval/parsed_cards.jsonl"
    with cards_path.open(encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def get_binding_from_card(card: dict):
    return card["bindings"]


def build_candidate_group(bindings, library, n_exact=2, n_near=3, n_hard=2, n_random=1, card_info=None, valid_binding_pool=None):
    """为一个 query binding 组生成固定比例的正、负候选卡牌。"""
    result = {"query_bindings": bindings, "query_message": render_query_card(bindings, library), "candidates": []}
    if card_info is not None:
        result["candidates"].append({"type": "card", "bindings": card_info["bindings"], "card_ability": card_info["ability"], "relevance": card_info["relevance"]})
    for type_name, count in (("exact", n_exact), ("near", n_near), ("hard", n_hard), ("random", n_random)):
        for _ in range(count):
            candidate_bindings = [generate_candidate_from_query(spec, type_name, library, valid_binding_pool) for spec in bindings]
            relevance = compute_binding_relevance(bindings, candidate_bindings)
            result["candidates"].append({"type": type_name, "bindings": candidate_bindings, "card_ability": render_candidate_card(candidate_bindings, library), "relevance": relevance})
    return result


def generate_candidate_from_query(query_spec: Mapping[str, Any], candidate_type: str, library=None, valid_binding_pool=None):
    """按候选类型变换一个 query binding，并保证结果可渲染。"""
    generators = {
        "exact": lambda: generate_exact_spec(query_spec),
        "near": lambda: generate_near_spec(query_spec, library, valid_binding_pool),
        "hard": lambda: generate_hard_spec(query_spec, valid_binding_pool),
        "random": lambda: generate_random_spec(query_spec, valid_binding_pool),
    }
    if candidate_type not in generators:
        raise ValueError(f"Unknown candidate type: {candidate_type}")
    spec = normalize_candidate_spec(generators[candidate_type]())
    if library is not None:
        validate_candidate_spec(spec, library)
    return spec


def _write_json(path: Path, data: dict):
    """先写入临时文件，再替换目标文件，避免留下半个 JSON。"""
    temp_path = path.with_suffix(f"{path.suffix}.tmp")
    with temp_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    temp_path.replace(path)


def _write_split_files(folder, binding_number, num_data, width, ratios, split_seed):
    """按比例打乱样本后写入 train、test、synthesis 三个索引文件。"""
    split_names = ("train", "test", "synthesis")
    if len(ratios) != len(split_names) or any(not isinstance(ratio, (int, float)) or ratio < 0 for ratio in ratios):
        raise ValueError("split ratios must be three non-negative numbers")
    ratio_sum = sum(ratios)
    if ratio_sum == 0:
        raise ValueError("at least one split ratio must be positive")

    raw_counts = [num_data * ratio / ratio_sum for ratio in ratios]
    counts = [int(count) for count in raw_counts]
    for index in sorted(range(3), key=lambda i: raw_counts[i] - counts[i], reverse=True)[:num_data - sum(counts)]:
        counts[index] += 1

    sample_indices = list(range(1, num_data + 1))
    random.Random(split_seed).shuffle(sample_indices)
    start = 0
    for name, count in zip(split_names, counts):
        with (folder / f"{name}.txt").open("w", encoding="utf-8") as file:
            file.write("index|binding_number\n")
            for position in range(start, start + count):
                sample_name = f"sample_{sample_indices[position]:0{width}d}"
                file.write(f"{sample_name}|{binding_number}\n")
        start += count
    return dict(zip(split_names, counts))


def generate_card_data():
    pass


def generate_fake_data(
    folder_name="fake_data_1bind_20260823", binding_number=1, num_data=1_000_000,
    train_ratio=0.8, test_ratio=0.1, synthesis_ratio=0.1, split_seed=42, output_root=None,
):
    """生成 query/candidates JSON，并在 total.txt 记录每个样本和 binding 数量。"""
    if not isinstance(binding_number, int) or binding_number < 1:
        raise ValueError("binding_number must be a positive integer")
    if not isinstance(num_data, int) or num_data < 1:
        raise ValueError("num_data must be a positive integer")
    if not folder_name or Path(folder_name).name != folder_name:
        raise ValueError("folder_name must be a single folder name")

    root = Path(output_root) if output_root is not None else Path(__file__).resolve().parents[4] / "data/text_data"
    folder = root / folder_name
    if folder.exists():
        raise FileExistsError(f"Output folder already exists: {folder}")

    query_dir, candidates_dir = folder / "query", folder / "candidates"
    query_dir.mkdir(parents=True)
    candidates_dir.mkdir()
    library = load_library()
    valid_binding_pool = build_valid_binding_pool(load_cards(), library)
    width = max(8, len(str(num_data)))

    with (folder / "total.txt").open("w", encoding="utf-8") as total_file:
        total_file.write("index|binding_number\n")
        for index in range(1, num_data + 1):
            sample_name = f"sample_{index:0{width}d}"
            bindings = get_random_bindings(valid_binding_pool, library, binding_number, binding_number)
            if len(bindings) != binding_number:
                raise ValueError(f"Cannot generate {binding_number} distinct effect bindings")
            group = build_candidate_group(bindings, library, valid_binding_pool=valid_binding_pool)
            _write_json(query_dir / f"{sample_name}.json", {"id": sample_name, "binding_number": binding_number, "query_bindings": group["query_bindings"], "query_message": group["query_message"]})
            _write_json(candidates_dir / f"{sample_name}.json", {"id": sample_name, "binding_number": binding_number, "candidates": group["candidates"]})
            total_file.write(f"{sample_name}|{binding_number}\n")
    split_counts = _write_split_files(folder, binding_number, num_data, width, (train_ratio, test_ratio, synthesis_ratio), split_seed)
    return {"folder": str(folder), "binding_number": binding_number, "num_data": num_data, "splits": split_counts}


if __name__ == "__main__":
    output_root="/home/a123456/Desktop/Magic/data/text_data"
    if 0:
        generate_fake_data(
            folder_name="fake_data_1bind_v1_20260823",
            binding_number=1,
            num_data=10,
            output_root=output_root,
        )

    if 1:
        generate_fake_data(
            folder_name="fake_data_2bind_v1_20260823",
            binding_number=2,
            num_data=100000,
            output_root=output_root,
        )
