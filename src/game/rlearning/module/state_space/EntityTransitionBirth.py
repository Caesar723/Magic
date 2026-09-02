"""Training support for source-aligned transitions with entity birth slots."""

import torch
import torch.nn.functional as F

import game.rlearning.utils.log as log
from game.rlearning.module.state_space.CVAE import (
    _stat_loss_options,
    masked_bce,
    masked_stat_class_loss,
)
from game.rlearning.module.state_space.EntityTransition import (
    EntityTransitionCVAETrainer,
)
from game.rlearning.net.state_space.EntityTransition import squeeze_entity_time_dim
from game.rlearning.synthesis.artifacts import (
    write_reconstruction_artifact,
    write_transition_space_artifact,
)
from game.rlearning.synthesis.entity_transition_birth import (
    align_birth_slots,
    entity_birth_reconstruction_metrics,
    entity_birth_transition_rows,
    state_from_entity_birth_prediction,
)
from game.rlearning.synthesis.entity_transition import state_from_entity_target
from game.rlearning.synthesis.projection import pca_project_2d
from game.rlearning.synthesis.state_space import (
    card_used_from_raw,
    describe_action,
    state_delta_from_target,
)
from game.rlearning.utils.data import batch_to_cuda


def _masked_cross_entropy(logits, target, valid_mask):
    if not valid_mask.any():
        return logits.new_zeros(())
    return F.cross_entropy(logits[valid_mask], target[valid_mask].long())


class EntityTransitionBirthCVAETrainer(EntityTransitionCVAETrainer):
    """Add set-prediction losses for source-free next-state entities."""

    def reconstruction_loss(self, batch):
        result = super().reconstruction_loss(batch)
        prediction = batch["pred_next"]
        births = prediction["births"]
        source = squeeze_entity_time_dim(batch["state"])
        target = squeeze_entity_time_dim(batch["next_state"])
        aligned = align_birth_slots(births, source, target)
        matched = aligned["matched"]
        stat_loss_options = _stat_loss_options(self.config)

        positive_weight = float(self.config.get("birth_presence_positive_weight", 4.0))
        presence_target = matched.float()
        result["birth_presence_loss"] = F.binary_cross_entropy_with_logits(
            births["presence"],
            presence_target,
            pos_weight=births["presence"].new_tensor(positive_weight),
        )

        result["birth_destination_loss"] = _masked_cross_entropy(
            births["destination_zone"],
            aligned["destination_zone"],
            matched,
        )
        result["birth_card_type_loss"] = _masked_cross_entropy(
            births["card_types"],
            aligned["card_types"],
            matched,
        )
        empty_source_mask = torch.zeros_like(matched)
        result["birth_card_cost_loss"] = masked_stat_class_loss(
            births["card_costs"],
            aligned["card_costs"],
            aligned["card_costs"],
            matched,
            empty_source_mask,
            value_scale=1.0,
            **stat_loss_options,
        )
        result["birth_special_type_loss"] = masked_bce(
            births["card_special_types"],
            aligned["card_special_types"],
            matched,
        )
        result["birth_has_state_loss"] = masked_bce(
            births["card_has_state"],
            aligned["card_has_state"],
            matched,
        )

        combat_valid = matched & aligned["card_has_state"].bool()
        birth_stat_losses = []
        for stat_name in ("card_atks", "card_hps"):
            birth_stat_losses.append(
                masked_stat_class_loss(
                    births[stat_name],
                    aligned[stat_name],
                    aligned[stat_name],
                    combat_valid,
                    empty_source_mask,
                    **stat_loss_options,
                )
            )
        result["birth_card_stat_loss"] = torch.stack(birth_stat_losses).sum()

        tapped_valid = matched & aligned["card_tapped_valid"].bool()
        result["birth_tapped_loss"] = masked_bce(
            births["card_tapped"],
            aligned["card_tapped"],
            tapped_valid,
        )

        attribute_loss = (
            result["birth_destination_loss"]
            + result["birth_card_type_loss"]
            + result["birth_card_cost_loss"]
            + result["birth_special_type_loss"]
            + result["birth_has_state_loss"]
            + result["birth_card_stat_loss"]
            + result["birth_tapped_loss"]
        )
        result["birth_attribute_loss"] = attribute_loss
        result["birth_loss"] = (
            float(self.config.get("w_birth_presence_loss", 1.0))
            * result["birth_presence_loss"]
            + float(self.config.get("w_birth_attribute_loss", 1.0))
            * attribute_loss
        )
        result["total_loss"] += (
            result["birth_loss"] * float(self.config.get("w_birth_loss", 1.0))
        )

        with torch.no_grad():
            predicted_count = (
                torch.sigmoid(births["presence"]) >= 0.5
            ).sum(dim=-1)
            result["birth_target_count"] = aligned["target_count"].float().mean()
            result["birth_matched_count"] = matched.float().sum(dim=-1).mean()
            result["birth_overflow_count"] = aligned["overflow_count"].float().mean()
            result["birth_count_mae"] = (
                predicted_count.float() - aligned["target_count"].float()
            ).abs().mean()
            if matched.any():
                predicted_destination = births["destination_zone"].argmax(dim=-1)
                result["birth_destination_accuracy"] = (
                    predicted_destination[matched]
                    == aligned["destination_zone"][matched]
                ).float().mean()
            else:
                result["birth_destination_accuracy"] = births["presence"].new_zeros(())

        return result

    @torch.no_grad()
    def _synthesis(self, models):
        """Write reconstruction artifacts that also render virtual births."""
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
            f"Birth-slot synthesis step {self.step}: encoding {transition_count} "
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
                selected_source_state = self._select_batch(source_state, selection)
                selected_target_state = self._select_batch(target_state, selection)

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
                        metrics = entity_birth_reconstruction_metrics(
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
                            "entity_transitions": entity_birth_transition_rows(
                                prediction,
                                selected_source_state,
                                selected_target_state,
                                reconstruction_index,
                            ),
                            "predicted_next_state": (
                                state_from_entity_birth_prediction(
                                    prediction,
                                    selected_source_state,
                                    reconstruction_index,
                                )
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
                            "reconstruction_type": "entity_transition_birth",
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
                    "Birth-slot synthesis step "
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
            f"Birth-slot synthesis step {self.step}: wrote "
            f"{reconstruction_path}, {transition_path}, and {card_fusion_path}."
        )
        return transition_path
