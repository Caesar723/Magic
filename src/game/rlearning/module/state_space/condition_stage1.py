import torch
import torch.nn.functional as F

from game.rlearning.module.state_space.EntityTransitionSupportPlanBirthRawReconstruction import EntityTransitionSupportPlanBirthRawReconstructionCVAETrainer
from game.rlearning.module.state_space.EntityTransitionSupportPlanBirth import extract_entity_tokens
from game.rlearning.net.state_space.EntityTransition import squeeze_entity_time_dim
from game.rlearning.net.state_space.LatentEntitySelector import build_existing_change_targets, strict_topk_mask
from game.rlearning.synthesis.entity_transition import align_entity_transitions


class ConditionStage1Trainer(EntityTransitionSupportPlanBirthRawReconstructionCVAETrainer):
    def __init__(self, config, restore_step, rank=0, n_gpus=1, name="main"):
        super().__init__(config, restore_step, rank, n_gpus, name)

        if restore_step != 0:
            return

        for checkpoint_path in config.get("pretrained_checkpoints", []):
            state = torch.load(checkpoint_path, map_location="cpu", weights_only=True)

            for model_name, model in self._models.items():
                if model_name not in state:
                    continue
                if config["model"][model_name].get("ignore_state", False):
                    continue

                model.load_state_dict(state[model_name], strict=True)
                self.models_test[model_name].load_state_dict(state[model_name], strict=True)

    def encode(self, batch, models, isTrain, step, epoch):
        h_s, tokens_s, pad_s, spans_s = models["StateTransformerEncoder"](batch["state"])
        h_action = models["ActionEncoder"](batch["card_action_index"])
        card_used = batch["card_used"]

        pooled_text, raw_text_tokens, text_padding = models["ConditionJinaTokenEncoder"](
            card_used["description"], device=h_s.device
        )

        h_text = models["ConditionTextProjection"](pooled_text)
        text_tokens = models["ConditionTextProjection"](raw_text_tokens)

        h_card_attr = models["CardStateEncoder"](
            card_used["card_type"].long(),
            card_used["special_type"],
            card_used["mana_cost"],
            card_used["attack"],
            card_used["defend"],
            card_used["has_state"].long(),
            card_used["color_identity"],
        )
        h_card = models["CardFusion"](h_text, h_card_attr)

        fused_tokens, fusion_hidden = models["ConditionStateTextFusion"](
            state_tokens=tokens_s,
            text_tokens=text_tokens,
            state_padding=pad_s,
            text_padding=text_padding,
            return_hidden=True,
        )

        h_fused_state = fused_tokens[:, 0]
        transition_plan = models["TransitionPlanner"](
            h_card, h_action, h_fused_state, fused_tokens, pad_s
        )

        entity_tokens, entity_padding = extract_entity_tokens(fused_tokens, pad_s, spans_s)

        source_state = squeeze_entity_time_dim(batch["state"])
        next_state = squeeze_entity_time_dim(batch["next_state"])
        entity_alignment = align_entity_transitions(source_state, next_state)

        changed_mask, existing_count, birth_count = build_existing_change_targets(
            source_state, next_state, entity_alignment
        )

        mean_p, std_p = models["PriorEncoder"](h_card, h_action, h_fused_state)
        mean_q, std_q = models["TransitionSupportPosteriorEncoder"](
            h_card, h_action, h_fused_state,
            entity_tokens, changed_mask, entity_padding, birth_count
        )

        z = (
            mean_q + std_q * torch.randn_like(mean_q)
            if isTrain else mean_p + std_p * torch.randn_like(mean_p)
        )

        existing_count_logits = models["ExistingTransitionCountHead"](transition_plan, z)
        birth_count_logits = models["BirthCountHead"](transition_plan, z)
        selection_logits = models["LatentEntitySelector"](
            entity_tokens, transition_plan, z, entity_padding
        )

        predicted_existing_count = existing_count_logits.argmax(dim=-1)
        predicted_selected_mask = strict_topk_mask(
            selection_logits, predicted_existing_count, entity_padding
        )

        batch.update({
            "h_s": h_fused_state,
            "tokens_s": fused_tokens,
            "pad_s": pad_s,
            "spans_s": spans_s,
            "text_tokens": text_tokens,
            "text_padding": text_padding,
            "fusion_hidden": fusion_hidden,
            "entity_tokens": entity_tokens,
            "entity_padding_mask": entity_padding,
            "h_action": h_action,
            "h_card": h_card,
            "transition_plan": transition_plan,
            "changed_mask": changed_mask,
            "existing_count": existing_count,
            "birth_count": birth_count,
            "entity_alignment": entity_alignment,
            "mean_p": mean_p,
            "std_p": std_p,
            "mean_q": mean_q,
            "std_q": std_q,
            "z": z,
            "existing_count_logits": existing_count_logits,
            "birth_count_logits": birth_count_logits,
            "selection_logits": selection_logits,
            "predicted_existing_count": predicted_existing_count,
            "predicted_selected_mask": predicted_selected_mask,
        })
        return batch

    @staticmethod
    def _masked_cross_entropy(logits, target, valid):
        classes = logits.shape[-1]
        target = target.long().clamp(0, classes - 1)
        values = F.cross_entropy(
            logits.reshape(-1, classes), target.reshape(-1), reduction="none"
        ).reshape_as(target)

        valid = valid.float()
        return (values * valid).sum() / valid.sum().clamp_min(1.0)

    def _effect_loss(self, batch, state_tokens, models):
        start, end = batch["spans_s"]["global_state"]
        global_tokens = state_tokens[:, start:end]
        effects = models["ConditionQuantityEffectHead"](
            global_tokens, batch["transition_plan"]
        )

        valid = batch["event_valid"].bool()
        valid_player = valid.unsqueeze(-1).expand_as(batch["player_damage"])

        damage_loss = self._masked_cross_entropy(
            effects["damage_logits"], batch["player_damage"], valid_player
        )
        heal_loss = self._masked_cross_entropy(
            effects["heal_logits"], batch["player_heal"], valid_player
        )
        draw_loss = self._masked_cross_entropy(
            effects["draw_logits"], batch["draw_counts"], valid_player
        )
        return damage_loss + heal_loss + draw_loss

    def _forward(self, batch, models, isTrain, step, epoch):
        loss = super()._forward(batch, models, isTrain, step, epoch)

        final_loss = self._effect_loss(batch, batch["tokens_s"], models)
        intermediate_loss = batch["tokens_s"].new_zeros(())

        if batch["fusion_hidden"]:
            intermediate_loss = self._effect_loss(
                batch, batch["fusion_hidden"][0], models
            )

        effect_loss = final_loss + self.config.get(
            "w_intermediate_effect_loss", 0.05
        ) * intermediate_loss

        loss["effect_loss"] = effect_loss
        loss["total_loss"] += self.config.get("w_effect_loss", 0.1) * effect_loss
        return loss