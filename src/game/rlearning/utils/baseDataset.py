import torch
import numpy as np

from torch.utils.data import Dataset
from tqdm import tqdm

import game.rlearning.utils.log as log
from game.rlearning.utils.common import CHECKPOINT_ROOT_PATH
from game.game_function_tool import ORGPATH

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
class BaseDataset(Dataset):
    def __init__(self, config):
        self.config = config
        self.datas=[]
        self.logdir = f'{ORGPATH}/../{CHECKPOINT_ROOT_PATH}/{config["log_dir"]}'
        self.pbar = tqdm(total=self.config.get("max_store", 1000), desc="Storing Samples", unit="sample")

    
    def store_data(self, data):
        data_batch={
            "state": data["state"],
            "action": data["action"],
            "reward": data["reward"],
            "next_state": data["next_state"],
            "done": data["done"],
            "global_reward": data["global_reward"]
        }
        self.datas.append(data_batch)
        if self.pbar is not None:
            self.pbar.n = len(self.datas)
            self.pbar.refresh()
            if len(self.datas) > self.config.get("max_store", 1000):
                self.pbar.close()
                self.pbar=None
        

    def log_data(self,trainer,batch_extra):
        batch_extra["global_reward"]=sum(batch_extra["global_reward"])/self.config["max_store"]
        reward_train=(torch.sum(batch_extra["reward"])/self.config["max_store"]).cpu().numpy()

        success_reward=batch_extra["reward"][batch_extra["done"]==1].cpu().numpy()
        success_rate=sum((success_reward+1)/2)/len(success_reward)
        log.SW.add_scalars( f"global_reward", {trainer.name:batch_extra["global_reward"]}, trainer.step) 
        log.SW.add_scalars( f"reward_train", {trainer.name:reward_train}, trainer.step) 
        log.SW.add_scalars( f"success_rate", {trainer.name:success_rate}, trainer.step) 

        if success_rate>0.8:
            with open(f"{self.logdir}/great_model.txt", "a", encoding="utf-8") as f:
                f.write(f"{trainer.step}\n")
        elif success_rate>0.6:
            with open(f"{self.logdir}/good_model.txt", "a", encoding="utf-8") as f:
                f.write(f"{trainer.step}\n")

    @torch.no_grad()
    def data_preprocess(self,trainer):
        pass
        

    def clear_data(self):
        self.datas = []
        self.pbar = tqdm(total=self.config.get("max_store", 1000), desc="Storing Samples", unit="sample")

    def get_sample(self, data):
        pass

    def get_sample_preprocess(self,data,extra_keys=[]):
        data=dict(data)
        pre_data=data
        for k in extra_keys:
            pre_data = pre_data[k]
        self.get_sample(pre_data)
        #print(data)
        return data

    def collate_fn(self, batch):
        pass

    def is_full(self):
        if self.__len__() > self.config.get("max_store", 1000):
            return True
        return False

    def __len__(self):
        return len(self.datas)

    def __getitem__(self, idx):
        idx = idx % len(self.datas)
        data = self.datas[idx]
        return self.get_sample_preprocess(data,extra_keys=["state"]) 