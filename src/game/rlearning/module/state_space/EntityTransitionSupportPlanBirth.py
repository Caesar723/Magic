import torch
import torch.nn.functional as F

from game.rlearning.module.state_space.EntityTransitionPlanBirthZeroMessage import EntityTransitionPlanBirthZeroMessageCVAETrainer
from game.rlearning.net.state_space.EntityTransition import squeeze_entity_time_dim
from game.rlearning.net.state_space.LatentEntitySelector import build_existing_change_targets, strict_topk_mask
from game.rlearning.states.state_space.specific_entity import CARD_ZONE_NAMES, BOARD_ZONE_NAMES,LOCATION_NAMES
from game.rlearning.synthesis.entity_transition import align_entity_transitions


def extract_entity_tokens(state_tokens,state_padding_mask,spans):
    zone_names=(*CARD_ZONE_NAMES,*BOARD_ZONE_NAMES)

    entity_tokens = []
    entity_padding_masks = []

    for zone_name in zone_names:
        start, end = spans[zone_name]

        entity_tokens.append(state_tokens[:,start:end])
        entity_padding_masks.append(state_padding_mask[:,start:end])

    entity_tokens = torch.cat(entity_tokens,dim=1)
    entity_padding_masks = torch.cat(entity_padding_masks,dim=1)
    return entity_tokens, entity_padding_masks

def _binary_identity(source_value, like):
    return torch.where(source_value.bool(), torch.full_like(like, 20.0), torch.full_like(like, -20.0))


def _class_identity(source_value, like):
    class_count = like.shape[-1]
    index = (source_value.float() * (class_count - 1)).round().long()
    identity = torch.full_like(like, -20.0)
    return identity.scatter(-1, index.clamp(0, class_count - 1).unsqueeze(-1), 20.0)


def apply_existing_transition_mask(prediction, source, selected_mask):
    cursor = 0
    

    for group_name, zone_names in (("card_zones", CARD_ZONE_NAMES), ("board_zones", BOARD_ZONE_NAMES)):
        for zone_name in zone_names:
            pred = prediction[group_name][zone_name]
            src = source[group_name][zone_name]
            count = pred["destination_zone"].shape[1]

            selected = selected_mask[:, cursor:cursor + count] & src["card_mask"].bool()
            cursor += count

            zone_identity = torch.full_like(pred["destination_zone"], -20.0)
            zone_identity[..., LOCATION_NAMES.index(zone_name)] = 20.0
            pred["destination_zone"] = torch.where(selected.unsqueeze(-1), pred["destination_zone"], zone_identity)

            for field in ("card_special_types",):
                pred[field] = torch.where(
                    selected.unsqueeze(-1), pred[field],
                    _binary_identity(src[field], pred[field]),
                )

            for field in ("card_atks", "card_hps"):
                pred[field] = torch.where(
                    selected.unsqueeze(-1), pred[field],
                    _class_identity(src[field], pred[field]),
                )

            for field in ("card_has_state", "card_tapped"):
                pred[field] = torch.where(
                    selected, pred[field],
                    _binary_identity(src[field], pred[field]),
                )
    return prediction

    
