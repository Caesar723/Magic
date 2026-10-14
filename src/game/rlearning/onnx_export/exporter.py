import argparse
import inspect
import json
import sys
from contextlib import contextmanager
from pathlib import Path

import numpy as np
import torch


SRC_ROOT=Path(__file__).resolve().parents[3]
PROJECT_ROOT=SRC_ROOT.parent
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0,str(SRC_ROOT))

from game.rlearning.onnx_export.base import ONNXExportWrapper,replace_rms_norm
from game.rlearning.utils.common import CHECKPOINT_ROOT_PATH
from game.rlearning.utils.file import read_yaml
from game.rlearning.utils.model import get_class_by_name,init_model


@contextmanager
def disable_mha_fastpath():
    mha_backend=getattr(torch.backends,"mha",None)
    if mha_backend is None or not hasattr(mha_backend,"set_fastpath_enabled"):
        yield
        return

    enabled=mha_backend.get_fastpath_enabled()
    mha_backend.set_fastpath_enabled(False)
    try:
        yield
    finally:
        mha_backend.set_fastpath_enabled(enabled)


def resolve_path(path,config_path=None):
    path=Path(path).expanduser()
    if path.is_absolute():
        return path

    candidates=[]
    if config_path is not None:
        candidates.append(Path(config_path).resolve().parent/path)
    candidates.extend((Path.cwd()/path,PROJECT_ROOT/path,SRC_ROOT/path))

    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    return (PROJECT_ROOT/path).resolve()


def resolve_checkpoint(training_config,onnx_config,step_override=None):
    step=onnx_config.get("restore_step",training_config.get("restore_step",0))
    if step_override is not None:
        step=step_override
    step=int(step)

    if step==0:
        raise ValueError("restore_step cannot be 0 when exporting ONNX")

    group=onnx_config.get("checkpoint_group","g")
    checkpoint_root=Path(onnx_config.get("checkpoint_root",CHECKPOINT_ROOT_PATH)).expanduser()
    checkpoint_dir=checkpoint_root/training_config["log_dir"]/"ckpt"
    checkpoint_path=checkpoint_dir/f"{group}_{'last' if step==-1 else step}"

    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")

    resolved_path=checkpoint_path.resolve()
    prefix=f"{group}_"
    actual_step=resolved_path.name[len(prefix):] if resolved_path.name.startswith(prefix) else str(step)
    return resolved_path,actual_step


def load_checkpoint(path):
    checkpoint=torch.load(path,map_location="cpu",weights_only=True)
    if "state_dict" in checkpoint:
        checkpoint=checkpoint["state_dict"]
    if not isinstance(checkpoint,dict):
        raise TypeError(f"Checkpoint must contain a dict: {path}")
    return checkpoint


def load_models(training_config,onnx_config,checkpoint,device):
    model_configs=training_config.get("model",{})
    model_names=onnx_config.get("model_names",[])
    if not model_names:
        raise ValueError("model_names cannot be empty")

    models={}
    for name in model_names:
        if name not in model_configs:
            raise KeyError(f"Model {name} is not defined in training config")
        if name not in checkpoint:
            raise KeyError(f"Model {name} is not present in checkpoint")

        model=init_model(model_configs[name])
        model.load_state_dict(checkpoint[name],strict=True)
        model.to(device).eval()
        for parameter in model.parameters():
            parameter.requires_grad_(False)
        models[name]=model
    return models


def normalize_outputs(outputs,output_names):
    if torch.is_tensor(outputs):
        outputs=(outputs,)
    elif isinstance(outputs,dict):
        outputs=tuple(outputs[name] for name in output_names)
    else:
        outputs=tuple(outputs)

    if len(outputs)!=len(output_names):
        raise ValueError(f"Expected {len(output_names)} outputs, got {len(outputs)}")
    if not all(torch.is_tensor(value) for value in outputs):
        raise TypeError("Every ONNX output must be a tensor")
    return outputs


def verify_onnx(wrapper,example_inputs,onnx_path,atol=1e-4,rtol=1e-4):
    try:
        import onnxruntime as ort
    except ImportError as error:
        raise RuntimeError("verify=true requires onnxruntime") from error

    with disable_mha_fastpath(),torch.no_grad():
        torch_outputs=normalize_outputs(wrapper(*example_inputs),wrapper.output_names)

    session=ort.InferenceSession(str(onnx_path),providers=["CPUExecutionProvider"])
    values={
        name:value.detach().cpu().numpy()
        for name,value in zip(wrapper.input_names,example_inputs)
    }
    ort_inputs={item.name:values[item.name] for item in session.get_inputs()}
    onnx_outputs=session.run(list(wrapper.output_names),ort_inputs)

    errors={}
    for name,torch_output,onnx_output in zip(wrapper.output_names,torch_outputs,onnx_outputs):
        expected=torch_output.detach().cpu().numpy()
        np.testing.assert_allclose(onnx_output,expected,atol=atol,rtol=rtol)
        errors[name]=float(np.max(np.abs(onnx_output-expected))) if expected.size else 0.0
    return errors


