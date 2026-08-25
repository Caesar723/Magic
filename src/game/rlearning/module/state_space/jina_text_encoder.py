

import copy
import json
from pathlib import Path
from typing import Optional

import torch
import torch.nn.functional as F

from game.rlearning.utils.baseAgent import ModelTrainer
from game.rlearning.net.state_space.jina_text_encoder import (
    JinaTextEncoder as JinaTextEncoderModel,
)
from game.rlearning.synthesis.artifacts import write_text_embedding_space_artifact
from game.rlearning.synthesis.projection import pca_project_2d
import game.rlearning.utils.log as log




def continuous_pairwise_ranking_loss(
    scores: torch.Tensor,
    relevance: torch.Tensor,
    temperature: float = 0.1,
    min_relevance_gap: float = 1e-6,
    gap_power: float = 1.0,
) -> torch.Tensor:
    """Rank higher-relevance candidates above lower-relevance candidates.

    ``scores`` and ``relevance`` have shape ``[batch_size, candidate_count]``.
    Each candidate pair contributes ``softplus(-signed_score_gap / temperature)``.
    Pairs with equal relevance are ignored, while pairs with a larger relevance
    gap receive a larger weight.
    """
    temperature = float(temperature)
    min_relevance_gap = float(min_relevance_gap)
    gap_power = float(gap_power)

    relevance = relevance.to(device=scores.device, dtype=scores.dtype)
    score_gap = scores.unsqueeze(-1) - scores.unsqueeze(-2)
    relevance_gap = relevance.unsqueeze(-1) - relevance.unsqueeze(-2)

    absolute_gap = relevance_gap.abs()
    upper_triangle = torch.triu(
        torch.ones_like(absolute_gap, dtype=torch.bool),
        diagonal=1,
    )
    valid_pairs = upper_triangle & (absolute_gap > min_relevance_gap)

    signed_score_gap = relevance_gap.sign() * score_gap
    safe_temperature = max(float(temperature), torch.finfo(scores.dtype).eps)
    pair_loss = F.softplus(-signed_score_gap / safe_temperature)
    pair_weight = absolute_gap.pow(gap_power) * valid_pairs

    return (pair_loss * pair_weight).sum() / pair_weight.sum().clamp_min(
        torch.finfo(scores.dtype).eps
    )


def continuous_listwise_ranking_loss(
    scores: torch.Tensor,
    relevance: torch.Tensor,
    temperature: float = 0.1,
    gain_base: float = 2.0,
) -> Optional[torch.Tensor]:
    """Match one query's score distribution to its graded relevance labels.

    ``scores`` and ``relevance`` have shape ``[batch_size, candidate_count]``.
    Relevance is converted to non-negative graded gains using
    ``gain_base ** relevance - 1`` and normalized within each query.  This
    supports multiple equally relevant candidates without forcing an arbitrary
    order between them.  ``None`` is returned when a group has no positive
    relevance signal.
    """
    relevance = relevance.to(device=scores.device, dtype=scores.dtype)
    safe_temperature = max(float(temperature), torch.finfo(scores.dtype).eps)
    safe_gain_base = max(float(gain_base), 1.0 + torch.finfo(scores.dtype).eps)

    gain_base_tensor = torch.as_tensor(
        safe_gain_base,
        device=scores.device,
        dtype=scores.dtype,
    )
    gains = torch.pow(gain_base_tensor, relevance) - 1
    gains = gains.clamp_min(0)
    gain_sum = gains.sum(dim=-1, keepdim=True)
    valid_rows = gain_sum.squeeze(-1) > torch.finfo(scores.dtype).eps
    if not valid_rows.any():
        return None

    target_distribution = gains[valid_rows] / gain_sum[valid_rows]
    log_score_distribution = F.log_softmax(
        scores[valid_rows] / safe_temperature,
        dim=-1,
    )
    return -(target_distribution * log_score_distribution).sum(dim=-1).mean()


def embedding_anchor_loss(
    embeddings: torch.Tensor,
    reference_embeddings: torch.Tensor,
) -> torch.Tensor:
    """Keep fine-tuned embeddings close to frozen reference embeddings."""
    reference_embeddings = reference_embeddings.detach().to(
        device=embeddings.device,
        dtype=embeddings.dtype,
    )
    return 1 - F.cosine_similarity(
        embeddings,
        reference_embeddings,
        dim=-1,
    ).mean()



