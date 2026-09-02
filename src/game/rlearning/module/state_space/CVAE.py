
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import torch
import torch.nn.functional as F


from game.rlearning.utils.baseAgent import BaseTrainer
from game.rlearning.utils.data import batch_to_cuda
from game.rlearning.net.state_space.StateEncoder import squeeze_time_dim_state
from game.rlearning.synthesis.artifacts import (
    write_card_fusion_space_artifact,
    write_reconstruction_artifact,
    write_transition_space_artifact,
)
from game.rlearning.synthesis.projection import pca_project_2d
from game.rlearning.synthesis.state_space import (
    card_used_from_raw,
    describe_action,
    reconstruction_metrics,
    state_delta_from_target,
    state_from_prediction,
    state_from_target,
)
import game.rlearning.utils.log as log


def masked_bce(pred_logits, target_value, valid_mask):
    loss = F.binary_cross_entropy_with_logits(
        pred_logits,
        target_value.float(),
        reduction="none",
    )
    valid_mask = valid_mask.float()

    while valid_mask.ndim < loss.ndim:
        valid_mask = valid_mask.unsqueeze(-1)

    denom = valid_mask.expand_as(loss).sum().clamp_min(1.0)
    return (loss * valid_mask).sum() / denom


def _values_to_classes(values, num_classes, value_scale):
    return (values.float() * value_scale).round().long().clamp(
        0,
        num_classes - 1,
    )


def masked_stat_class_loss(
    pred_logits,
    target_value,
    source_value,
    valid_mask,
    source_mask,
    *,
    expected_l1_weight=1.0,
    unchanged_bonus=3.0,
    value_scale=None,
):
    """Combine class CE and expected-value L1 for masked discrete values."""

    # 1. Convert source and target values to discrete class indices.
    num_classes = pred_logits.shape[-1]
    if value_scale is None:
        value_scale = num_classes - 1

    target_class = _values_to_classes(target_value, num_classes, value_scale)
    source_class = _values_to_classes(source_value, num_classes, value_scale)

    # 2. Expand slot masks to match multi-channel values such as card costs.
    valid = valid_mask.bool()
    source_valid = source_mask.bool()
    while valid.ndim < target_class.ndim:
        valid = valid.unsqueeze(-1)
        source_valid = source_valid.unsqueeze(-1)

    valid = valid.expand_as(target_class)
    source_valid = source_valid.expand_as(target_class)
    if not valid.any():
        return pred_logits.new_zeros(())

    # 3. Give unchanged valid values an additional loss weight.
    unchanged = valid & source_valid & (source_class == target_class)
    slot_weights = 1.0 + float(unchanged_bonus) * unchanged.float()

    # 4. Compute cross-entropy independently for every valid value.
    flat_logits = pred_logits.reshape(-1, pred_logits.shape[-1])
    flat_target = target_class.reshape(-1)
    ce = F.cross_entropy(flat_logits, flat_target, reduction="none").reshape_as(
        target_class
    )

    # 5. Penalize the distance between the predicted expectation and target.
    probs = F.softmax(pred_logits, dim=-1)
    class_values = torch.arange(
        num_classes,
        device=pred_logits.device,
        dtype=pred_logits.dtype,
    )
    expected = (probs * class_values).sum(dim=-1)
    expected_l1 = (expected - target_class.float()).abs()

    # 6. Apply weights and masks, then average over valid values only.
    per_slot = ce + float(expected_l1_weight) * expected_l1
    valid = valid.float()
    weighted_loss = per_slot * slot_weights * valid
    return weighted_loss.sum() / valid.sum().clamp_min(1.0)


def _stat_loss_options(config):
    return {
        "expected_l1_weight": float(config.get("w_stat_expected_l1", 1.0)),
        "unchanged_bonus": float(config.get("unchanged_stat_bonus", 3.0)),
    }


