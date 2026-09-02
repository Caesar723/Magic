"""Entity-transition samples augmented with parser-derived binding matrices."""

import numpy as np
import torch

from game.rlearning.data.retrieval.binding_labels import binding_pair_target
from game.rlearning.datasets.state_space.CVAE import _normalize_description
from game.rlearning.datasets.state_space.EntityTransition import EntityTransitionDataset


class EntityTransitionBindingDataset(EntityTransitionDataset):
    """Attach original-card bindings before description augmentation changes its text."""
    def get_sample(self, data):
        """Keep the regular transition sample and its parser bindings together."""
        sample = super().get_sample(data)
        description = data["state"]["card_used"]["description"]
        sample["binding_pairs"] = self.extra["description_to_bindings"].get(_normalize_description(description), [])
        return sample

    def collate_fn(self, batch):
        """Stack one multi-hot pair matrix per sample for GPU-ready auxiliary loss."""
        result = super().collate_fn(batch)
        labels = [binding_pair_target(sample["binding_pairs"]) for sample in batch]
        result["binding_pair_target"] = torch.as_tensor(np.stack([label[0] for label in labels]))
        result["binding_pair_valid"] = torch.as_tensor([label[1] for label in labels], dtype=torch.bool)
        return result
