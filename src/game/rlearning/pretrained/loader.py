from pathlib import Path
import os
import threading
import torch

from game.rlearning.utils.file import read_yaml
from game.rlearning.utils.model import get_class_by_name,init_model


class PretrainedSession:
    def __init__(self,model,operation,device):
        self.model=model
        method,self.output_names=model.operations[operation]
        self.function=getattr(model,method)
        self.device=torch.device(device)

    @torch.no_grad()
    def run(self,inputs,output_specs,**kwargs):
        unknown=set(output_specs)-set(self.output_names)
        if unknown:
            raise KeyError(f"Unknown outputs: {sorted(unknown)}")
        prepared={}
        for name,value in inputs.items():
            if not torch.is_tensor(value):
                raise TypeError(f"{name} must be a tensor")
            if value.device!=self.device:
                raise ValueError(f"{name} is on {value.device}, expected {self.device}")
            prepared[name]=value.detach().contiguous()

        values=self.function(**prepared,**kwargs)
        if isinstance(values,dict):
            outputs=values
        else:
            values=(values,) if torch.is_tensor(values) else tuple(values)
            if len(values)!=len(self.output_names):
                raise ValueError("Unexpected number of model outputs")
            outputs=dict(zip(self.output_names,values))
        for name,(shape,dtype) in output_specs.items():
            value=outputs[name]
            if tuple(value.shape)!=tuple(shape) or value.dtype!=dtype or value.device!=self.device:
                raise ValueError(f"Unexpected output {name}: {value.shape}, {value.dtype}, {value.device}")
        return {name:outputs[name] for name in output_specs}


class PretrainedLoader:
    _instances={}
    _lock=threading.Lock()

    @classmethod
    def get(cls,settings,device,root="."):
        root=Path(root).expanduser()
        def resolve(value):
            return str((root/Path(value).expanduser()).resolve())

        config_path=resolve(settings["config_path"])
        paths=settings["checkpoint"]
        paths=[paths] if isinstance(paths,(str,Path)) else paths
        paths=tuple(resolve(path) for path in paths)
        device=torch.device(device)
        if device.type=="cuda" and device.index is None:
            device=torch.device("cuda",torch.cuda.current_device())
        class_name=settings["class_name"]
        key=(os.getpid(),class_name,config_path,paths,device)
        with cls._lock:
            if key not in cls._instances:
                cls._instances[key]=cls(class_name,config_path,paths,device)
            return cls._instances[key]

    def __init__(self,class_name,config_path,checkpoint_paths,device):
        adapter=get_class_by_name(class_name)
        config=read_yaml(config_path)
        checkpoint={}
        for path in checkpoint_paths:
            state=torch.load(path,map_location="cpu",weights_only=True)
            checkpoint.update(state.get("state_dict",state))

        missing=[name for name in adapter.required_models if name not in checkpoint]
        if missing:
            raise KeyError(f"Checkpoint is missing models: {missing}")
        models={}
        for name in adapter.required_models:
            model=init_model(config["model"][name])
            model.load_state_dict(checkpoint[name],strict=True)
            models[name]=model.to(device).eval().requires_grad_(False)

        self.model=adapter(models,config).eval().requires_grad_(False)
        self.sessions={
            name:PretrainedSession(self.model,name,device)
            for name in self.model.operations
        }

    def session(self,name):
        return self.sessions[name]