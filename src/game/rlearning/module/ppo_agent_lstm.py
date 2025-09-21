
import torch
import torch.nn.functional as F
from torch.nn.utils.rnn import pad_packed_sequence, pack_padded_sequence

from game.rlearning.utils.baseAgent import BaseTrainer



class PPOTrainer(BaseTrainer):
    def __init__(self, config,restore_step, rank=0, n_gpus=1,name="main"):
        super().__init__(config,restore_step, rank, n_gpus,name)

    def _forward(self, batch, models, isTrain, step, epoch):

        batch=self.predict(batch,models,isTrain,step,epoch)
        #print(batch["action"])
        batch["new_prob_log"]=batch["dist"].log_prob(batch["action"].squeeze(-1))

        total_loss=0

        loss={}
        

        if self.config.get("w_val_loss",0)>0:
            val_loss=F.mse_loss(batch["rewards_adv"].detach(),batch["value"])
            total_loss+=self.config["w_val_loss"]*val_loss
            loss["val_loss"]=val_loss

        if self.config.get("w_act_loss",0)>0:
            
            rate=torch.exp(batch["new_prob_log"]-batch["old_prob_log"].detach()).unsqueeze(1)

            adv = batch["advantage"].detach()
            surr1=rate*adv
            surr2=torch.clamp(rate,1-self.config["ppo"]["clip_para"],1+self.config["ppo"]["clip_para"])*adv
            
            act_loss=-torch.min(surr1,surr2).squeeze(1)#-0.01*batch["entropy"]
            act_loss=act_loss.mean()

            total_loss+=self.config["w_act_loss"]*act_loss
            loss["act_loss"]=act_loss

        if self.config.get("w_kl_loss",0)>0:
            old_dist=torch.distributions.Categorical(batch["old_actions"])
            kl_per_state = torch.distributions.kl.kl_divergence(old_dist, batch["dist"])
            #print(kl_per_state,kl_per_state.shape)
            kl_loss=kl_per_state.mean()
            total_loss+=self.config["w_kl_loss"]*kl_loss
            loss["kl_loss"]=kl_loss

        if self.config.get("w_entropy_loss",0)>0:
            entropy_loss=-batch["entropy"]
            total_loss+=self.config["w_entropy_loss"]*entropy_loss
            loss["entropy_loss"]=entropy_loss


        loss["total_loss"]=total_loss
        return loss

    def predict(self,batch,models,isTrain,step,epoch):
        print("HeroEmbedSelf")
        hero_embed_self=models["HeroEmbedSelf"](batch["self_life"])
        print("HeroEmbedOppo")
        hero_embed_oppo=models["HeroEmbedOppo"](batch["oppo_life"])
        print("ManaEmbed")
        mana_embed=models["ManaEmbed"](batch["self_mana"])
        print("CardsHandEmbed")
        cards_hand_embed=models["CardsHandEmbed"](
            batch["card_hand_card_matrix"],
        )
        print("CardsBoardEmbedSelf")
        cards_board_embed_self=models["CardsBoardEmbedSelf"](
            batch["self_board_card_special_types"],
            batch["self_board_card_atks"],
            batch["self_board_card_hps"],
            batch["self_board_card_has_attack"],
            batch["self_board_card_has_defend"],
            batch["self_board_card_mask"],
        )
        print("CardsBoardEmbedOppo")
        cards_board_embed_oppo=models["CardsBoardEmbedOppo"](
            batch["oppo_board_card_special_types"],
            batch["oppo_board_card_atks"],
            batch["oppo_board_card_hps"],
            batch["oppo_board_card_has_attack"],
            batch["oppo_board_card_has_defend"],
            batch["oppo_board_card_mask"],
        )
        print("AttackerEmbed")
        attacker_embed=models["AttackerEmbed"](
            batch["attacker_card_special_types"],
            batch["attacker_card_atks"],
            batch["attacker_card_hps"],
            batch["attacker_card_has_attack"],
            batch["attacker_card_has_defend"],
            
        ).squeeze(1)

        print("pack_padded_sequence")
        #print(batch["action_history_one_hot"])
        #print(batch["action_history_length"])

        lengths = batch["action_history_length"].cpu()
        packed = pack_padded_sequence(batch["action_history_one_hot"], lengths, batch_first=True, enforce_sorted=False)
        #batch["action_history_packed"]=packed
        print("HistoryEmbed")
        history_embed=models["HistoryEmbed"](packed)
        history_embed_output, _ = pad_packed_sequence(history_embed, batch_first=True)
        
        history_embed_output = history_embed_output[torch.arange(len(lengths)), lengths - 1]
        
        
        print("all_embed")
        batch["all_embed"]=torch.cat([
            hero_embed_self,
            hero_embed_oppo,
            mana_embed,
            cards_hand_embed,
            cards_board_embed_self,
            cards_board_embed_oppo,
            attacker_embed,
            history_embed_output,
        ],dim=-1)
        #print(batch["all_embed"].shape)
        print("Actor")
        batch["actions"]=models["Actor"](batch["all_embed"])
        print("dist")
        dist=torch.distributions.Categorical(batch["actions"])
        print("entropy")
        batch["dist"]=dist
        batch["entropy"]=dist.entropy()
        print("Critic")
        batch["value"]=models["Critic"](batch["all_embed"])
        print("return")


            


        return batch
    
    