from pathlib import Path
import os
import threading
import numpy as np
import onnxruntime as ort
import torch
import json

from game.rlearning.onnx_export.base import replace_rms_norm
from game.rlearning.onnx_export.exporter import load_checkpoint,load_models,normalize_outputs
from game.rlearning.utils.file import read_yaml
from game.rlearning.utils.model import get_class_by_name

class TorchONNXSession:
    dtype_map={
        torch.float32:np.float32,
        torch.float64:np.float64,
        torch.int32:np.int32,
        torch.int64:np.int64,
        torch.bool:np.bool_
    }
    _sessions={}
    _session_lock=threading.Lock()

    @classmethod
    def get(cls,path,device,providers,backend="onnx"):
        path=str(Path(path).resolve())
        device=torch.device(device)
        stream=None
        if device.type=="cuda":
            if device.index is None:
                device=torch.device("cuda",torch.cuda.current_device())
            stream=torch.cuda.current_stream(device).cuda_stream

        key=(os.getpid(),path,device,tuple(providers),stream,backend)
        with cls._session_lock:
            if key not in cls._sessions:
                cls._sessions[key]=cls(path,device,providers,backend)
            return cls._sessions[key]

    def __init__(self,path,device,providers,backend="onnx"):
        self.path=str(Path(path).resolve())
        self.device=torch.device(device)

        if not Path(self.path).exists():
            raise FileNotFoundError(f"ONNX file not found: {self.path}")
        if backend not in ("onnx","torch"):
            raise ValueError(f"Unknown embedding backend: {backend}")
        self.backend=backend
        if backend=="torch":
            self._init_torch()
            return
        available=set(ort.get_available_providers())
        session_options=ort.SessionOptions()
        session_options.graph_optimization_level=ort.GraphOptimizationLevel.ORT_ENABLE_ALL

        if self.device.type=="cuda":
            if "CUDAExecutionProvider" not in available:
                raise RuntimeError(f"CUDAExecutionProvider is unavailable: {sorted(available)}")

            device_id=self.device.index
            if device_id is None:
                device_id=torch.cuda.current_device()
                self.device=torch.device("cuda",device_id)

            cuda_options={
                "device_id":str(device_id),
                "user_compute_stream":str(torch.cuda.current_stream(self.device).cuda_stream)
            }
            session_providers=[("CUDAExecutionProvider",cuda_options)]
            if "CPUExecutionProvider" in providers:
                session_providers.append("CPUExecutionProvider")
        else:
            if "CPUExecutionProvider" not in available:
                raise RuntimeError(f"CPUExecutionProvider is unavailable: {sorted(available)}")
            session_providers=["CPUExecutionProvider"]

        self.session=ort.InferenceSession(
            self.path,
            sess_options=session_options,
            providers=session_providers
        )
        self.input_names={item.name for item in self.session.get_inputs()}
        self.output_names={item.name for item in self.session.get_outputs()}
    def _init_torch(self):
        metadata=json.loads(Path(self.path).with_suffix(".json").read_text())
        config=read_yaml(metadata["training_config_path"])
        checkpoint=load_checkpoint(metadata["checkpoint_path"])
        models=load_models(config,metadata,checkpoint,self.device)
        wrapper=get_class_by_name(metadata["wrapper_class_name"])
        self.model=wrapper(models,config,metadata)
        self.model=replace_rms_norm(self.model).to(self.device).eval()
        self.model.requires_grad_(False)
        self.input_names=set(self.model.input_names)
        self.output_names=set(self.model.output_names)

    @torch.no_grad()
    def _run_torch(self,inputs,output_specs):
        inputs={name:self._prepare_tensor(name,value) for name,value in inputs.items()}
        values=normalize_outputs(self.model(**inputs),self.model.output_names)
        outputs=dict(zip(self.model.output_names,values))
        result={}
        for name,(shape,dtype) in output_specs.items():
            value=outputs[name]
            if tuple(value.shape)!=tuple(shape) or value.dtype!=dtype or value.device!=self.device:
                raise ValueError(f"Unexpected output for {name}: {value.shape}, {value.dtype}, {value.device}")
            result[name]=value
        return result
    def _prepare_tensor(self,name,tensor):
        if not torch.is_tensor(tensor):
            raise TypeError(f"{name} must be a torch.Tensor")
        if tensor.device!=self.device:
            raise ValueError(f"{name} is on {tensor.device}, expected {self.device}")
        if tensor.dtype not in self.dtype_map:
            raise TypeError(f"{name} has unsupported dtype: {tensor.dtype}")
        return tensor.detach().contiguous()

    def run(self,inputs,output_specs):
        missing=self.input_names-set(inputs)
        unknown=set(inputs)-self.input_names
        if missing:
            raise KeyError(f"Missing ONNX inputs: {sorted(missing)}")
        if unknown:
            raise KeyError(f"Unknown ONNX inputs: {sorted(unknown)}")

        unknown_outputs=set(output_specs)-self.output_names
        if unknown_outputs:
            raise KeyError(f"Unknown ONNX outputs: {sorted(unknown_outputs)}")
        if self.backend=="torch":
            return self._run_torch(inputs,output_specs)
        io_binding=self.session.io_binding()
        bound_inputs={
            name:self._prepare_tensor(name,inputs[name])
            for name in self.input_names
        }

        device_id=self.device.index or 0
        for name,tensor in bound_inputs.items():
            io_binding.bind_input(
                name=name,
                device_type=self.device.type,
                device_id=device_id,
                element_type=self.dtype_map[tensor.dtype],
                shape=tuple(tensor.shape),
                buffer_ptr=tensor.data_ptr()
            )

        outputs={}
        for name,(shape,dtype) in output_specs.items():
            output=torch.empty(shape,dtype=dtype,device=self.device)
            io_binding.bind_output(
                name=name,
                device_type=self.device.type,
                device_id=device_id,
                element_type=self.dtype_map[dtype],
                shape=tuple(shape),
                buffer_ptr=output.data_ptr()
            )
            outputs[name]=output

        self.session.run_with_iobinding(io_binding)
        return outputs