def zone_reconstruction_loss(
    pred_zone,
    target_zone,
    source_zone,
    stat_loss_options,
    *,
    include_card_metadata,
):
    zone_loss = pred_zone["card_mask"].new_zeros(())

    # 所有 slot 都训练“这里是否有卡”
    target_mask = target_zone["card_mask"].float()
    zone_loss = zone_loss + F.binary_cross_entropy_with_logits(
        pred_zone["card_mask"],
        target_mask,
    )

    # 卡实际存在时，才训练其属性
    valid_mask = target_mask > 0.5
    if not valid_mask.any():
        return zone_loss

    if include_card_metadata:
        zone_loss = zone_loss + F.cross_entropy(
            pred_zone["card_types"][valid_mask],
            target_zone["card_types"][valid_mask].long(),
        )

        zone_loss = zone_loss + masked_stat_class_loss(
            pred_zone["card_costs"],
            target_zone["card_costs"],
            source_zone["card_costs"],
            valid_mask,
            source_zone["card_mask"],
            value_scale=1.0,
            **stat_loss_options,
        )

    zone_loss = zone_loss + masked_bce(
        pred_zone["card_special_types"],
        target_zone["card_special_types"],
        valid_mask,
    )

    source_mask = source_zone["card_mask"]
    for stat_name in ("card_atks", "card_hps"):
        zone_loss = zone_loss + masked_stat_class_loss(
            pred_zone[stat_name],
            target_zone[stat_name],
            source_zone[stat_name],
            valid_mask,
            source_mask,
            **stat_loss_options,
        )

    zone_loss = zone_loss + masked_bce(
        pred_zone["card_has_state"],
        target_zone["card_has_state"],
        valid_mask,
    )
    return zone_loss


