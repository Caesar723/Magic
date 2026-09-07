"""Plan-conditioned entity transition trainer with an identity-message branch."""

import torch

from game.rlearning.module.state_space.EntityTransitionPlanBirth import (
    EntityTransitionPlanBirthCVAETrainer,
)


class EntityTransitionPlanBirthZeroMessageCVAETrainer(
    EntityTransitionPlanBirthCVAETrainer
):
    """Train the plan-conditioned decoder to preserve state for zero message.

    The regular transition path is left unchanged.  During training, a
    configurable fraction of each batch is additionally decoded with both
    transition memories set to zero.  Those predictions are supervised against
    the current state, which defines the identity constraint
    ``D(state, zero_message) == state``.

    ``z`` and ``transition_plan`` are both cleared deliberately: in the plan
    conditioned decoder they are two separate sources of transition
    information, so clearing only ``z`` would not represent a zero message.
    """

    def _zero_message_percentage(self):
        percentage = float(self.config.get("zero_message_percentage", 0.0))
        if not 0.0 <= percentage <= 100.0:
            raise ValueError(
                "zero_message_percentage must be between 0 and 100, "
                f"got {percentage}."
            )
        return percentage

    def _zero_message_indices(self, batch_size, device, is_train):
        percentage = self._zero_message_percentage()
        if not is_train or percentage <= 0.0 or batch_size <= 0:
            return torch.empty(0, dtype=torch.long, device=device)

        count = int(round(batch_size * percentage / 100.0))
        count = max(1, min(batch_size, count))
        return torch.randperm(batch_size, device=device)[:count]

    def decode(self, batch, models, isTrain, step, epoch):
        """Run the normal path and, when enabled, a zero-message path."""
        batch = super().decode(batch, models, isTrain, step, epoch)

        indices = self._zero_message_indices(
            batch_size=batch["z"].shape[0],
            device=batch["z"].device,
            is_train=isTrain,
        )
        batch["zero_message_indices"] = indices

        if indices.numel() == 0:
            batch["zero_message_pred"] = None
            return batch

        decoder = models["TokenTransitionStateDecoder"]
        state_tokens = batch["tokens_s"].index_select(0, indices)
        state_padding_mask = batch["pad_s"].index_select(0, indices)
        transition_vec = torch.zeros_like(batch["z"].index_select(0, indices))
        transition_plan = torch.zeros_like(
            batch["transition_plan"].index_select(0, indices)
        )

        batch["zero_message_pred"] = decoder(
            state_tokens=state_tokens,
            state_padding_mask=state_padding_mask,
            spans=batch["spans_s"],
            transition_vec=transition_vec,
            transition_plan=transition_plan,
        )
        return batch

    def reconstruction_loss(self, batch):
        """Add identity reconstruction loss for the selected zero messages."""
        result = super().reconstruction_loss(batch)
        indices = batch.get("zero_message_indices")
        zero_prediction = batch.get("zero_message_pred")

        if indices is None or indices.numel() == 0 or zero_prediction is None:
            result["zero_message_loss"] = batch["z"].new_zeros(())
            result["zero_message_count"] = batch["z"].new_zeros(())
            result["score"] = result["total_loss"].detach().add(1).reciprocal()
            return result

        current_state = self._select_batch(batch["state"], indices)
        identity_batch = dict(batch)
        identity_batch["state"] = current_state
        identity_batch["next_state"] = current_state
        identity_batch["pred_next"] = zero_prediction

        identity_result = super().reconstruction_loss(identity_batch)
        identity_loss = identity_result["total_loss"]
        result["zero_message_loss"] = identity_loss
        result["zero_message_count"] = batch["z"].new_tensor(
            float(indices.numel())
        )

        # Scale like adding selected identity samples to the ordinary batch:
        # at 10%, the auxiliary branch contributes about 10% of the normal
        # reconstruction objective when w_zero_message_loss == 1.
        batch_fraction = batch["z"].new_tensor(
            float(indices.numel()) / max(batch["z"].shape[0], 1)
        )
        result["total_loss"] += (
            identity_loss
            * float(self.config.get("w_zero_message_loss", 1.0))
            * batch_fraction
        )
        result["score"] = result["total_loss"].detach().add(1).reciprocal()
        return result