class EntityTransitionSupportPlanBirthZeroMessageCVAETrainer(EntityTransitionPlanBirthZeroMessageCVAETrainer):
    
    def encode(self,batch,models,isTrain,step,epoch):
        
        # 1) state embedding
        h_s, tokens_s, pad_s, spans_s = models["StateTransformerEncoder"](batch["state"])

        # 2) action
        h_action = models["ActionEncoder"](batch["card_action_index"])
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
            cu["color_identity"],
        )

        h_card = models["CardFusion"](h_text, h_card_attr)

        ##########################################################
        # 4) Entity Transition Support
        ##########################################################

        transition_plan = models["TransitionPlanner"](h_card,h_action,h_s,tokens_s,pad_s)

        entity_tokens, entity_padding_masks = extract_entity_tokens(tokens_s, pad_s, spans_s)

        source_state = squeeze_entity_time_dim(batch["state"])
        next_state = squeeze_entity_time_dim(batch["next_state"])

        entity_alignment = align_entity_transitions(source_state, next_state)
        changed_mask,existing_count,birth_count = build_existing_change_targets(source_state,next_state,entity_alignment)
         
        mean_p, std_p = models["PriorEncoder"](h_card,h_action,h_s)

        mean_q, std_q = models["TransitionSupportPosteriorEncoder"](h_card,h_action,h_s,entity_tokens,changed_mask,entity_padding_masks,birth_count)

        if isTrain:
            z = mean_q + std_q * torch.randn_like(mean_q)
        else:
            z = mean_p + std_p * torch.randn_like(mean_p)

        existing_count_logits = models["ExistingTransitionCountHead"](transition_plan, z)
        birth_count_logits = models["BirthCountHead"](transition_plan, z)
        selection_logits = models["LatentEntitySelector"](entity_tokens, transition_plan, z, entity_padding_masks)


        predicted_existing_count=existing_count_logits.argmax(dim=-1)

        predicted_selected_mask = strict_topk_mask(selection_logits,predicted_existing_count,entity_padding_masks)


        

        batch.update({
            "h_s": h_s,
            "tokens_s": tokens_s,
            "pad_s": pad_s,
            "spans_s": spans_s,

            "h_action": h_action,
            "h_card": h_card,

            "entity_tokens": entity_tokens,
            "entity_padding_mask": entity_padding_masks,

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

            "transition_plan": transition_plan,
        })
        return batch

    def decode(self, batch, models, isTrain, step, epoch):
        batch = super().decode(batch, models, isTrain, step, epoch)

        selected_mask = batch["changed_mask"] if isTrain else batch["predicted_selected_mask"]

        source = squeeze_entity_time_dim(batch["state"])
        batch["pred_next"] = apply_existing_transition_mask(batch["pred_next"],source,selected_mask)
        batch["effective_selected_mask"] = selected_mask
        return batch

    def reconstruction_loss(self, batch):
        result = super().reconstruction_loss(batch)

        selection_logits = batch["selection_logits"]
        changed_mask = batch["changed_mask"]
        padding_mask = batch["entity_padding_mask"]

        existing_count_logits = batch["existing_count_logits"]
        birth_count_logits = batch["birth_count_logits"]

        ##########################
        # Entity selection loss
        ##########################
        positive_weight = float(self.config.get("selection_positive_weight",1.0))
        valid_mask = ~padding_mask
        if valid_mask.any():
            valid_logits = selection_logits[valid_mask]
            valid_targets = changed_mask[valid_mask].float()
            selection_loss = F.binary_cross_entropy_with_logits(
                valid_logits,
                valid_targets,
                pos_weight=valid_logits.new_tensor(
                    positive_weight
                ),
            )
            selection_loss = selection_loss.mean()
        else:
            selection_loss = selection_logits.new_zeros(())

        result["selection_loss"] = selection_loss
        if self.config.get("w_selection_loss",1.0)>0:
            result["total_loss"] = result["total_loss"] + selection_loss*self.config.get("w_selection_loss",1.0)
        
        ##########################
        # count loss
        ##########################
        max_existing_count=existing_count_logits.shape[-1] - 1
        max_birth_count=birth_count_logits.shape[-1] - 1

        existing_count_targets = batch["existing_count"].clamp(0,max_existing_count)
        birth_count_targets = batch["birth_count"].clamp(0,max_birth_count)

        existing_count_loss = F.cross_entropy(existing_count_logits,existing_count_targets)
        birth_count_loss = F.cross_entropy(birth_count_logits,birth_count_targets)

        result["existing_count_loss"] = existing_count_loss
        result["birth_count_loss"] = birth_count_loss

        if self.config.get("w_existing_count_loss",1.0)>0:
            result["total_loss"] = result["total_loss"] + existing_count_loss*self.config.get("w_existing_count_loss",1.0)
        if self.config.get("w_birth_count_loss",1.0)>0:
            result["total_loss"] = result["total_loss"] + birth_count_loss*self.config.get("w_birth_count_loss",1.0)

        return result



    def _synthesis_decoder_predictions(self, models, batch, selection):
        plans = batch["transition_plan"].index_select(0, selection)
        entity_tokens = batch["entity_tokens"].index_select(0, selection)
        entity_padding = batch["entity_padding_mask"].index_select(0, selection)
        source = self._select_batch(
            squeeze_entity_time_dim(batch["state"]),
            selection,
        )

        decoder_inputs = {
            "state_tokens": batch["tokens_s"].index_select(0, selection),
            "state_padding_mask": batch["pad_s"].index_select(0, selection),
            "spans": batch["spans_s"],
            "transition_plan": plans,
        }

        def decode_view(z):
            count_logits = models["ExistingTransitionCountHead"](plans, z)
            counts = count_logits.argmax(dim=-1)

            selection_logits = models["LatentEntitySelector"](
                entity_tokens,
                plans,
                z,
                entity_padding,
            )
            selected_mask = strict_topk_mask(
                selection_logits,
                counts,
                entity_padding,
            )

            prediction = models["TokenTransitionStateDecoder"](
                **decoder_inputs,
                transition_vec=z,
            )
            prediction = apply_existing_transition_mask(
                prediction,
                source,
                selected_mask,
            )
            return prediction, selected_mask

        prior_prediction, prior_mask = decode_view(
            batch["mean_p"].index_select(0, selection)
        )
        posterior_prediction, posterior_mask = decode_view(
            batch["mean_q"].index_select(0, selection)
        )

        return {
            "prior": {
                "encoder": "PriorEncoder",
                "label": "Prior · inference",
                "condition": "current state + card + action",
                "prediction": prior_prediction,
                "selected_mask": prior_mask,
            },
            "posterior": {
                "encoder": "PosteriorEncoder",
                "label": "Posterior · reconstruction",
                "condition": "current state + card + action + true next state",
                "prediction": posterior_prediction,
                "selected_mask": posterior_mask,
            },
        }
