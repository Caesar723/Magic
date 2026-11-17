from collections import OrderedDict
import torch


class CudaGraphRunner:
    def __init__(self,max_graphs=2,capture_after=3):
        self.max_graphs=max(0,int(max_graphs))
        self.capture_after=max(1,int(capture_after))
        self.entries={}
        self.seen=OrderedDict()
        self.stats={"captures":0,"replays":0,"eager":0}

    def _copy_outputs(self,value):
        if torch.is_tensor(value):
            return value.clone()
        if isinstance(value,dict):
            return {key:self._copy_outputs(item) for key,item in value.items()}
        if isinstance(value,tuple):
            return tuple(self._copy_outputs(item) for item in value)
        raise TypeError(f"Unsupported graph output: {type(value)}")

    def _capture(self,function,inputs,device):
        static_inputs={
            name:value.detach().clone()
            for name,value in inputs.items()
        }
        current=torch.cuda.current_stream(device)
        stream=torch.cuda.Stream(device=device)
        stream.wait_stream(current)

        with torch.cuda.stream(stream):
            for _ in range(3):
                function(static_inputs)

        current.wait_stream(stream)
        graph=torch.cuda.CUDAGraph()

        with torch.cuda.graph(graph,stream=stream):
            outputs=function(static_inputs)

        current.wait_stream(stream)
        return {
            "graph":graph,
            "inputs":static_inputs,
            "outputs":outputs
        }

    @torch.no_grad()
    def run(self,function,inputs):
        device=next(iter(inputs.values())).device
        if device.type!="cuda" or self.max_graphs==0:
            self.stats["eager"]+=1
            return function(inputs)

        if any(value.device!=device for value in inputs.values()):
            raise ValueError("Graph inputs must be on the same CUDA device")

        signature=tuple(
            (name,tuple(value.shape),value.dtype,value.device)
            for name,value in sorted(inputs.items())
        )
        key=(
            signature,
            torch.is_autocast_enabled("cuda"),
            torch.get_autocast_dtype("cuda"),
            torch.is_inference_mode_enabled()
        )
        entry=self.entries.get(key)

        if entry is None:
            if len(self.entries)>=self.max_graphs:
                self.stats["eager"]+=1
                return function(inputs)

            count=self.seen.get(key,0)+1
            self.seen[key]=count
            self.seen.move_to_end(key)

            if len(self.seen)>32:
                self.seen.popitem(last=False)

            if count<self.capture_after:
                self.stats["eager"]+=1
                return function(inputs)

            with torch.cuda.device(device):
                entry=self._capture(function,inputs,device)

            self.entries[key]=entry
            self.seen.pop(key,None)
            self.stats["captures"]+=1

        with torch.cuda.device(device):
            for name,value in inputs.items():
                entry["inputs"][name].copy_(value)

            entry["graph"].replay()
            outputs=self._copy_outputs(entry["outputs"])

        self.stats["replays"]+=1
        return outputs