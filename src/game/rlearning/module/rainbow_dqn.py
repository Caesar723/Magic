
import torch
import numpy as np
import torch.nn.functional as F
from torch.nn.utils.rnn import pad_packed_sequence, pack_padded_sequence

from game.rlearning.utils.baseAgent import BaseTrainer
from game.rlearning.utils.data import batch_to_cuda,to_cuda





class RainbowDQNTrainer(BaseTrainer):
    def __init__(self, config,restore_step, rank=0, n_gpus=1,name="main"):
        super().__init__(config,restore_step, rank, n_gpus,name)
        self.support = torch.from_numpy(np.linspace(self.config["rainbowdqn"]["v_min"], self.config["rainbowdqn"]["v_max"], self.config["rainbowdqn"]["atom_size"], dtype=np.float32))
        self.support =to_cuda(self.support,rank)

        self.models["Target"].load_state_dict(self.models["Online"].state_dict())

    def _forward(self, batch, models, isTrain, step, epoch):
        total_loss=0
        loss={}
        models["Online"].reset_noise()
        models["Target"].reset_noise()

        
        batch_state_result=self.predict(batch["state"],models,isTrain,step,epoch)
        eps =1e-8
        #print(batch_state_result["actions"][range(self.config["dataloader"]["batch_size"]), batch["action"]])
        log_p = torch.log(batch_state_result["actions"][range(self.config["dataloader"]["batch_size"]), batch["action"]]+eps)
        #print(log_p)
        with torch.no_grad():
            batch_next_state_result=self.predict(batch["next_state"],models,isTrain,step,epoch)
            next_q_online = torch.sum(batch_next_state_result["actions"] * self.support.view(1,1,-1), dim=2)
            next_actions = next_q_online.argmax(1)

            next_prob_target = models["Target"](batch_next_state_result["all_embed"])
            next_dist = next_prob_target[range(self.config["dataloader"]["batch_size"]), next_actions].cpu().numpy()

            target_dist = self.projection_distribution(
                next_dist, batch["reward"].cpu().numpy(), batch["done"].cpu().numpy(),
            )
            target_dist=to_cuda(torch.from_numpy(target_dist),self.rank)
            #print(target_dist)

        if self.config["w_q_loss"]>0:
            per_sample_loss = -torch.sum(target_dist * log_p, dim=1)
            loss_q = (per_sample_loss * batch["weights"]).mean()

            new_priorities = per_sample_loss.detach().cpu().numpy() + 1e-6
            #print(batch["idxs"],new_priorities)
            self.dataset.update_priority(batch["idxs"], new_priorities)

            total_loss+=self.config["w_q_loss"]*loss_q
            loss["q_loss"]=loss_q

        loss["total_loss"]=total_loss
        return loss

    def projection_distribution(self, next_dist, rewards, dones):
        batch_size = self.config["dataloader"]["batch_size"]
        v_min = self.config["rainbowdqn"]["v_min"]
        v_max = self.config["rainbowdqn"]["v_max"]
        atom_size = self.config["rainbowdqn"]["atom_size"]
        gamma = self.config["rainbowdqn"]["gamma"]
        n_step = self.config["rainbowdqn"]["nstep"]
        delta_z = float(v_max - v_min) / (atom_size - 1)
        support = np.linspace(v_min, v_max, atom_size, dtype=np.float32)
        projected = np.zeros((batch_size, atom_size), dtype=np.float32)
        for i in range(batch_size):
            Tz = rewards[i] + (1 - dones[i]) * (gamma ** n_step) * support
            Tz = np.clip(Tz, v_min, v_max)
            b = (Tz - v_min) / delta_z
            l = np.floor(b).astype(int)
            u = np.ceil(b).astype(int)
            for j in range(atom_size):
                if l[j] == u[j]:
                    projected[i, l[j]] += next_dist[i, j]
                else:
                    projected[i, l[j]] += next_dist[i, j] * (u[j] - b[j])
                    projected[i, u[j]] += next_dist[i, j] * (b[j] - l[j])
        return projected

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

        #print(batch["action_history_one_hot"])
        #print(batch["action_history_length"])

        lengths = batch["action_history_length"].cpu()
        packed = pack_padded_sequence(batch["action_history_one_hot"], lengths, batch_first=True, enforce_sorted=False)
        #batch["action_history_packed"]=packed
        history_embed=models["HistoryEmbed"](packed)
        history_embed_output, _ = pad_packed_sequence(history_embed, batch_first=True)
        
        history_embed_output = history_embed_output[torch.arange(len(lengths)), lengths - 1]
        
        

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

        batch["actions"]=models["Online"](batch["all_embed"])
        return batch

    @torch.no_grad()
    def choose_action(self,batch,extra_keys=[],isTrain=False):#如果是一个动作记得加[batch]
        models = self.models
        [ models[k].train() if isTrain else models[k].eval() for k in models ] 
        models["Online"].reset_noise()
        if "mask" in batch[0]:
            mask=batch[0]["mask"]
        else:
            mask=None
        batch=[self.dataset.get_sample_preprocess(b,extra_keys) for b in batch]
        batch=self.dataset.collate_state(batch,extra_keys)
        batch=batch_to_cuda(batch, self.rank)
        batch=self.predict(batch,models,False,self.step,self.epoch)
        actions=batch['actions']
        
        if mask is not None:
            
            
            
            q = torch.sum(actions * self.support.unsqueeze(0).unsqueeze(0), dim=2)
            q[mask==False]=-999
            
            action = q.argmax(1).item()
            
            batch["action"]=action
        return batch

    def check_log(self,loss_dict):
        super().check_log(loss_dict)
        if self.step % self.config["target_update_interval"] == 0:
            print(f"update target model at {self.step} step")
            self.models["Target"].load_state_dict(self.models["Online"].state_dict())
        
    
    