class CVAETrainer(BaseTrainer):
    def __init__(self, config, restore_step, rank=0, n_gpus=1, name="main"):
        super().__init__(config, restore_step, rank, n_gpus, name)

    def _synthesis(self, models):
        """Write a latent transition space with linked reconstruction highlights."""
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

        source_indices = self._synthesis_source_indices(dataset_size, transition_count)
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

        # The Jina encoder is frozen and loaded outside the registered state
        # dict. Reuse the already-loaded training copy to avoid loading a second
        # 1.3 GB encoder when synthesis switches to moving-average models.
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
            f"Synthesis step {self.step}: encoding {transition_count} transitions "
            f"in batches of {batch_size}; {reconstruction_count} reconstruction highlights."
        )

        for batch_start in range(0, transition_count, batch_size):
            batch_end = min(batch_start + batch_size, transition_count)
            batch_source_indices = source_indices[batch_start:batch_end]
            source_samples = [
                self.dataset.get_sample(self.dataset.datas[index])
                for index in batch_source_indices
            ]
            batch = batch_to_cuda(self.dataset.collate_fn(source_samples), self.rank)
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

            source_state = squeeze_time_dim_state(batch["state"])
            target_state = squeeze_time_dim_state(batch["next_state"])

            for local_index, source_index in enumerate(batch_source_indices):
                vector_index = batch_start + local_index
                action_index = int(
                    batch["action_index"][local_index].detach().cpu().item()
                )
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
                        metrics = reconstruction_metrics(
                            prediction,
                            selected_target_state,
                            reconstruction_index,
                        )
                        prediction_views[prediction_key] = {
                            "encoder": prediction_info["encoder"],
                            "label": prediction_info["label"],
                            "condition": prediction_info["condition"],
                            "metrics": metrics,
                            "predicted_next_state": state_from_prediction(
                                prediction,
                                reconstruction_index,
                            ),
                        }
                    prior_metrics = prediction_views["prior"]["metrics"]
                    posterior_metrics = prediction_views["posterior"]["metrics"]
                    transition_records[vector_index]["reconstruction_score"] = prior_metrics[
                        "score"
                    ]
                    transition_records[vector_index]["reconstruction_scores"] = {
                        "prior": prior_metrics["score"],
                        "posterior": posterior_metrics["score"],
                    }
                    reconstruction_records.append(
                        {
                            "schema_version": 2,
                            "sample_id": sample_id,
                            "source_index": source_index,
                            "vector_index": vector_index,
                            "summary": {
                                "action": describe_action(action_index),
                                "score": prior_metrics["score"],
                                "prior_score": prior_metrics["score"],
                                "posterior_score": posterior_metrics["score"],
                            },
                            "input_state": state_from_target(
                                source_state,
                                local_index,
                            ),
                            "transition": {
                                "card_used": card_used,
                                "action": {
                                    "index": action_index,
                                    "label": describe_action(action_index),
                                },
                            },
                            "predictions": prediction_views,
                            "target_next_state": state_from_target(
                                target_state,
                                local_index,
                            ),
                        }
                    )

            if batch_end == transition_count or batch_end % (batch_size * 10) == 0:
                log.info(
                    f"Synthesis step {self.step}: encoded {batch_end}/{transition_count} transitions."
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
            f"Synthesis step {self.step}: wrote {reconstruction_path}, "
            f"{transition_path}, and {card_fusion_path}."
        )
        return transition_path

    @staticmethod
    def _synthesis_source_indices(dataset_size, item_count):
        """Select evenly-spaced current replay samples deterministically."""
        if item_count >= dataset_size:
            return list(range(dataset_size))
        if item_count == 1:
            return [0]
        return [round(index * (dataset_size - 1) / (item_count - 1)) for index in range(item_count)]

    def _write_card_fusion_space_artifact(
        self,
        step_dir,
        models,
        *,
        fallback_vectors,
        transition_records,
    ):
        """Encode every parsed card with the same CardFusion used at inference."""
        catalog_cards = self._load_card_fusion_catalog_cards()
        text_encoder = models.get("TextEncoder")
        if not catalog_cards or not hasattr(text_encoder, "_load_encoder"):
            if catalog_cards:
                log.warning(
                    "CardFusion catalog view needs a raw-text encoder; "
                    "using replay cards instead."
                )
            return write_card_fusion_space_artifact(
                step_dir,
                step=self.step,
                fused_vectors=fallback_vectors,
                records=transition_records,
            )

        observed_outcomes = self._card_fusion_observed_outcomes(transition_records)
        catalog_records = []
        for catalog_card in catalog_cards:
            change_counts = Counter()
            for description in catalog_card["description_keys"]:
                change_counts.update(observed_outcomes.get(description, {}))
            catalog_records.append(
                {
                    "card_used": catalog_card["card_used"],
                    "semantic_effects": catalog_card["semantic_effects"],
                    "state_change_counts": dict(change_counts),
                    "sample_count": sum(change_counts.values()),
                }
            )

        device = next(models["CardFusion"].parameters()).device
        batch_size = max(
            1,
            int(self.config.get("synthesis_card_fusion_batch_size", 64)),
        )
        vector_chunks = []
        with torch.no_grad():
            for batch_start in range(0, len(catalog_cards), batch_size):
                card_batch = catalog_cards[batch_start : batch_start + batch_size]
                h_text = text_encoder(
                    [card["card_used"]["description"] for card in card_batch],
                    device=device,
                )
                h_card_attr = models["CardStateEncoder"](
                    torch.as_tensor(
                        [card["model_attributes"]["card_type"] for card in card_batch],
                        dtype=torch.long,
                        device=device,
                    ),
                    torch.as_tensor(
                        [card["model_attributes"]["special_type"] for card in card_batch],
                        dtype=torch.float32,
                        device=device,
                    ),
                    torch.as_tensor(
                        [card["model_attributes"]["mana_cost"] for card in card_batch],
                        dtype=torch.float32,
                        device=device,
                    ),
                    torch.as_tensor(
                        [card["model_attributes"]["attack"] for card in card_batch],
                        dtype=torch.float32,
                        device=device,
                    ),
                    torch.as_tensor(
                        [card["model_attributes"]["health"] for card in card_batch],
                        dtype=torch.float32,
                        device=device,
                    ),
                    torch.as_tensor(
                        [card["model_attributes"]["has_state"] for card in card_batch],
                        dtype=torch.long,
                        device=device,
                    ),
                )
                vector_chunks.append(
                    models["CardFusion"](h_text, h_card_attr).detach().float().cpu()
                )

        return write_card_fusion_space_artifact(
            step_dir,
            step=self.step,
            fused_vectors=torch.cat(vector_chunks).numpy(),
            records=catalog_records,
            source_sample_count=len(transition_records),
        )

    def _load_card_fusion_catalog_cards(self):
        default_path = (
            Path(__file__).resolve().parents[2]
            / "data/retrieval/parsed_cards.jsonl"
        )
        cards_path = Path(
            self.config.get("synthesis_card_fusion_cards_path", default_path)
        )
        if not cards_path.is_file():
            log.warning(f"CardFusion catalog file was not found: {cards_path}")
            return []

        cards = []
        with cards_path.open("r", encoding="utf-8") as stream:
            for line in stream:
                if not line.strip():
                    continue
                try:
                    card = json.loads(line)
                except json.JSONDecodeError:
                    continue
                description = card.get("ability") or card.get("index_text") or card.get("name")
                if not description:
                    continue
                card_used, model_attributes = self._card_fusion_catalog_attributes(
                    card,
                    description,
                )
                description_keys = {
                    self._normalize_card_fusion_text(value)
                    for value in (card.get("ability"), card.get("index_text"), description)
                    if value
                }
                effects = sorted(
                    {
                        str(binding.get("effect"))
                        for binding in card.get("bindings", [])
                        if isinstance(binding, dict) and binding.get("effect")
                    }
                )
                cards.append(
                    {
                        "card_used": card_used,
                        "model_attributes": model_attributes,
                        "description_keys": description_keys,
                        "semantic_effects": effects,
                    }
                )
        return cards

    @staticmethod
    def _normalize_card_fusion_text(value):
        return " ".join(str(value).split()).casefold()

    @staticmethod
    def _card_fusion_catalog_attributes(card, description):
        type_name = str(card.get("type", "Unknown"))
        type_id = {
            "creature": 1,
            "instant": 2,
            "land": 3,
            "sorcery": 4,
        }.get(type_name.casefold(), 0)
        mana_cost = CVAETrainer._card_fusion_mana_cost(card.get("cost", ""))
        special_type = [0.0] * 20
        text = str(description).casefold()
        special_type[0] = float("enters the battlefield" in text)
        special_type[1] = float("leaves the battlefield" in text or "dies" in text)
        for index, keyword in enumerate(
            ("reach", "trample", "flying", "haste", "flash", "lifelink"),
            start=2,
        ):
            special_type[index] = float(bool(re.search(rf"\\b{keyword}\\b", text)))
        special_type[8] = 1.0
        special_type[9] = float(bool(re.search(r"\\binfect\\b", text)))
        special_type[10] = float(bool(re.search(r"\\bindestructible\\b", text)))
        attack = CVAETrainer._card_fusion_stat(card.get("power"))
        health = CVAETrainer._card_fusion_stat(card.get("toughness"))
        has_state = int(type_id == 1)
        return (
            {
                "card_id": card.get("card_id"),
                "name": card.get("name"),
                "description": str(description),
                "type": type_name,
                "mana_cost": [round(value * 20) for value in mana_cost],
                "attack": round(attack * 20),
                "health": round(health * 20),
                "has_state": bool(has_state),
                "special_types": [
                    name
                    for name, value in zip(
                        (
                            "ETB effect", "LTB effect", "Reach", "Trample", "Flying",
                            "Haste", "Flash", "Lifelink", "Can attack", "Infect",
                            "Indestructible",
                        ),
                        special_type,
                    )
                    if value
                ],
            },
            {
                "card_type": type_id,
                "special_type": special_type,
                "mana_cost": mana_cost,
                "attack": attack,
                "health": health,
                "has_state": has_state,
            },
        )

    @staticmethod
    def _card_fusion_mana_cost(cost):
        values = [0.0] * 6
        cost = str(cost or "")
        generic = "".join(re.findall(r"\d+", cost))
        values[0] = min(20, int(generic)) / 20 if generic else 0.0
        for index, color in enumerate(("U", "W", "B", "R", "G"), start=1):
            values[index] = min(20, cost.upper().count(color)) / 20
        return values

    @staticmethod
    def _card_fusion_stat(value):
        try:
            return max(0.0, min(20.0, float(value))) / 20
        except (TypeError, ValueError):
            return 0.0

    def _card_fusion_observed_outcomes(self, transition_records):
        outcomes = defaultdict(Counter)
        for record in transition_records:
            card = record.get("card_used", {})
            description = self._normalize_card_fusion_text(card.get("description", ""))
            if not description:
                continue
            change = str(
                record.get("state_delta", {}).get("change_type", "no_major_change")
            )
            outcomes[description][change] += 1
        return outcomes

    @staticmethod
    def _raw_card_used(data):
        state = data.get("state", {})
        if isinstance(state, (list, tuple)):
            state = state[-1] if state else {}
        return state.get("card_used", {}) if isinstance(state, dict) else {}

    @staticmethod
    def _synthesis_card_model_description(card_used, sample_index):
        """Keep the displayed text aligned with the text that reached CardFusion."""
        descriptions = card_used.get("description") if isinstance(card_used, dict) else None
        if isinstance(descriptions, (list, tuple)) and sample_index < len(descriptions):
            value = descriptions[sample_index]
            return value if isinstance(value, str) else None
        return None

    @staticmethod
    def _select_batch(value, indices):
        if isinstance(value, dict):
            return {
                key: CVAETrainer._select_batch(item, indices)
                for key, item in value.items()
            }
        if isinstance(value, torch.Tensor):
            return value.index_select(0, indices.to(value.device))
        return value

    @staticmethod
    def _synthesis_decoder_predictions(models, batch, selection):
        """Decode deterministic Prior and Posterior means for viewer comparison.

        The Prior view represents inference from the current state, card and
        action.  The Posterior view additionally observes the true next state,
        so it remains useful as the reconstruction upper bound.
        """
        decoder_inputs = {
            "state_tokens": batch["tokens_s"].index_select(0, selection),
            "state_padding_mask": batch["pad_s"].index_select(0, selection),
            "spans": batch["spans_s"],
        }
        decoder = models["TokenTransitionStateDecoder"]
        return {
            "prior": {
                "encoder": "PriorEncoder",
                "label": "Prior · inference",
                "condition": "current state + card + action",
                "prediction": decoder(
                    **decoder_inputs,
                    transition_vec=batch["mean_p"].index_select(0, selection),
                ),
            },
            "posterior": {
                "encoder": "PosteriorEncoder",
                "label": "Posterior · reconstruction",
                "condition": "current state + card + action + true next state",
                "prediction": decoder(
                    **decoder_inputs,
                    transition_vec=batch["mean_q"].index_select(0, selection),
                ),
            },
        }

    def _forward(self, batch, models, isTrain, step, epoch):

        batch=self.encode(batch,models,isTrain,step,epoch)
        batch=self.decode(batch,models,isTrain,step,epoch)
        total_loss=0

        loss={}


        

        if self.config.get("w_kl_loss",1.0)>0:
            loss["kl_loss"]=self.prior_posterior_kl_loss(batch)
            total_loss=total_loss+loss["kl_loss"]*self.config.get("w_kl_loss",1.0)
        if self.config.get("w_reconstruction_loss",1.0)>0:
            loss_reconstruction=self.reconstruction_loss(batch)
            loss["reconstruction_loss"]=loss_reconstruction["total_loss"]
            for key in loss_reconstruction:
                if key not in ["total_loss"]:
                    loss[f"reconstruction_{key}"]=loss_reconstruction[key]
            total_loss=total_loss+loss["reconstruction_loss"]*self.config.get("w_reconstruction_loss",1.0)

        loss["total_loss"]=total_loss
        return loss

    def encode(self, batch, models, isTrain, step, epoch):
        # 1) state embedding
        h_s, tokens_s, pad_s, spans_s = models["StateTransformerEncoder"](batch["state"])
        h_s_next, tokens_s_next, pad_s_next, spans_s_next = models["StateTransformerEncoder"](
            batch["next_state"]
        )
        # 2) action
        h_action = models["ActionEncoder"](batch["action_index"])
        # 3) card_used
        cu = batch["card_used"]
        if "attention_mask" in cu:
            h_text = models["TextEncoder"](
                cu["description"],
                src_key_padding_mask=~cu["attention_mask"].bool(),
            )
        else:
            h_text = models["TextEncoder"](
                cu["description"],
                device=h_s.device,
            )
        h_card_attr = models["CardStateEncoder"](
            cu["card_type"].long(),
            cu["special_type"],
            cu["mana_cost"],
            cu["attack"],
            cu["defend"],
            cu["has_state"].long(),
        )
        # 按你的设计把 text / attr 合成 h_card，维度 = d_model
        h_card = models["CardFusion"](h_text, h_card_attr)  # 或 Linear(cat(...))
        # 4) CVAE prior / posterior
        mean_p, std_p = models["PriorEncoder"](h_card, h_action, h_s)
        mean_q, std_q = models["PosteriorEncoder"](h_card, h_action, h_s, h_s_next)
        if isTrain:
            z = mean_q + std_q * torch.randn_like(mean_q)
        else:
            z = mean_p + std_p * torch.randn_like(mean_p)
        batch.update({
            "h_s": h_s, "h_s_next": h_s_next,
            "tokens_s": tokens_s, "tokens_s_next": tokens_s_next, 
            "pad_s": pad_s, "pad_s_next": pad_s_next, 
            "spans_s": spans_s, "spans_s_next": spans_s_next,
            "h_action": h_action, "h_card": h_card,
            "mean_p": mean_p, "std_p": std_p,
            "mean_q": mean_q, "std_q": std_q,
            "z": z,
        })
        return batch
        
    def decode(self, batch, models, isTrain, step, epoch):
        transition_vec =batch["z"]
        pred_next = models["TokenTransitionStateDecoder"](
            state_tokens=batch["tokens_s"],
            state_padding_mask=batch["pad_s"],
            spans=batch["spans_s"],
            transition_vec=transition_vec,
        )
        batch["pred_next"]=pred_next
        return batch


    def prior_posterior_kl_loss(self, batch):
        """Return the standard CVAE divergence KL(q(z|...) || p(z|...))."""
        mean_p = batch["mean_p"]
        std_p = batch["std_p"].clamp_min(1e-6)

        mean_q = batch["mean_q"]
        std_q = batch["std_q"].clamp_min(1e-6)

        # q is the posterior that observes s_next; p is the inference-time prior.
        kl_loss = (
            torch.log(std_p / std_q)
            + (std_q.pow(2) + (mean_q - mean_p).pow(2))
            / (2 * std_p.pow(2))
            - 0.5
        )

        return kl_loss.sum(dim=-1).mean()


    def reconstruction_loss(self, batch):
        pred = batch["pred_next"]
        target = squeeze_time_dim_state(batch["next_state"])
        source = squeeze_time_dim_state(batch["state"])
        stat_loss_options = _stat_loss_options(self.config)

        result = {}
        result["total_loss"] = pred["global_state"].new_zeros(())

        # 生命值和五种法力均按离散值训练。
        global_valid = torch.ones_like(target["global_state"], dtype=torch.bool)
        result["global_state_loss"] = masked_stat_class_loss(
            pred["global_state"],
            target["global_state"],
            source["global_state"],
            global_valid,
            global_valid,
            **stat_loss_options,
        )
        result["total_loss"] += result["global_state_loss"] * self.config.get(
            "w_global_state_loss",
            1.0,
        )

        for zone_name in ["hand", "library", "graveyard", "stack_cards"]:
            loss_name = f"card_zone_loss_{zone_name}"
            result[loss_name] = zone_reconstruction_loss(
                pred["card_zones"][zone_name],
                target["card_zones"][zone_name],
                source["card_zones"][zone_name],
                stat_loss_options,
                include_card_metadata=True,
            )
            result["total_loss"] += result[loss_name] * self.config.get(
                f"w_card_zone_loss_{zone_name}",
                1.0,
            )

        for zone_name in ["self_board", "oppo_board"]:
            loss_name = f"board_zone_loss_{zone_name}"
            result[loss_name] = zone_reconstruction_loss(
                pred["board_zones"][zone_name],
                target["board_zones"][zone_name],
                source["board_zones"][zone_name],
                stat_loss_options,
                include_card_metadata=False,
            )
            result["total_loss"] += result[loss_name] * self.config.get(
                f"w_board_zone_loss_{zone_name}",
                1.0,
            )

        return result

    
    
    
