"""Plan CVAE trainer with balanced CardFusion binding-pair supervision."""

import torch
import torch.nn.functional as F

from game.rlearning.module.state_space.EntityTransitionPlanBirth import EntityTransitionPlanBirthCVAETrainer


def balanced_pair_bce(logits, target, valid):
    """Balance sparse positive pairs against the many absent effect-target cells."""
    if not valid.any():
        return logits.new_zeros(())
    values = F.binary_cross_entropy_with_logits(logits[valid], target[valid], reduction="none")
    positive = target[valid].bool()
    return (values[positive].mean() + values[~positive].mean()) * 0.5


def masked_smooth_l1(prediction, target, valid):
    """Return zero for an empty mask and Huber loss for valid numeric attributes."""
    return F.smooth_l1_loss(prediction[valid], target[valid]) if valid.any() else prediction.new_zeros(())


def card_attribute_losses(prediction, card_used):
    """Recover categorical and numeric card inputs from h_card with valid combat masking."""
    has_state = card_used["has_state"].float()
    combat_valid = has_state.bool()
    losses = {
        "card_attribute_type_loss": F.cross_entropy(prediction["card_type"], card_used["card_type"].long()),
        "card_attribute_special_loss": F.binary_cross_entropy_with_logits(prediction["special_type"], card_used["special_type"].float()),
        "card_attribute_mana_loss": F.smooth_l1_loss(prediction["mana_cost"], card_used["mana_cost"].float()),
        "card_attribute_attack_loss": masked_smooth_l1(prediction["attack"], card_used["attack"].float(), combat_valid),
        "card_attribute_defend_loss": masked_smooth_l1(prediction["defend"], card_used["defend"].float(), combat_valid),
        "card_attribute_has_state_loss": F.binary_cross_entropy_with_logits(prediction["has_state"], has_state),
    }
    losses["card_attribute_loss"] = sum(losses.values())
    return losses


class EntityTransitionPlanBirthBindingCVAETrainer(EntityTransitionPlanBirthCVAETrainer):
    """Add binding-pair loss while retaining the exact B transition architecture."""
    def _forward(self, batch, models, isTrain, step, epoch):
        """Append auxiliary pair loss and diagnostics after the inherited CVAE losses."""
        loss = super()._forward(batch, models, isTrain, step, epoch)
        logits = models["BindingPairHead"](batch["h_card"])
        target, valid = batch["binding_pair_target"], batch["binding_pair_valid"]
        pair_loss = balanced_pair_bce(logits, target, valid)
        loss["binding_pair_loss"] = pair_loss
        loss["total_loss"] = loss["total_loss"] + pair_loss * float(self.config.get("w_card_binding_pair_loss", 0.05))
        with torch.no_grad():
            positive = target[valid].bool()
            predicted = logits[valid].sigmoid() >= 0.5
            loss["binding_pair_recall"] = (predicted[positive].float().mean() if positive.any() else pair_loss.new_zeros(()))
            loss["binding_pair_precision"] = ((predicted & positive).sum().float() / predicted.sum().clamp_min(1))
            loss["binding_pair_valid_fraction"] = valid.float().mean()
        if "CardAttributeHeads" in models:
            prediction = models["CardAttributeHeads"](batch["h_card"])
            attributes = card_attribute_losses(prediction, batch["card_used"])
            loss.update(attributes)
            loss["total_loss"] = loss["total_loss"] + attributes["card_attribute_loss"] * float(self.config.get("w_card_attribute_loss", 0.05))
            with torch.no_grad():
                loss["card_attribute_type_accuracy"] = (prediction["card_type"].argmax(dim=-1) == batch["card_used"]["card_type"].long()).float().mean()
                loss["card_attribute_mana_mae"] = (prediction["mana_cost"] - batch["card_used"]["mana_cost"].float()).abs().mean()
                loss["card_attribute_has_state_accuracy"] = ((prediction["has_state"] >= 0) == batch["card_used"]["has_state"].bool()).float().mean()
        return loss
