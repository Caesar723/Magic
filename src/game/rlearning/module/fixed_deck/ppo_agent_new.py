
import torch
import torch.nn.functional as F


from game.rlearning.utils.baseAgent import BaseTrainer



class PPOTrainer(BaseTrainer):
    def __init__(self, config,restore_step, rank=0, n_gpus=1,name="main"):
        super().__init__(config,restore_step, rank, n_gpus,name)

    def _forward(self, batch, models, isTrain, step, epoch):

        batch=self.predict(batch,models,isTrain,step,epoch)
        total_loss=0

        loss={}
        

        if self.config["w_val_loss"]>0:
            val_loss=F.mse_loss(batch["rewards_adv"].detach(),batch["value"])
            total_loss+=self.config["w_val_loss"]*val_loss
            loss["val_loss"]=val_loss

        if self.config["w_act_loss"]>0:
            new_prob_log=batch["dist"].log_prob(batch["action"].squeeze(-1))
            rate=torch.exp(new_prob_log-batch["old_prob_log"].detach()).unsqueeze(1)

            adv = batch["advantage"].detach()
            surr1=rate*adv
            surr2=torch.clamp(rate,1-self.config["ppo"]["clip_para"],1+self.config["ppo"]["clip_para"])*adv
            #print(surr1.squeeze(1).shape,surr2.squeeze(1).shape,batch["entropy"].shape)
            act_loss=-torch.min(surr1,surr2).squeeze(1)-0.01*batch["entropy"]
            act_loss=act_loss.mean()

            total_loss+=self.config["w_act_loss"]*act_loss
            loss["act_loss"]=act_loss


        loss["total_loss"]=total_loss
        return loss

    def predict(self,batch,models,isTrain,step,epoch):
        
        hero_embed_self=models["HeroEmbedSelf"](batch["self_life"])
        hero_embed_oppo=models["HeroEmbedOppo"](batch["oppo_life"])
        mana_embed=models["ManaEmbed"](batch["self_mana"])
        cards_hand_embed=models["CardsHandEmbed"](
            batch["card_hand_card_matrix"],
        )
        cards_board_embed_self=models["CardsBoardEmbedSelf"](
            batch["self_board_card_special_types"],
            batch["self_board_card_atks"],
            batch["self_board_card_hps"],
            batch["self_board_card_has_attack"],
            batch["self_board_card_has_defend"],
            batch["self_board_card_mask"],
        )
        cards_board_embed_oppo=models["CardsBoardEmbedOppo"](
            batch["oppo_board_card_special_types"],
            batch["oppo_board_card_atks"],
            batch["oppo_board_card_hps"],
            batch["oppo_board_card_has_attack"],
            batch["oppo_board_card_has_defend"],
            batch["oppo_board_card_mask"],
        )
        attacker_embed=models["AttackerEmbed"](
            batch["attacker_card_special_types"],
            batch["attacker_card_atks"],
            batch["attacker_card_hps"],
            batch["attacker_card_has_attack"],
            batch["attacker_card_has_defend"],
            
        ).squeeze(1)
        

        

        batch["all_embed"]=torch.cat([
            hero_embed_self,
            hero_embed_oppo,
            mana_embed,
            cards_hand_embed,
            cards_board_embed_self,
            cards_board_embed_oppo,
            attacker_embed,
        ],dim=-1)



        batch["actions"]=models["Actor"](batch["all_embed"])
        dist=torch.distributions.Categorical(batch["actions"])
        batch["dist"]=dist
        batch["entropy"]=dist.entropy()
        batch["value"]=models["Critic"](batch["all_embed"])


            


        return batch
    
    