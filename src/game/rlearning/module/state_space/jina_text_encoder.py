

import torch
import torch.nn.functional as F




from game.rlearning.utils.baseAgent import ModelTrainer




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



class JinaTextEncoder(ModelTrainer):




    def __init__(self, config, restore_step, rank=0, n_gpus=1, name="main"):
        super().__init__(config, restore_step, rank, n_gpus)

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

        return loss

    @torch.no_grad()
    def synthesis(self):
        # This trainer has no generated artifact to save.  The base synthesis
        # routine expects an ``index`` field that the text-matching dataset
        # intentionally does not return.
        return None
