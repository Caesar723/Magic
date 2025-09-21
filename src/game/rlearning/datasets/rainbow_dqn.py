from jinja2 import pass_context
import torch
import numpy as np
from collections import deque
import random
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


class RainbowDQNDataset(BaseDataset):
    def __init__(self, config):
        super().__init__(config)
        self.capacity = config["rainbowdqn"]["tree_capacity"]
        self.tree = np.zeros(2 * self.capacity - 1, dtype=np.float32)
        self.datatree = [None] * self.capacity
        self.nstep_buffer = deque(maxlen=config["rainbowdqn"]["nstep"])
        self.write = 0
        self.n_entries = 0
        self.max_priority = config["rainbowdqn"]["max_priority"]

    def get_tree_idx(self, s):
        idx = 0
        while True:
            left = 2 * idx + 1
            right = left + 1
            if left >= len(self.tree):
                return idx
            if s <= self.tree[left]:
                idx = left
            else:
                s -= self.tree[left]
                idx = right
    
    def __len__(self):
        return self.n_entries

    def __getitem__(self, idx):
        #print(idx)
        total = self.tree[0]
        seg = total / self.config["dataloader"]["batch_size"]
        i = idx % self.config["dataloader"]["batch_size"]
        #print(i)

        s = random.uniform(seg*i, seg*(i+1))
        idx = self.get_tree_idx(s)
        data_idx = idx - self.capacity + 1
        # print(self.tree)
        # print(s)
        # print(idx)
        # print(data_idx)
        data = self.datatree[data_idx]
        #print(data)
        data["idxs"] = idx
        data["priorities"] = self.tree[idx]

        return self.get_sample_preprocess(data,extra_keys=["state"]) 

    def add_to_tree(self, data,p):
        idx = self.write + self.capacity - 1
        self.datatree[self.write] = data
        self.update_tree(idx, p)
        self.write = (self.write + 1) % self.capacity
        self.n_entries = min(self.capacity, self.n_entries + 1)

    def update_tree(self, idx, p):
        change = p - self.tree[idx]
        self.tree[idx] = p
        while idx != 0:
            idx = (idx - 1) // 2
            self.tree[idx] += change

    def update_priority(self, idxs, priorities):
        for idx, p in zip(idxs, priorities):
            self.update_tree(idx, p ** self.config["rainbowdqn"]["alpha"])
            self.max_priority = max(self.max_priority, p)


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


   

    def store_data(self, data):
        data_batch={
            "state": data["state"],
            "action": data["action"],
            "reward": data["reward"],
            "next_state": data["next_state"],
            "done": data["done"],
            "global_reward": data["global_reward"]
        }
        self.nstep_buffer.append(data_batch)
        self.datas.append(data_batch)

        if len(self.nstep_buffer) < self.config["rainbowdqn"]["nstep"]:
            return

        nstep_data = self._get_n_step()
        self.add_to_tree(nstep_data,self.max_priority ** self.config["rainbowdqn"]["alpha"])
        if self.pbar is not None:
            self.pbar.n = self.n_entries
            self.pbar.refresh()
            if self.n_entries > self.config.get("max_store", 1000):
                self.pbar.close()
                self.pbar=None

    def clear_data(self):
        super().clear_data()
        self.n_entries=0


    def _get_n_step(self):
        R = 0.0
        for i, trans in enumerate(self.nstep_buffer):
            R += (self.config["rainbowdqn"]["gamma"] ** i) * trans["reward"]
            if trans["done"]:
                break
        return {
            "state":self.nstep_buffer[0]["state"],
            "action":self.nstep_buffer[0]["action"],
            "reward":R,
            "next_state":self.nstep_buffer[i]["next_state"],
            "done":self.nstep_buffer[i]["done"],
            "global_reward": self.nstep_buffer[i]["global_reward"]
        }
                
    @torch.no_grad()
    def data_preprocess(self,trainer):

        batch_extra=_collate_batch(
            self.datas,["global_reward"],["reward","done","action"]
        )
        self.log_data(trainer,batch_extra)
        

        # print(batch_extra["action"])
        # print(success_reward,batch_extra["done"])

        
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
        batch["self_life"]=batch["self_life"].to(torch.float32) 
        batch["oppo_life"]=batch["oppo_life"].to(torch.float32) 

        
        return batch
    
    

    
    
    def collate_fn(self,batch):
        batch=batch.copy()
        
        batch_state=self.collate_state(
            batch,["state"]
        )
        batch_next_state=self.collate_state(
            batch,["state"]
        )
        batch_extra=_collate_batch(batch,["idxs","priorities"],["action","done","reward"])
        total = self.tree[0]
        probs = np.array(batch_extra["priorities"]) / total
        weights = (len(self.tree.data) * probs) ** (-self.config["dataloader"]["beta"])
        weights /= weights.max()

        batch_extra["weights"]=torch.from_numpy(weights)
        batch_extra["state"]=batch_state
        batch_extra["next_state"]=batch_next_state
        

        return batch_extra

   