import os
import torch
import numpy as np
import random
from torch.utils.data import Dataset
from tqdm import tqdm

from game.rlearning.utils.file import read_metadata
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
        self.pbar = self._new_pbar()

    def _new_pbar(self):
        # Rollout workers only collect data.  Their progress bars compete for
        # the same terminal and are intentionally disabled by the worker entry.
        if os.environ.get("RL_ROLLOUT_WORKER") == "1":
            return None
        return tqdm(total=self.config.get("max_store", 1000), desc="Storing Samples", unit="sample")

    
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

    def store_round_data(self,datas):
        for data in datas:
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
        self.pbar = self._new_pbar()

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




class ModelDataset(Dataset):
    
    def __init__(self, config, mode):
        super().__init__() 

        self.mode = mode 
        self.train = ( mode == "train" ) 
        self.config = config 
        if "dataset_root" in config:
            data_root = config["dataset_root"]
            self.dataset_paths = [f"{data_root}/{d}" for d in config['dataset_paths']]
        else:
            self.dataset_paths = config['dataset_paths']
        self.dataset_multiple = self.config["dataset_multiple"] if (self.train and "dataset_multiple" in self.config) else 1

        
        self.read_metadata() 
        
        assert len(self.metadata) > 0, "not find any valid metas"
        print(f"total {mode} meta size {len(self.metadata)}.")


    def read_metadata(self):
        metadata = []
        for dpath in self.dataset_paths:
            meta_file = f"{dpath}/{self.mode}.meta"
            
            if not os.path.isfile(meta_file):
                continue
            
            metas, _ = read_metadata( meta_file ) 
            #print(metas)
            #if self.config.get('use_filter_meta',False):
            #print(metas)
            
            
            for meta in metas:
                meta["dataset_path"] = dpath  
                metadata.append(meta)
            

            #print(f"load {len(metas)} metas from {meta_file}.")

        self.metadata = metadata 
        self.total_index = set(meta["index"] for meta in metadata) 


    def index_filter(self, index):
        if self.config.get("include_index_filter", None) is not None:
            for i in self.config["include_index_filter"]:
                if i in index:
                    return True
            return False
        if self.config.get("exclude_index_filter", None) is not None:
            for i in self.config["exclude_index_filter"]:
                if i in index:
                    return False
            return True
        return True



    def filter_metadata(self, dataset_path, metas: list):
        
        if self.filter_index is None:
            return metas
        filtered = []
        for meta in metas:
            index = meta["index"]
            if index in self.filter_index: 
                continue
            filtered.append(meta) 
        return filtered


    def __len__(self):
        return len(self.metadata) * self.dataset_multiple

    def __getitem__(self, idx):
        idx = idx % len(self.metadata)
        meta = self.metadata[idx] 
        return self.get_sample(meta) 

    def get_sample(self, meta):
        pass 

    def collate_fn(self, batch):
        pass 


