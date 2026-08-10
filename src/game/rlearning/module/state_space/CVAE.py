
import torch
import torch.nn.functional as F


from game.rlearning.utils.baseAgent import BaseTrainer
from game.rlearning.net.state_space.StateEncoder import squeeze_time_dim_state

def masked_mse(pred_value, target_value, valid_mask):
    loss = (pred_value - target_value.float()).pow(2)

    valid_mask = valid_mask.float()

    while valid_mask.ndim < loss.ndim:
        valid_mask = valid_mask.unsqueeze(-1)

    valid_mask = valid_mask.expand_as(loss)
    denom = valid_mask.sum().clamp_min(1.0)

    return (loss * valid_mask).sum() / denom
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

def card_zone_loss(pred_zone, target_zone):
    zone_loss = pred_zone["card_mask"].new_zeros(())

    # 所有 slot 都训练“这里是否有卡”
    target_mask = target_zone["card_mask"].float()
    zone_loss = zone_loss + F.binary_cross_entropy_with_logits(
        pred_zone["card_mask"],
        target_mask,
    )

    # 卡实际存在时，才训练其属性
    valid_mask = target_mask > 0.5

    if valid_mask.any():
        zone_loss = zone_loss + F.cross_entropy(
            pred_zone["card_types"][valid_mask],
            target_zone["card_types"][valid_mask].long(),
        )

        zone_loss = zone_loss + masked_mse(
            pred_zone["card_costs"],
            target_zone["card_costs"],
            valid_mask,
        )

        zone_loss = zone_loss + masked_bce(
            pred_zone["card_special_types"],
            target_zone["card_special_types"],
            valid_mask,
        )

        zone_loss = zone_loss + masked_mse(
            pred_zone["card_atks"],
            target_zone["card_atks"],
            valid_mask,
        )

        zone_loss = zone_loss + masked_mse(
            pred_zone["card_hps"],
            target_zone["card_hps"],
            valid_mask,
        )

        zone_loss = zone_loss + masked_bce(
            pred_zone["card_has_state"],
            target_zone["card_has_state"],
            valid_mask,
        )

    return zone_loss

def board_zone_loss(pred_zone, target_zone):
    zone_loss = pred_zone["card_mask"].new_zeros(())

    target_mask = target_zone["card_mask"].float()
    zone_loss = zone_loss + F.binary_cross_entropy_with_logits(
        pred_zone["card_mask"],
        target_mask,
    )

    valid_mask = target_mask > 0.5

    if valid_mask.any():
        zone_loss = zone_loss + masked_bce(
            pred_zone["card_special_types"],
            target_zone["card_special_types"],
            valid_mask,
        )

        zone_loss = zone_loss + masked_mse(
            pred_zone["card_atks"],
            target_zone["card_atks"],
            valid_mask,
        )

        zone_loss = zone_loss + masked_mse(
            pred_zone["card_hps"],
            target_zone["card_hps"],
            valid_mask,
        )

        zone_loss = zone_loss + masked_bce(
            pred_zone["card_has_state"],
            target_zone["card_has_state"],
            valid_mask,
        )

    return zone_loss
class CVAETrainer(BaseTrainer):
    def __init__(self, config,restore_step, rank=0, n_gpus=1,name="main"):
        super().__init__(config,restore_step, rank, n_gpus,name)

    def _synthesis(self, models):
        """CVAE synthesis hook; generation and output handling are added later."""
        return None

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
        mean_p, std_p = models["PriorityEncoder"](h_card, h_action, h_s)
        mean_q, std_q = models["PosteriorDecoder"](h_card, h_action, h_s, h_s_next)
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
        mean_p = batch["mean_p"]
        std_p = batch["std_p"].clamp_min(1e-6)

        mean_q = batch["mean_q"]
        std_q = batch["std_q"].clamp_min(1e-6)

        kl_loss= torch.log(std_q / std_p) + (std_p.pow(2) + (mean_p - mean_q).pow(2)) / (2 * std_q.pow(2)) - 0.5

        return kl_loss.sum(dim=-1).mean()


    def reconstruction_loss(self, batch):
        pred = batch["pred_next"]
        target = squeeze_time_dim_state(batch["next_state"])

        result={}
        result["total_loss"] = pred["global_state"].new_zeros(())

        # 全局状态：self_life、oppo_life、self_mana
        result["global_state_loss"] = F.mse_loss(
            pred["global_state"],
            target["global_state"].float(),
        )
        result["total_loss"]=result["total_loss"]+result["global_state_loss"]*self.config.get("w_global_state_loss",1.0)
        for zone_name in ["hand", "library", "graveyard", "stack_cards"]:
            result[f"card_zone_loss_{zone_name}"] = card_zone_loss(
                pred["card_zones"][zone_name],
                target["card_zones"][zone_name],
            )
            result["total_loss"]=result["total_loss"]+result[f"card_zone_loss_{zone_name}"]*self.config.get(f"w_card_zone_loss_{zone_name}",1.0)

        for zone_name in ["self_board", "oppo_board"]:
            result[f"board_zone_loss_{zone_name}"] = board_zone_loss(
                pred["board_zones"][zone_name],
                target["board_zones"][zone_name],
            )
            result["total_loss"]=result["total_loss"]+result[f"board_zone_loss_{zone_name}"]*self.config.get(f"w_board_zone_loss_{zone_name}",1.0)

        return result

    
    
    
