import torch


from torch.utils.data import Dataset
from tqdm import tqdm


class BaseDataset(Dataset):
    def __init__(self, config):
        self.config = config
        self.datas=[]
        self.pbar = tqdm(total=self.config.get("max_store", 1000), desc="Storing Samples", unit="sample")

    def clear_data(self):
        self.datas=[]

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


    @torch.no_grad()
    def data_preprocess(self,trainer):
        pass

    def clear_data(self):
        self.datas = []
        self.pbar = tqdm(total=self.config.get("max_store", 1000), desc="Storing Samples", unit="sample")

    def get_sample(self, data):
        pass

    def collate_fn(self, batch):
        pass

    def is_full(self):
        if len(self.datas) > self.config.get("max_store", 1000):
            return True
        return False

    def __len__(self):
        return len(self.datas)

    def __getitem__(self, idx):
        idx = idx % len(self.datas)
        data = self.datas[idx]
        return self.get_sample(data) 