def export_onnx(config_path,step_override=None,output_override=None,device_override=None):
    config_path=resolve_path(config_path)
    onnx_config=read_yaml(config_path)
    training_config_path=resolve_path(onnx_config["training_config_path"],config_path)
    training_config=read_yaml(training_config_path)

    export_config=onnx_config.get("export",{})
    device_name=device_override or export_config.get("device","cpu")
    if device_name.startswith("cuda") and not torch.cuda.is_available():
        raise RuntimeError("CUDA export was requested but CUDA is unavailable")
    device=torch.device(device_name)

    checkpoint_path,actual_step=resolve_checkpoint(training_config,onnx_config,step_override)
    checkpoint=load_checkpoint(checkpoint_path)
    models=load_models(training_config,onnx_config,checkpoint,device)

    wrapper_class=get_class_by_name(onnx_config["wrapper_class_name"])
    if not issubclass(wrapper_class,ONNXExportWrapper):
        raise TypeError("wrapper_class_name must point to an ONNXExportWrapper subclass")

    wrapper=wrapper_class(
        models=models,
        training_config=training_config,
        export_config=onnx_config
    )
    wrapper=replace_rms_norm(wrapper).to(device).eval()
    example_inputs=wrapper.prepare_example_inputs(device)

    output_value=output_override or onnx_config.get("output_path")
    if not output_value:
        output_value=f"checkpoints/onnx/action_embedder_step_{actual_step}.onnx"
    output_value=str(output_value).format(step=actual_step)
    output_path=resolve_path(output_value,config_path)
    output_path.parent.mkdir(parents=True,exist_ok=True)

    dynamic_axes=wrapper.get_dynamic_axes(
        dynamic_batch=export_config.get("dynamic_batch",True),
        dynamic_candidates=export_config.get("dynamic_candidates",True)
    )
    opset_version=int(export_config.get("opset_version",18))

    with disable_mha_fastpath(),torch.no_grad():
        normalize_outputs(wrapper(*example_inputs),wrapper.output_names)
        export_kwargs={
            "input_names":list(wrapper.input_names),
            "output_names":list(wrapper.output_names),
            "dynamic_axes":dynamic_axes or None,
            "opset_version":opset_version,
            "do_constant_folding":True
        }
        if "dynamo" in inspect.signature(torch.onnx.export).parameters:
            export_kwargs["dynamo"]=False
        torch.onnx.export(wrapper,example_inputs,str(output_path),**export_kwargs)

    errors={}
    if export_config.get("verify",True):
        errors=verify_onnx(
            wrapper,
            example_inputs,
            output_path,
            atol=float(export_config.get("atol",1e-4)),
            rtol=float(export_config.get("rtol",1e-4))
        )

    metadata={
        "training_config_path":str(training_config_path),
        "checkpoint_path":str(checkpoint_path),
        "restore_step":actual_step,
        "wrapper_class_name":onnx_config["wrapper_class_name"],
        "model_names":list(models),
        "input_names":list(wrapper.input_names),
        "output_names":list(wrapper.output_names),
        "opset_version":opset_version,
        "dynamic_axes":dynamic_axes,
        "verification_max_abs_error":errors
    }
    metadata_path=output_path.with_suffix(".json")
    with open(metadata_path,"w",encoding="utf-8") as file:
        json.dump(metadata,file,ensure_ascii=False,indent=2)

    return output_path,metadata_path,metadata


def main():
    parser=argparse.ArgumentParser(description="Export selected checkpoint models to ONNX")
    parser.add_argument("-c","--config",required=True,help="Path to ONNX export config")
    parser.add_argument("-r","--restore-step",type=int,default=None)
    parser.add_argument("-o","--output",default=None)
    parser.add_argument("--device",default=None)
    args=parser.parse_args()

    output_path,metadata_path,metadata=export_onnx(
        args.config,
        step_override=args.restore_step,
        output_override=args.output,
        device_override=args.device
    )
    print(f"ONNX saved to {output_path}")
    print(f"Metadata saved to {metadata_path}")
    for name,error in metadata["verification_max_abs_error"].items():
        print(f"{name} max abs error: {error:.8f}")


if __name__=="__main__":
    main()
