from game.rlearning.module.state_space.EntityTransitionPlanBirthZeroMessage import EntityTransitionPlanBirthZeroMessageCVAETrainer
from game.rlearning.module.state_space.EntityTransitionSupportPlanBirth import EntityTransitionSupportPlanBirthZeroMessageCVAETrainer,apply_existing_transition_mask
from game.rlearning.net.state_space.EntityTransition import squeeze_entity_time_dim


class EntityTransitionSupportPlanBirthRawReconstructionCVAETrainer(EntityTransitionSupportPlanBirthZeroMessageCVAETrainer):
    
    def decode(self, batch, models, isTrain, step, epoch):
        batch = EntityTransitionPlanBirthZeroMessageCVAETrainer.decode(
            self, batch, models, isTrain, step, epoch
        )

        if isTrain:
            return batch

        selected_mask = batch["predicted_selected_mask"]
        source = squeeze_entity_time_dim(batch["state"])
        batch["pred_next"] = apply_existing_transition_mask(
            batch["pred_next"], source, selected_mask
        )
        batch["effective_selected_mask"] = selected_mask
        return batch