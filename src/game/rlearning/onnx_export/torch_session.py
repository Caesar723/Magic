from pathlib import Path

import numpy as np
import onnxruntime as ort
import torch


class TorchONNXSession:
    dtype_map={
        torch.float32:np.float32,
        torch.float64:np.float64,
        torch.int32:np.int32,
        torch.int64:np.int64,
        torch.bool:np.bool_
    }

    def __init__(self,path,device,providers):
        self.path=str(Path(path).resolve())
        self.device=torch.device(device)

        if not Path(self.path).exists():
            raise FileNotFoundError(f"ONNX file not found: {self.path}")

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