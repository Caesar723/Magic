import torch
import torch.nn.functional as F

import game.rlearning.utils.log as log
from game.rlearning.module.state_space.CVAE import (
    CVAETrainer,
    _stat_loss_options,
    masked_stat_class_loss,
)
from game.rlearning.net.state_space.EntityTransition import (
    squeeze_entity_time_dim,
)
from game.rlearning.synthesis.artifacts import (
    write_reconstruction_artifact,
    write_transition_space_artifact,
)
from game.rlearning.synthesis.entity_transition import (
    align_next_entities,
    entity_reconstruction_metrics,
    entity_transition_rows,
    flatten_entity_predictions,
    state_from_entity_prediction,
    state_from_entity_target,
)
from game.rlearning.synthesis.projection import pca_project_2d
from game.rlearning.synthesis.state_space import (
    card_used_from_raw,
    describe_action,
    state_delta_from_target,
)
from game.rlearning.utils.data import batch_to_cuda


# ============================================================
# Trainer
# ============================================================


def _change_weights(
    changed,
    reference,
    *,
    changed_weight,
    unchanged_weight,
):
    """Assign a larger loss weight only where a value changed."""
    return torch.where(
        changed,
        reference.new_tensor(changed_weight),
        reference.new_tensor(unchanged_weight),
    )


def _change_weighted_bce(
    pred_logits,
    target_value,
    source_value,
    valid_mask,
    *,
    changed_weight,
    unchanged_weight,
    changed_mask=None,
):
    """Average BCE with a larger weight on values that changed."""
    loss = F.binary_cross_entropy_with_logits(
        pred_logits,
        target_value.float(),
        reduction="none",
    )
    valid = valid_mask.bool()
    while valid.ndim < loss.ndim:
        valid = valid.unsqueeze(-1)
    valid = valid.expand_as(loss)

    if changed_mask is None:
        changed_mask = source_value != target_value
    while changed_mask.ndim < loss.ndim:
        changed_mask = changed_mask.unsqueeze(-1)
    changed_mask = changed_mask.expand_as(loss)

    weights = _change_weights(
        changed_mask,
        loss,
        changed_weight=changed_weight,
        unchanged_weight=unchanged_weight,
    )
    weighted_valid = weights * valid.float()
    return (loss * weighted_valid).sum() / weighted_valid.sum().clamp_min(1.0)


def _change_weighted_stat_loss(
    pred_logits,
    target_value,
    source_value,
    valid_mask,
    source_mask,
    *,
    changed_weight,
    unchanged_weight,
    stat_loss_options,
    changed_mask=None,
):
    """Combine changed and unchanged stat losses with stable normalization."""
    if changed_mask is None:
        changed_mask = source_value != target_value
    changed = changed_mask.bool()
    changed_valid = valid_mask.bool() & changed
    unchanged_valid = valid_mask.bool() & ~changed

    changed_loss = masked_stat_class_loss(
        pred_logits,
        target_value,
        source_value,
        changed_valid,
        source_mask,
        **stat_loss_options,
    )
    unchanged_loss = masked_stat_class_loss(
        pred_logits,
        target_value,
        source_value,
        unchanged_valid,
        source_mask,
        **stat_loss_options,
    )

    changed_count = changed_valid.float().sum()
    unchanged_count = unchanged_valid.float().sum()
    normalizer = (
        changed_weight * changed_count
        + unchanged_weight * unchanged_count
    ).clamp_min(1.0)
    return (
        changed_weight * changed_count * changed_loss
        + unchanged_weight * unchanged_count * unchanged_loss
    ) / normalizer


