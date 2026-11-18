import numpy as np
import torch


class PreparedPolicyBatch:
    def __init__(self):
        self.datasets={}

    def __call__(self,state,config_path):
        from game.rlearning.utils.file import read_yaml
        from game.rlearning.utils.model import get_class_by_name

        if config_path not in self.datasets:
            config=read_yaml(config_path)
            enabled=config.get("extra",{}).get("cuda_graph",{}).get("frozen_features",False)
            self.datasets[config_path]=get_class_by_name(
                config["dataset_class_name"]
            )(config) if enabled else None

        dataset=self.datasets[config_path]
        if dataset is None:
            return state

        batch=dataset.collate_inference([state],compact=True)

        def numpy(value):
            if torch.is_tensor(value):
                return value.numpy()
            if isinstance(value,dict):
                return {
                    name:numpy(item)
                    for name,item in value.items()
                }
            return value

        return {
            "_prepared_inference":numpy(batch),
            "_candidate_count":len(state["candidate_actions"])
        }

    @staticmethod
    def combine(values):
        def join(items,path=()):
            first=items[0]

            if isinstance(first,np.ndarray):
                axis=1 if path and path[0] in (
                    "actor_state_in","critic_state_in"
                ) else 0
                return np.concatenate(items,axis=axis)

            if isinstance(first,dict):
                return {
                    name:join(
                        [item[name] for item in items],path+(name,)
                    )
                    for name in first
                }

            raise TypeError(f"Unsupported prepared field: {path}")

        ordinary={
            name:[value[name] for value in values]
            for name in values[0]
            if name not in ("candidates","_packed_entities")
        }
        result={
            name:join(items,(name,))
            for name,items in ordinary.items()
        }

        entity_values=[value["_packed_entities"] for value in values]
        entities=entity_values[0]["mask"].shape[1]

        result["_packed_entities"]={
            "inputs":join([
                value["inputs"] for value in entity_values
            ]),
            "slots":np.concatenate([
                value["slots"]+row*entities
                for row,value in enumerate(entity_values)
            ]),
            "count":sum(
                value["count"] for value in entity_values
            ),
            "descriptions":[
                text
                for value in entity_values
                for text in value["descriptions"]
            ],
            "mask":join([
                value["mask"] for value in entity_values
            ]),
            "dynamic":join([
                value["dynamic"] for value in entity_values
            ])
        }

        candidates=[value["candidates"] for value in values]
        capacity=max(value["mask"].shape[2] for value in candidates)
        result["candidates"]={}

        for name,first in candidates[0].items():
            if name=="descriptions":
                result["candidates"][name]=[
                    [
                        value[name][0][0]
                        +[""]*(capacity-value["mask"].shape[2])
                    ]
                    for value in candidates
                ]
                continue

            shape=(len(values),1,capacity)+first.shape[3:]
            fill=-1 if name in ("indices","actions") else 0
            output=np.full(shape,fill,dtype=first.dtype)

            for row,value in enumerate(candidates):
                count=value["mask"].shape[2]
                output[row:row+1,:,:count]=value[name]

            result["candidates"][name]=output

        def tensor(value):
            if isinstance(value,np.ndarray):
                return torch.from_numpy(value)
            if isinstance(value,dict):
                return {
                    name:tensor(item)
                    for name,item in value.items()
                }
            return value

        return tensor(result)