"""Export a training checkpoint as a standalone Jina Embeddings v5 model.

Example:
    python src/game/rlearning/scripts/convert_jina_checkpoint.py \
        --root /mnt/data/trainData/checkpoints/text_encoder/text_encoder_v4 \
        --step 55000
"""

import argparse
import json
import shutil
from pathlib import Path

import torch
from huggingface_hub import snapshot_download
from safetensors import safe_open
from safetensors.torch import save_file


MODEL_ID = "jinaai/jina-embeddings-v5-text-small"
ENCODER_PREFIX = "_encoder.base_model.model."


def tensor_keys(path):
    with safe_open(path, framework="pt", device="cpu") as weights:
        return set(weights.keys())


def require_same_keys(actual, expected, name):
    if actual != expected:
        raise RuntimeError(
            f"{name} keys do not match the official model "
            f"(missing={len(expected - actual)}, extra={len(actual - expected)})."
        )


def base_weights(state_dict):
    """Remove the training wrapper and PEFT's ``base_layer`` wrapper."""
    weights = {}
    for name, tensor in state_dict.items():
        if name.startswith(ENCODER_PREFIX) and ".lora_" not in name:
            name = name.removeprefix(ENCODER_PREFIX).replace(".base_layer.", ".")
            weights[name] = tensor.contiguous()
    return weights


def adapter_weights(state_dict, task):
    """Select one task adapter and restore the official PEFT key names."""
    weights = {}
    for kind in ("lora_A", "lora_B"):
        source = f".{kind}.{task}.weight"
        target = f".{kind}.weight"
        for name, tensor in state_dict.items():
            if source in name:
                weights[name.removeprefix("_encoder.").replace(source, target)] = (
                    tensor.contiguous()
                )
    return weights


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True, help="Training directory")
    parser.add_argument("--step", type=int, required=True, help="Checkpoint step")
    parser.add_argument(
        "--output",
        type=Path,
        help="Export directory (default: <root>/jina_embeddings_v5_step_<step>)",
    )
    parser.add_argument(
        "--base-model",
        type=Path,
        help="Local official Jina snapshot; downloads/uses the Hugging Face cache by default",
    )
    args = parser.parse_args()

    checkpoint = args.root / "ckpt" / f"g_{args.step}"
    if not checkpoint.is_file():
        sibling = args.root / "ckpt" / f"d_{args.step}"
        hint = f"; {sibling.name} only contains optimizer state" if sibling.is_file() else ""
        raise FileNotFoundError(f"Model checkpoint not found: {checkpoint}{hint}")

    output = args.output or args.root / f"jina_embeddings_v5_step_{args.step}"
    if output.exists():
        raise FileExistsError(f"Output already exists: {output}")

    base_model = args.base_model or Path(snapshot_download(MODEL_ID))
    state_dict = torch.load(checkpoint, map_location="cpu", weights_only=True)["TextEncoder"]
    config = json.loads((base_model / "config.json").read_text())

    base = base_weights(state_dict)
    require_same_keys(set(base), tensor_keys(base_model / "model.safetensors"), "Base model")
    adapters = {task: adapter_weights(state_dict, task) for task in config["task_names"]}
    for task, weights in adapters.items():
        expected = tensor_keys(base_model / "adapters" / task / "adapter_model.safetensors")
        require_same_keys(set(weights), expected, f"{task} adapter")

    # Keep config, tokenizer, remote code and adapter configs from the official snapshot.
    shutil.copytree(
        base_model,
        output,
        ignore=shutil.ignore_patterns("model.safetensors", "adapter_model.safetensors"),
    )
    save_file(base, output / "model.safetensors")
    for task, weights in adapters.items():
        save_file(weights, output / "adapters" / task / "adapter_model.safetensors")

    print(f"Exported step {args.step} to {output}")


if __name__ == "__main__":
    main()
