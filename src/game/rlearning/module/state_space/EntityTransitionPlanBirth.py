"""Birth-slot trainer with an explicit deterministic transition-plan path."""

import torch

from game.rlearning.module.state_space.EntityTransitionBirth import EntityTransitionBirthCVAETrainer
from game.rlearning.synthesis.transition_plan import write_transition_plan_artifact
from game.rlearning.utils.data import batch_to_cuda


class EntityTransitionPlanBirthCVAETrainer(EntityTransitionBirthCVAETrainer):
    """Keep v03 losses while adding direct planner memory to the decoder."""
    def encode(self, batch, models, isTrain, step, epoch):
        """Reuse v03 encoders, then attach a deterministic four-token plan."""
        batch = super().encode(batch, models, isTrain, step, epoch)
        batch["transition_plan"] = models["TransitionPlanner"](
            batch["h_card"], batch["h_action"], batch["h_s"], batch["tokens_s"], batch["pad_s"]
        )
        return batch

    def decode(self, batch, models, isTrain, step, epoch):
        """Decode next state from current state, direct plan memory and z memory."""
        batch["pred_next"] = models["TokenTransitionStateDecoder"](
            state_tokens=batch["tokens_s"], state_padding_mask=batch["pad_s"], spans=batch["spans_s"],
            transition_vec=batch["z"], transition_plan=batch["transition_plan"]
        )
        return batch

    @staticmethod
    def _synthesis_decoder_predictions(models, batch, selection):
        """Compare deterministic prior and posterior plans with the same direct plan memory."""
        inputs = {"state_tokens": batch["tokens_s"].index_select(0, selection), "state_padding_mask": batch["pad_s"].index_select(0, selection), "spans": batch["spans_s"], "transition_plan": batch["transition_plan"].index_select(0, selection)}
        decoder = models["TokenTransitionStateDecoder"]
        return {
            "prior": {"encoder": "PriorEncoder", "label": "Prior · inference", "condition": "current state + card + action", "prediction": decoder(**inputs, transition_vec=batch["mean_p"].index_select(0, selection))},
            "posterior": {"encoder": "PosteriorEncoder", "label": "Posterior · reconstruction", "condition": "current state + card + action + true next state", "prediction": decoder(**inputs, transition_vec=batch["mean_q"].index_select(0, selection))},
        }

    @torch.no_grad()
    def _synthesis(self, models):
        """Write inherited artifacts first, then append deterministic plan vectors."""
        result = super()._synthesis(models)
        count = min(int(self.config.get("synthesis_transition_items", 1000)), len(self.dataset.datas))
        if count <= 0:
            return result
        model_copy = dict(models)
        if "TextEncoder" in self.models:
            model_copy["TextEncoder"] = self.models["TextEncoder"]
        batch_size = max(1, int(self.config.get("synthesis_transition_batch_size", 32)))
        indices = self._synthesis_source_indices(len(self.dataset.datas), count)
        plans = []
        for start in range(0, count, batch_size):
            samples = [self.dataset.get_sample(self.dataset.datas[index]) for index in indices[start:start + batch_size]]
            batch = batch_to_cuda(self.dataset.collate_fn(samples), self.rank)
            plans.append(self.encode(batch, model_copy, True, self.step, self.epoch)["transition_plan"].float().cpu())
        write_transition_plan_artifact(f"{self.logdir}/synthesis/{self.step}", self.step, torch.cat(plans).numpy())
        return result
