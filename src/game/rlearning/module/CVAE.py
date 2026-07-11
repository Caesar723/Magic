
import torch
import torch.nn.functional as F


from game.rlearning.utils.baseAgent import BaseTrainer



class CVAETrainer(BaseTrainer):
    def __init__(self, config,restore_step, rank=0, n_gpus=1,name="main"):
        super().__init__(config,restore_step, rank, n_gpus,name)

    def _forward(self, batch, models, isTrain, step, epoch):

        batch=self.encode(batch,models,isTrain,step,epoch)
        batch=self.decode(batch,models,isTrain,step,epoch)
        total_loss=0

        loss={}


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
        h_text = models["TextEncoder"](
            cu["description"],
            src_key_padding_mask=~cu["attention_mask"].bool(),
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
        pass


    def reconstruction_loss(self, batch):
        pass
    
    
    