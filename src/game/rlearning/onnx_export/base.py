from abc import ABC,abstractmethod

import torch
import torch.nn as nn


class ONNXExportWrapper(nn.Module,ABC):
    input_names=()
    output_names=()

    def __init__(self,models,training_config,export_config):
        super().__init__()
        self.models=nn.ModuleDict(models)
        self.training_config=training_config
        self.export_config=export_config

    @abstractmethod
    def forward(self,*inputs):
        raise NotImplementedError

    @abstractmethod
    def build_example_inputs(self):
        raise NotImplementedError

    def get_dynamic_axes(self,dynamic_batch=True,dynamic_candidates=True):
        return {}

    def validate_export_spec(self,example_inputs):
        if not self.input_names:
            raise ValueError("Wrapper input_names cannot be empty")
        if not self.output_names:
            raise ValueError("Wrapper output_names cannot be empty")
        if not isinstance(example_inputs,(tuple,list)):
            raise TypeError("build_example_inputs must return a tuple or list")
        if len(example_inputs)!=len(self.input_names):
            raise ValueError(
                f"Expected {len(self.input_names)} example inputs, got {len(example_inputs)}"
            )
        if not all(torch.is_tensor(value) for value in example_inputs):
            raise TypeError("Every ONNX example input must be a tensor")

    def prepare_example_inputs(self,device):
        example_inputs=tuple(self.build_example_inputs())
        self.validate_export_spec(example_inputs)
        return tuple(value.to(device) for value in example_inputs)


class ONNXCompatibleRMSNorm(nn.Module):
    def __init__(self,module):
        super().__init__()
        self.normalized_shape=tuple(module.normalized_shape)
        self.eps=module.eps
        if module.weight is None:
            self.register_parameter("weight",None)
        else:
            self.weight=nn.Parameter(
                module.weight.detach().clone(),
                requires_grad=module.weight.requires_grad
            )

    def forward(self,value):
        dims=tuple(range(value.ndim-len(self.normalized_shape),value.ndim))
        eps=torch.finfo(value.dtype).eps if self.eps is None else self.eps
        scale=torch.sqrt(value.square().mean(dim=dims,keepdim=True)+eps)
        result=value/scale
        return result if self.weight is None else result*self.weight


def replace_rms_norm(module):
    rms_norm=getattr(nn,"RMSNorm",None)
    if rms_norm is None:
        return module

    for name,child in list(module.named_children()):
        if isinstance(child,rms_norm):
            setattr(module,name,ONNXCompatibleRMSNorm(child))
        else:
            replace_rms_norm(child)
    return module
