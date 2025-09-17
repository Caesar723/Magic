import torch
import numpy as np
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

from game.rlearning.utils.baseDataset import BaseDataset
from game.rlearning.utils.data import batch_to_cuda,detach_cuda,to_cpu,to_cuda
import game.rlearning.utils.log as log


def nested_get(d, keys):
    for k in keys:
        if not isinstance(d,dict) or k not in d:
            return None
        d = d[k]
    return d

def _collate_batch(batch, s_keys, g_keys,extra_keys=[]):
    #规定&为字典层级分割符
    
    collate_batch = {}
    #-----------------------
    for k in s_keys:
        k=k.split("&")
        v=nested_get(batch[0],k)
        if v is None:
            continue
        collate_batch["_".join(k)] = [ nested_get(b,k) for b in batch ]

    #-----------------------

    for k in g_keys:
        k=k.split("&")
        v=nested_get(batch[0],k)
        
        
        if v is None:
            continue
        v = [ torch.from_numpy(np.array(nested_get(b,k))) for b in batch ]
        for ek in extra_keys:
            if ek in k:
                k.remove(ek)
        collate_batch["_".join(k)] = torch.stack(v, dim=0)
        # print(collate_batch[k].shape)
        # print(k)
    
    return collate_batch


class PPOAgentDataset(BaseDataset):
    def __init__(self, config):
        super().__init__(config)
        

    def normalize_adv(self,adv:torch.Tensor):
        return ((adv - adv.mean()) / (adv.std() + 1e-5))

    def get_sample(self, data):
        
        
        card_ids=data["card_hand"]["card_ids"]
        #print(card_ids)
        id_dict={}
        for i in card_ids:
            if i==0:continue
            id_dict[i]=id_dict.get(i,0)+1
        card_mat=np.zeros((4,40))
        #print(id_dict)
        for i in id_dict:
            id_dict[i]=max(0,min(id_dict[i],4))
            if id_dict[i]==0:continue
            card_mat[id_dict[i]-1][i-1]=1
        #print(card_mat)

        data["card_hand"]["card_matrix"]=card_mat
        action_history_one_hot=np.zeros((self.config["action_history_length"],61))
        for i in range(len(data["action_history"])):
            action_history_one_hot[i][data["action_history"][i]]=1
        data["action_history_one_hot"]=action_history_one_hot
        data["action_history_length"]=len(data["action_history"])
        
        return data


    def advantage_cal(self,delta:torch.Tensor,done:torch.Tensor):
        advantage_list=[]
        advantage=0
        #print(delta.cpu().numpy())
        for reward,done in zip(delta.cpu().numpy()[::-1],done.cpu().numpy()[::-1]):
            if done:
                advantage=0
            advantage=reward+self.config["ppo"]["lambd"]*self.config["ppo"]["gamma"]*advantage
            # print(advantage)
            # print()
            advantage_list.insert(0,advantage)
        #print(advantage_list)
        return np.array(advantage_list)
    
    @torch.no_grad()
    def data_preprocess(self,trainer):
        
        batch_extra=_collate_batch(
            self.datas,["global_reward"],["reward","done","action"]
        )
        
        batch_extra["global_reward"]=sum(batch_extra["global_reward"])/self.config["max_store"]
        reward_train=(torch.sum(batch_extra["reward"])/self.config["max_store"]).cpu().numpy()

        success_reward=batch_extra["reward"][batch_extra["done"]==1].cpu().numpy()
        success_rate=sum((success_reward+1)/2)/len(success_reward)
        log.SW.add_scalars( f"global_reward", {trainer.name:batch_extra["global_reward"]}, trainer.step) 
        log.SW.add_scalars( f"reward_train", {trainer.name:reward_train}, trainer.step) 
        log.SW.add_scalars( f"success_rate", {trainer.name:success_rate}, trainer.step) 
        
        
        batch_extra["action"]=batch_extra["action"].unsqueeze(-1)
        batch_extra["reward"]=batch_extra["reward"].unsqueeze(-1)
        batch_extra["done"]=batch_extra["done"].unsqueeze(-1)
        print(batch_extra["done"])
        
        


        
        state_result=trainer.choose_action(self.datas,["state"])
        next_state_result=trainer.choose_action(self.datas,["next_state"])

        batch_extra["done"]=batch_extra["done"].to(torch.int32)
        
        batch_extra=batch_to_cuda(batch_extra,0)
        delta=batch_extra["reward"]+self.config["ppo"]["gamma"]*next_state_result["value"]*(1-batch_extra["done"])-state_result["value"]
        
        advantage=self.advantage_cal(delta,batch_extra["done"])

        advantage=to_cuda(torch.FloatTensor(advantage).detach(),0)
        rewards=advantage+state_result["value"]
        advantage=self.normalize_adv(advantage)
        clip_value=self.config["ppo"].get("clip_value_advantage",50.0)
        advantage=torch.clamp(advantage,-clip_value,clip_value)
        
        old_prob_log=state_result["dist"].log_prob(batch_extra["action"].squeeze(-1))


        advantage=advantage.cpu()
        rewards=rewards.cpu()
        old_prob_log=old_prob_log.cpu()
        old_actions=state_result["actions"].cpu()

        print(advantage.shape,rewards.shape,old_prob_log.shape)
        
        for i in range(len(self.datas)):
            self.datas[i]["advantage"]=advantage[i]
            self.datas[i]["rewards_adv"]=rewards[i]
            self.datas[i]["old_prob_log"]=old_prob_log[i]
            self.datas[i]["old_actions"]=old_actions[i]

        return self.datas
    
    
    
    
    

    def collate_state(self,batch,extra_keys=[]):
        s_keys=[]
        g_keys=[
            "self_life","oppo_life","self_mana","action_history_one_hot","action_history_length",
            "card_hand&card_matrix",
            # "card_hand&card_ids","card_hand&card_types",
            # "card_hand&card_costs","card_hand&card_special_types",
            # "card_hand&card_atks","card_hand&card_hps",
            # "card_hand&card_has_attack","card_hand&card_has_defend",
            # "card_hand&card_mask",

            "self_board&card_special_types","self_board&card_atks","self_board&card_hps",
            "self_board&card_has_attack","self_board&card_has_defend","self_board&card_mask",

            "oppo_board&card_special_types","oppo_board&card_atks","oppo_board&card_hps",
            "oppo_board&card_has_attack","oppo_board&card_has_defend","oppo_board&card_mask",

            "attacker&card_special_types","attacker&card_atks","attacker&card_hps",
            "attacker&card_has_attack","attacker&card_has_defend",
        ]
        
        for key in extra_keys[::-1]:
            for i in range(len(g_keys)):
                g_keys[i]=key+"&"+g_keys[i]
            
            
            
        
        
        batch=_collate_batch(batch,s_keys,g_keys,extra_keys)

        batch["action_history_one_hot"]=batch["action_history_one_hot"].to(torch.float32)
        batch["card_hand_card_matrix"]=batch["card_hand_card_matrix"].to(torch.float32)
        batch["self_life"]=batch["self_life"].to(torch.float32) 
        batch["oppo_life"]=batch["oppo_life"].to(torch.float32) 

        
        return batch
    
    

    
    
    def collate_fn(self,batch):
        batch=batch.copy()
        
        batch_state=self.collate_state(
            batch,["state"]
        )
        batch_extra=_collate_batch(batch,[],["action","advantage","rewards_adv","old_prob_log","old_actions"])

        batch_state.update(batch_extra)
        

        return batch_state