class EntityTransitionCVAETrainer(CVAETrainer):
    """Train source-aligned location and dynamic-attribute predictions."""

    def reconstruction_loss(self, batch):
        prediction = batch["pred_next"]
        target = squeeze_entity_time_dim(batch["next_state"])
        source = squeeze_entity_time_dim(batch["state"])
        stat_loss_options = _stat_loss_options(self.config)
        changed_attribute_weight = float(
            self.config.get("changed_attribute_weight", 4.0)
        )
        unchanged_attribute_weight = float(
            self.config.get("unchanged_attribute_weight", 1.0)
        )
        changed_life_weight = float(
            self.config.get("changed_life_weight", 4.0)
        )
        unchanged_life_weight = float(
            self.config.get("unchanged_life_weight", 1.0)
        )

        result = {}
        result["total_loss"] = prediction["global_state"].new_zeros(())

        # 1. Keep life and global mana reconstruction unchanged.
        global_valid = torch.ones_like(
            target["global_state"],
            dtype=torch.bool,
        )
        life_changed = torch.zeros_like(global_valid)
        life_changed[:, :2] = (
            source["global_state"][:, :2]
            != target["global_state"][:, :2]
        )
        result["global_state_loss"] = _change_weighted_stat_loss(
            prediction["global_state"],
            target["global_state"],
            source["global_state"],
            global_valid,
            global_valid,
            changed_weight=changed_life_weight,
            unchanged_weight=unchanged_life_weight,
            stat_loss_options=stat_loss_options,
            changed_mask=life_changed,
        )
        result["total_loss"] += result["global_state_loss"] * self.config.get(
            "w_global_state_loss",
            1.0,
        )

        # 2. Align every next-state card with its source entity.
        source_entities, aligned_target = align_next_entities(source, target)
        predicted_entities = flatten_entity_predictions(prediction)
        source_valid = source_entities["card_mask"].bool()
        matched = aligned_target["matched"]

        # 3. Predict an absolute destination zone for every source card.
        location_ce = F.cross_entropy(
            predicted_entities["destination_zone"].flatten(0, 1),
            aligned_target["destination_zone"].flatten(),
            reduction="none",
        ).view_as(source_valid)
        moved = (
            aligned_target["destination_zone"]
            != source_entities["zone_indices"]
        )
        moved_weight = float(self.config.get("moved_location_weight", 8.0))
        location_weight = torch.where(
            moved,
            torch.full_like(location_ce, moved_weight),
            torch.ones_like(location_ce),
        )
        weighted_location_mask = location_weight * source_valid.float()
        result["location_loss"] = (
            location_ce * weighted_location_mask
        ).sum() / weighted_location_mask.sum().clamp_min(1.0)
        result["total_loss"] += result["location_loss"] * self.config.get(
            "w_card_location_loss",
            1.0,
        )

        with torch.no_grad():
            predicted_zone = predicted_entities["destination_zone"].argmax(
                dim=-1
            )
            location_correct = (
                predicted_zone == aligned_target["destination_zone"]
            )
            result["location_accuracy"] = (
                location_correct.float() * source_valid.float()
            ).sum() / source_valid.float().sum().clamp_min(1.0)

            moved_valid = moved & source_valid
            result["moved_location_accuracy"] = (
                location_correct.float() * moved_valid.float()
            ).sum() / moved_valid.float().sum().clamp_min(1.0)
            result["matched_card_rate"] = (
                matched.float() * source_valid.float()
            ).sum() / source_valid.float().sum().clamp_min(1.0)

        # 4. Predict dynamic metadata only for matched card instances.
        result["special_type_loss"] = _change_weighted_bce(
            predicted_entities["card_special_types"],
            aligned_target["card_special_types"],
            source_entities["card_special_types"],
            matched,
            changed_weight=changed_attribute_weight,
            unchanged_weight=unchanged_attribute_weight,
        )
        result["has_state_loss"] = _change_weighted_bce(
            predicted_entities["card_has_state"],
            aligned_target["card_has_state"],
            source_entities["card_has_state"],
            matched,
            changed_weight=changed_attribute_weight,
            unchanged_weight=unchanged_attribute_weight,
        )
        result["total_loss"] += (
            result["special_type_loss"] + result["has_state_loss"]
        ) * self.config.get("w_card_state_loss", 1.0)

        # 5. Attack and health are valid only for cards with combat stats.
        combat_valid = matched & aligned_target["card_has_state"].bool()
        source_combat_valid = (
            source_valid & source_entities["card_has_state"].bool()
        )
        stat_losses = []
        for stat_name in ("card_atks", "card_hps"):
            stat_losses.append(
                _change_weighted_stat_loss(
                    predicted_entities[stat_name],
                    aligned_target[stat_name],
                    source_entities[stat_name],
                    combat_valid,
                    source_combat_valid,
                    changed_weight=changed_attribute_weight,
                    unchanged_weight=unchanged_attribute_weight,
                    stat_loss_options=stat_loss_options,
                )
            )
        result["card_stat_loss"] = torch.stack(stat_losses).sum()
        result["total_loss"] += result["card_stat_loss"] * self.config.get(
            "w_card_stat_loss",
            1.0,
        )

        # 6. Tapped state is meaningful only on creature and land zones.
        tapped_valid = matched & aligned_target["card_tapped_valid"].bool()
        tapped_changed = (
            source_entities["card_tapped"]
            != aligned_target["card_tapped"]
        ) | (
            source_entities["card_tapped_valid"].bool()
            != aligned_target["card_tapped_valid"].bool()
        )
        result["tapped_loss"] = _change_weighted_bce(
            predicted_entities["card_tapped"],
            aligned_target["card_tapped"],
            source_entities["card_tapped"],
            tapped_valid,
            changed_weight=changed_attribute_weight,
            unchanged_weight=unchanged_attribute_weight,
            changed_mask=tapped_changed,
        )
        result["total_loss"] += result["tapped_loss"] * self.config.get(
            "w_card_tapped_loss",
            1.0,
        )
        result["score"] = result["total_loss"].detach().add(1).reciprocal()

        return result

    @torch.no_grad()
    def _synthesis(self, models):
        """Write linked entity reconstruction and latent-space artifacts."""
        dataset_size = len(self.dataset.datas)
        transition_count = min(
            int(self.config.get("synthesis_transition_items", 1000)),
            dataset_size,
        )
        reconstruction_count = min(
            int(self.config.get("synthesis_items", 20)),
            transition_count,
        )
        if transition_count <= 0:
            return None

        source_indices = self._synthesis_source_indices(
            dataset_size,
            transition_count,
        )
        highlight_vector_indices = self._synthesis_source_indices(
            transition_count,
            reconstruction_count,
        )
        highlight_sample_ids = {
            vector_index: f"{sample_number:03d}"
            for sample_number, vector_index in enumerate(highlight_vector_indices)
        }
        batch_size = max(
            1,
            int(
                self.config.get(
                    "synthesis_transition_batch_size",
                    self.config.get("dataloader", {}).get("batch_size", 32),
                )
            ),
        )

        synthesis_models = dict(models)
        if "TextEncoder" in self.models:
            synthesis_models["TextEncoder"] = self.models["TextEncoder"]

        vector_chunks = {
            "h_card": [],
            "mean_q": [],
            "std_q": [],
            "mean_p": [],
            "std_p": [],
            "z_sampled": [],
        }
        transition_records = []
        reconstruction_records = []

        log.info(
            f"Entity synthesis step {self.step}: encoding {transition_count} "
            f"transitions in batches of {batch_size}; "
            f"{reconstruction_count} reconstruction highlights."
        )

        for batch_start in range(0, transition_count, batch_size):
            batch_end = min(batch_start + batch_size, transition_count)
            batch_source_indices = source_indices[batch_start:batch_end]
            source_samples = [
                self.dataset.get_sample(self.dataset.datas[index])
                for index in batch_source_indices
            ]
            batch = batch_to_cuda(
                self.dataset.collate_fn(source_samples),
                self.rank,
            )
            batch = self.encode(
                batch,
                synthesis_models,
                isTrain=True,
                step=self.step,
                epoch=self.epoch,
            )

            for vector_name in vector_chunks:
                source_name = "z" if vector_name == "z_sampled" else vector_name
                vector_chunks[vector_name].append(
                    batch[source_name].detach().float().cpu()
                )

            source_state = squeeze_entity_time_dim(batch["state"])
            target_state = squeeze_entity_time_dim(batch["next_state"])
            for local_index, source_index in enumerate(batch_source_indices):
                vector_index = batch_start + local_index
                action_index = int(batch["action_index"][local_index].item())
                card_used = card_used_from_raw(
                    self._raw_card_used(self.dataset.datas[source_index])
                )
                reconstruction_sample_id = highlight_sample_ids.get(vector_index)
                transition_records.append(
                    {
                        "vector_index": vector_index,
                        "source_index": source_index,
                        "is_highlighted": reconstruction_sample_id is not None,
                        "reconstruction_sample_id": reconstruction_sample_id,
                        "state_delta": state_delta_from_target(
                            source_state,
                            target_state,
                            local_index,
                        ),
                        "card_model_description": self._synthesis_card_model_description(
                            batch["card_used"],
                            local_index,
                        ),
                        "action": {
                            "index": action_index,
                            "label": describe_action(action_index),
                        },
                        "card_used": card_used,
                    }
                )

            highlight_local_indices = [
                vector_index - batch_start
                for vector_index in highlight_vector_indices
                if batch_start <= vector_index < batch_end
            ]
            if highlight_local_indices:
                selection = torch.as_tensor(
                    highlight_local_indices,
                    dtype=torch.long,
                    device=batch["mean_q"].device,
                )
                predictions = self._synthesis_decoder_predictions(
                    synthesis_models,
                    batch,
                    selection,
                )
                selected_source_state = self._select_batch(
                    source_state,
                    selection,
                )
                selected_target_state = self._select_batch(
                    target_state,
                    selection,
                )

                for reconstruction_index, local_index in enumerate(
                    highlight_local_indices
                ):
                    vector_index = batch_start + local_index
                    source_index = source_indices[vector_index]
                    sample_id = highlight_sample_ids[vector_index]
                    action_index = int(
                        batch["action_index"][local_index].detach().cpu().item()
                    )
                    card_used = card_used_from_raw(
                        self._raw_card_used(self.dataset.datas[source_index])
                    )
                    prediction_views = {}
                    for prediction_key, prediction_info in predictions.items():
                        prediction = prediction_info["prediction"]
                        metrics = entity_reconstruction_metrics(
                            prediction,
                            selected_source_state,
                            selected_target_state,
                            reconstruction_index,
                        )
                        prediction_views[prediction_key] = {
                            "encoder": prediction_info["encoder"],
                            "label": prediction_info["label"],
                            "condition": prediction_info["condition"],
                            "metrics": metrics,
                            "entity_transitions": entity_transition_rows(
                                prediction,
                                selected_source_state,
                                selected_target_state,
                                reconstruction_index,
                            ),
                            "predicted_next_state": state_from_entity_prediction(
                                prediction,
                                selected_source_state,
                                reconstruction_index,
                            ),
                        }
                    prior_metrics = prediction_views["prior"]["metrics"]
                    posterior_metrics = prediction_views["posterior"]["metrics"]
                    transition_records[vector_index]["reconstruction_score"] = (
                        prior_metrics["score"]
                    )
                    transition_records[vector_index]["reconstruction_scores"] = {
                        "prior": prior_metrics["score"],
                        "posterior": posterior_metrics["score"],
                    }
                    reconstruction_records.append(
                        {
                            "schema_version": 2,
                            "reconstruction_type": "entity_transition",
                            "sample_id": sample_id,
                            "source_index": source_index,
                            "vector_index": vector_index,
                            "summary": {
                                "action": describe_action(action_index),
                                "score": prior_metrics["score"],
                                "prior_score": prior_metrics["score"],
                                "posterior_score": posterior_metrics["score"],
                            },
                            "input_state": state_from_entity_target(
                                selected_source_state,
                                reconstruction_index,
                            ),
                            "transition": {
                                "card_used": card_used,
                                "action": {
                                    "index": action_index,
                                    "label": describe_action(action_index),
                                },
                            },
                            "predictions": prediction_views,
                            "target_next_state": state_from_entity_target(
                                selected_target_state,
                                reconstruction_index,
                            ),
                        }
                    )

            if batch_end == transition_count or batch_end % (batch_size * 10) == 0:
                log.info(
                    "Entity synthesis step "
                    f"{self.step}: encoded {batch_end}/{transition_count} transitions."
                )

        vectors = {
            name: torch.cat(chunks, dim=0).numpy()
            for name, chunks in vector_chunks.items()
        }
        posterior_coordinates, posterior_projection = pca_project_2d(
            vectors["mean_q"],
            source="mean_q",
        )
        prior_coordinates, prior_projection = pca_project_2d(
            vectors["mean_p"],
            source="mean_p",
        )
        step_dir = f"{self.logdir}/synthesis/{self.step}"
        reconstruction_path = write_reconstruction_artifact(
            step_dir,
            step=self.step,
            samples=reconstruction_records,
        )
        transition_path = write_transition_space_artifact(
            step_dir,
            step=self.step,
            vectors=vectors,
            records=transition_records,
            coordinates=posterior_coordinates,
            projection=posterior_projection,
            coordinates_by_view={
                "prior": prior_coordinates,
                "posterior": posterior_coordinates,
            },
            projections={
                "prior": prior_projection,
                "posterior": posterior_projection,
            },
        )
        card_fusion_path = self._write_card_fusion_space_artifact(
            step_dir,
            synthesis_models,
            fallback_vectors=vectors["h_card"],
            transition_records=transition_records,
        )
        log.info(
            f"Entity synthesis step {self.step}: wrote "
            f"{reconstruction_path}, {transition_path}, and {card_fusion_path}."
        )
        return transition_path