class JinaTextEncoder(ModelTrainer):

    def __init__(self, config, restore_step, rank=0, n_gpus=1, name="main"):
        super().__init__(config, restore_step, rank, n_gpus)

    def _init_extra(self):
        """Optionally keep a frozen base encoder for embedding distillation."""
        super()._init_extra()
        self.anchor_teacher = None
        if float(self.config.get("w_anchor_loss", 0)) <= 0:
            return

        # Keep ``trainable=True`` so the teacher follows the same differentiable
        # encoding path and pooling rule as the student.  Its parameters are
        # then frozen and its forward pass is always protected by ``no_grad``.
        teacher_config = copy.deepcopy(self.config["model"]["TextEncoder"])
        teacher_config["trainable"] = True
        self.anchor_teacher = JinaTextEncoderModel(teacher_config)
        self.anchor_teacher.eval()
        self.anchor_teacher.requires_grad_(False)
        log.info("Enabled frozen base TextEncoder teacher for anchor loss.")

    def _forward(self, batch, models, isTrain, step, epoch):

        loss = {"total_loss":0}
        relevance = batch["relevance"].float()
        candidate_offsets = batch["candidate_offsets"].tolist()

        query_embeddings = models["TextEncoder"](
            batch["query"],
            device=relevance.device,
            prompt_name="query",
        )
        candidate_embeddings = models["TextEncoder"](
            batch["candidate"],
            device=relevance.device,
            prompt_name="document",
        )

        if self.config.get("w_ranking_loss", 1)>0:
            ranking_losses = []
            for query_embedding, start, end in zip(
                query_embeddings,
                candidate_offsets[:-1],
                candidate_offsets[1:],
            ):
                scores = F.cosine_similarity(
                    query_embedding.unsqueeze(0),
                    candidate_embeddings[start:end],
                    dim=-1,
                )
                ranking_losses.append(
                    continuous_pairwise_ranking_loss(
                        scores.unsqueeze(0),
                        relevance[start:end].unsqueeze(0),
                        temperature=self.config.get("ranking_temperature", 0.1),
                        min_relevance_gap=self.config.get("min_relevance_gap", 1e-6),
                        gap_power=self.config.get("relevance_gap_power", 1.0),
                    )
                )

            ranking_loss = torch.stack(ranking_losses).mean()
            loss["ranking_loss"] = ranking_loss
            loss["total_loss"] += ranking_loss*self.config.get("w_ranking_loss", 1)
        if self.config.get("w_listwise_loss", 1)>0:
            listwise_losses = []
            for query_embedding, start, end in zip(
                query_embeddings,
                candidate_offsets[:-1],
                candidate_offsets[1:],
            ):
                if end <= start:
                    continue

                scores = F.cosine_similarity(
                    query_embedding.unsqueeze(0),
                    candidate_embeddings[start:end],
                    dim=-1,
                )
                listwise_loss = continuous_listwise_ranking_loss(
                    scores.unsqueeze(0),
                    relevance[start:end].unsqueeze(0),
                    temperature=self.config.get("listwise_temperature", 0.1),
                    gain_base=self.config.get("listwise_gain_base", 2.0),
                )
                if listwise_loss is not None:
                    listwise_losses.append(listwise_loss)

            if listwise_losses:
                listwise_loss = torch.stack(listwise_losses).mean()
                loss["listwise_loss"] = listwise_loss
                loss["total_loss"] += listwise_loss * self.config.get(
                    "w_listwise_loss", 1
                )

        if self.anchor_teacher is not None:
            with torch.no_grad():
                reference_query_embeddings = self.anchor_teacher(
                    batch["query"],
                    device=query_embeddings.device,
                    prompt_name="query",
                )
                reference_candidate_embeddings = self.anchor_teacher(
                    batch["candidate"],
                    device=candidate_embeddings.device,
                    prompt_name="document",
                )

            anchor_loss = 0.5 * (
                embedding_anchor_loss(query_embeddings, reference_query_embeddings)
                + embedding_anchor_loss(
                    candidate_embeddings,
                    reference_candidate_embeddings,
                )
            )
            loss["anchor_loss"] = anchor_loss
            loss["total_loss"] += anchor_loss * self.config.get(
                "w_anchor_loss", 0
            )

        return loss

    def synthesis(self):
        """Project synthesis queries together with every parsed card embedding."""
        self._moving_average()
        models = self.models_test
        for model in models.values():
            model.eval()

        dataset = self.dataset_class(self.config, "synthesis")
        total = min(len(dataset), int(self.config.get("synthesis_items", 10)))
        if total <= 0:
            return None

        cards = self._load_synthesis_cards()
        if not cards:
            log.warning("Text synthesis skipped because no parsed cards were found.")
            return None

        query_batch_size = max(
            1,
            int(
                self.config.get(
                    "synthesis_text_batch_size",
                    self.config.get("dataloader", {}).get("batch_size", 1),
                )
            ),
        )
        card_batch_size = max(
            1,
            int(self.config.get("synthesis_card_batch_size", 64)),
        )
        source_metadata = dataset.fixed_synthesis_metadata
        if source_metadata is None:
            source_metadata = dataset.metadata[:total]

        query_embeddings = []
        query_records = []
        log.info(
            f"Synthesis step {self.step}: encoding {total} queries and "
            f"{len(cards)} parsed cards."
        )

        with torch.no_grad():
            for batch_start in range(0, total, query_batch_size):
                batch_metadata = source_metadata[batch_start : batch_start + query_batch_size]
                source_samples = [dataset.get_sample(metadata) for metadata in batch_metadata]
                batch_queries = [sample["query"] for sample in source_samples]
                values = models["TextEncoder"](
                    batch_queries,
                    prompt_name="query",
                ).detach().float().cpu()
                query_embeddings.append(values)

                for local_index, metadata in enumerate(batch_metadata):
                    source_index = batch_start + local_index
                    query_records.append(
                        {
                            "kind": "query",
                            "query_index": source_index,
                            "source_index": source_index,
                            "sample_id": metadata["index"],
                            "dataset": metadata.get("name", "dataset"),
                            "binding_label": self._binding_label(
                                source_samples[local_index]["query_bindings"]
                            ),
                            "text": batch_queries[local_index],
                        }
                    )

            card_embeddings = []
            for batch_start in range(0, len(cards), card_batch_size):
                card_batch = cards[batch_start : batch_start + card_batch_size]
                values = models["TextEncoder"](
                    [card["synthesis_text"] for card in card_batch],
                    prompt_name="document",
                ).detach().float().cpu()
                card_embeddings.append(values)

        query_values = torch.cat(query_embeddings)
        card_values = torch.cat(card_embeddings)
        records = []
        for vector_index, record in enumerate(query_records):
            records.append({"vector_index": vector_index, **record})
        for card_index, card in enumerate(cards):
            records.append(
                {
                    "vector_index": len(query_records) + card_index,
                    "kind": "card",
                    "card_id": card.get("card_id"),
                    "name": card.get("name", card.get("card_id", "Unnamed card")),
                    "type": card.get("type", card.get("kind", "Unknown")),
                    "cost": card.get("cost"),
                    "binding_label": self._binding_label(card.get("bindings", [])),
                    "bindings": card.get("bindings", []),
                    "text": card["synthesis_text"],
                }
            )

        embeddings = torch.cat([query_values, card_values]).numpy()
        coordinates, projection = pca_project_2d(embeddings)
        projection["source"] = "text_embeddings"
        step_dir = f"{self.logdir}/synthesis/{self.step}"
        artifact_path = write_text_embedding_space_artifact(
            step_dir,
            step=self.step,
            embeddings=embeddings,
            records=records,
            coordinates=coordinates,
            projection=projection,
        )
        log.info(f"Synthesis step {self.step}: wrote {artifact_path}.")
        return artifact_path

    def _load_synthesis_cards(self):
        default_path = Path(__file__).resolve().parents[2] / "data/retrieval/parsed_cards.jsonl"
        cards_path = Path(self.config.get("synthesis_cards_path", default_path))
        if not cards_path.is_file():
            log.warning(f"Parsed-card file was not found: {cards_path}")
            return []

        cards = []
        with cards_path.open("r", encoding="utf-8") as file:
            for line in file:
                if not line.strip():
                    continue
                card = json.loads(line)
                text = card.get("ability") or card.get("index_text") or card.get("name")
                if text:
                    card["synthesis_text"] = text
                    cards.append(card)
        return cards

    @staticmethod
    def _binding_label(bindings):
        effects = []
        for binding in bindings:
            effect = binding.get("effect", "UNSPECIFIED")
            if effect not in effects:
                effects.append(effect)
        return " + ".join(effects) if effects else "UNSPECIFIED"