class WeightedDataset(ModelDataset):
    """A ``ModelDataset`` that samples its configured folders by weight.

    ``dataset_paths`` uses the same direct-folder layout as ``ModelDataset``:

    .. code-block:: yaml

        dataset_root: /data/text_data
        dataset_paths:
          - fake_data_1bind_v1_20260823
          - fake_data_3bind_v1_20260823
        dataset_weights: [3.0, 1.0]

    Each path is read directly; child folders are deliberately not searched.
    A path can also be written as a mapping with an inline ``weight`` (and an
    optional display ``name``), for example ``{path: fake_data_1bind, weight:
    3.0}``.
    """

    def __init__(self, config, mode):
        base_config = dict(config)
        base_config.setdefault("dataset_paths", [])
        self.dataset_groups = self._parse_dataset_groups(base_config)
        # ``filter_metadata`` is used while the parent constructor calls our
        # ``read_metadata`` implementation.
        self.filter_index = None
        base_config["dataset_paths"] = [group["path"] for group in self.dataset_groups]

        super().__init__(base_config, mode)
        self.fixed_synthesis_metadata = None
        if (
            self.mode == "synthesis"
            and self.config.get("synthesis_fixed_items", True)
        ):
            self.fixed_synthesis_metadata = self._build_fixed_synthesis_metadata()

    @staticmethod
    def _path_weight(configured_weights, index, path, name):
        if configured_weights is None:
            return 1.0
        if isinstance(configured_weights, dict):
            return configured_weights.get(path, configured_weights.get(name, 1.0))
        return configured_weights[index]

    def _parse_dataset_groups(self, config):
        dataset_paths = config["dataset_paths"]
        configured_weights = config.get("dataset_weights", config.get("weights"))

        if configured_weights is not None and not isinstance(configured_weights, dict):
            if not isinstance(configured_weights, (list, tuple)):
                raise TypeError("dataset_weights must be a list or a path-to-weight mapping")
            if len(configured_weights) != len(dataset_paths):
                raise ValueError("dataset_weights must have one value per dataset_paths entry")

        groups = []
        for index, dataset_path in enumerate(dataset_paths):
            if isinstance(dataset_path, dict):
                path = dataset_path.get(
                    "path",
                    dataset_path.get(
                        "dataset_path",
                        dataset_path.get("folder_name", dataset_path.get("foldername")),
                    ),
                )
                name = dataset_path.get("name")
                weight = dataset_path.get(
                    "weight",
                    self._path_weight(configured_weights, index, path, name),
                )
            else:
                path = dataset_path
                name = None
                weight = self._path_weight(configured_weights, index, path, name)

            if path is None or str(path).strip() == "":
                raise ValueError("each dataset_paths entry must define a non-empty path")

            path = str(path)
            name = str(name) if name else os.path.basename(os.path.normpath(path))
            weight = float(weight)
            if weight < 0:
                raise ValueError(f"dataset group {name} has negative weight")

            groups.append({"name": name, "path": path, "weight": weight})
        return groups

    def _read_metadata_from_paths(self, dataset_paths, name=None):
        metadata = []

        for dpath in dataset_paths:
            meta_file = f"{dpath}/{self.mode}.meta"

            if not os.path.isfile(meta_file):
                continue
            #print(f"reading metadata from {meta_file}")
            metas, _ = read_metadata(meta_file)
            metas = self.filter_metadata(dpath, metas)

            for meta in metas:
                meta["dataset_path"] = dpath
                if name is not None:
                    meta["name"] = name
                metadata.append(meta)

        return metadata

    def _append_weighted_group(self, groups, name, weight, metadata):
        weight = float(weight)
        if weight < 0:
            raise ValueError(f"dataset group {name} has negative weight")
        if len(metadata) == 0 or weight == 0:
            return

        groups.append({
            "name": name,
            "weight": weight,
            "metadata": metadata,
        })

    def get_filterindex(self):
        indexs = set()
        for dpath in self.dataset_paths:
            meta_file = f"{dpath}/filtered.meta"
            if not os.path.isfile(meta_file):
                continue
            metas, _ = read_metadata(meta_file)
            for meta in metas:
                if self.index_filter(meta['index']):
                    indexs.add(meta['index'])
        self.filter_index = indexs

    def read_metadata(self):
        metadata = []
        weighted_groups = []

        # ``self.dataset_paths`` has already had ``dataset_root`` applied by
        # ModelDataset.  Pair it with the original group definitions so each
        # configured folder, rather than any of its children, is one sampling
        # group.
        for dpath, group in zip(self.dataset_paths, self.dataset_groups):
            group_metadata = self._read_metadata_from_paths([dpath], name=group["name"])
            self._append_weighted_group(
                weighted_groups,
                group["name"],
                group["weight"],
                group_metadata,
            )
            if group["weight"] > 0:
                metadata += group_metadata

        total_weight = sum(group["weight"] for group in weighted_groups)
        if len(weighted_groups) > 0 and total_weight <= 0:
            raise ValueError("weighted dataset groups must have positive total weight")

        self.metadata = metadata
        self.weighted_metadata_groups = weighted_groups
        self.weighted_metadata_group_weights = torch.as_tensor(
            [group["weight"] for group in weighted_groups],
            dtype=torch.float,
        )
        self.total_index = set(meta["index"] for meta in metadata)

    def __len__(self):
        fixed_metadata = getattr(self, "fixed_synthesis_metadata", None)
        if fixed_metadata is not None:
            return len(fixed_metadata)
        return super().__len__()

    def _build_fixed_synthesis_metadata(self):
        total = min(
            len(self.metadata),
            int(self.config.get("synthesis_items", 10)),
        )
        if total <= 0:
            return []
        if len(self.weighted_metadata_groups) == 0:
            seed = int(self.config.get("synthesis_seed", self.config.get("seed", 0)))
            return self._fixed_sample(self.metadata, total, seed)

        counts = self._fixed_synthesis_group_counts(total)
        seed = int(self.config.get("synthesis_seed", self.config.get("seed", 0)))
        metadata = []
        for group_index, (group, count) in enumerate(
            zip(self.weighted_metadata_groups, counts)
        ):
            metadata.extend(
                self._fixed_sample(
                    group["metadata"],
                    count,
                    seed + group_index * 1009,
                )
            )
        return metadata

    def _fixed_synthesis_group_counts(self, total):
        capacities = [
            len(group["metadata"]) for group in self.weighted_metadata_groups
        ]
        weights = [float(group["weight"]) for group in self.weighted_metadata_groups]
        target_total = min(total, sum(capacities))
        active = [
            index for index, capacity in enumerate(capacities)
            if capacity > 0 and weights[index] > 0
        ]
        if not active:
            return [0 for _ in self.weighted_metadata_groups]

        weight_sum = sum(weights[index] for index in active)
        counts = [0 for _ in self.weighted_metadata_groups]
        remainders = []
        for index in active:
            raw_count = target_total * weights[index] / weight_sum
            count = min(capacities[index], int(raw_count))
            counts[index] = count
            remainders.append((raw_count - count, index))

        remaining = target_total - sum(counts)
        remainders.sort(key=lambda item: (-item[0], item[1]))
        while remaining > 0:
            added = False
            for _, index in remainders:
                if counts[index] >= capacities[index]:
                    continue
                counts[index] += 1
                remaining -= 1
                added = True
                if remaining == 0:
                    break
            if not added:
                break
        return counts

    def _fixed_sample(self, metadata, count, seed):
        if count <= 0:
            return []
        indices = list(range(len(metadata)))
        random.Random(seed).shuffle(indices)
        return [metadata[index] for index in indices[:count]]

    def __getitem__(self, idx):
        fixed_metadata = getattr(self, "fixed_synthesis_metadata", None)
        if fixed_metadata is not None:
            meta = fixed_metadata[idx % len(fixed_metadata)]
            return self.get_sample(meta)

        if len(self.weighted_metadata_groups) == 0:
            return super().__getitem__(idx)

        group_idx = int(torch.multinomial(
            self.weighted_metadata_group_weights,
            num_samples=1,
        ).item())
        group_metadata = self.weighted_metadata_groups[group_idx]["metadata"]
        meta = group_metadata[torch.randint(len(group_metadata), (1,)).item()]
        return self.get_sample(meta)
