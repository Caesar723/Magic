from __future__ import annotations

import json
from pathlib import Path

import torch

from game.rlearning.utils.baseDataset import WeightedDataset


class JinaTextEncoder(WeightedDataset):
    """Dataset for query--candidate relevance fine-tuning.

    Every ``<dataset_path>/query/<index>.json`` is paired with its matching
    ``<dataset_path>/candidates/<index>.json``. Each source item returns one
    query string, all candidate strings, and their relevance labels. The Jina
    encoder tokenizes the strings internally.
    """

    def __init__(self, config, mode="train"):
        super().__init__(config, mode)

    def collate_fn(self, batch):
        candidate_offsets = [0]
        candidates = []
        relevances = []

        for sample in batch:
            candidates.extend(sample["candidate"])
            relevances.append(sample["relevance"])
            candidate_offsets.append(candidate_offsets[-1] + len(sample["candidate"]))

        return {
            "query": [sample["query"] for sample in batch],
            "candidate": candidates,
            "relevance": torch.cat(relevances),
            "candidate_offsets": torch.as_tensor(candidate_offsets, dtype=torch.long),
        }

    def get_sample(self, data):
        """Read and return one query--candidate training pair."""
        dataset_path = Path(data["dataset_path"])
        sample_id = data["index"]

        with (dataset_path / "query" / f"{sample_id}.json").open(
            "r", encoding="utf-8"
        ) as file:
            query = json.load(file)
        with (dataset_path / "candidates" / f"{sample_id}.json").open(
            "r", encoding="utf-8"
        ) as file:
            candidates = json.load(file)["candidates"]

        return {
            "query": query["query_message"],
            "candidate": [candidate["card_ability"] for candidate in candidates],
            "relevance": torch.as_tensor(
                [candidate["relevance"] for candidate in candidates],
                dtype=torch.float32,
            ),
        }
