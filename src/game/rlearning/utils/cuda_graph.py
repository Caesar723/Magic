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
            return {
                name:self._copy_outputs(item)
                for name,item in value.items()
            }
        if isinstance(value,(tuple,list)):
            items=[self._copy_outputs(item) for item in value]
            return tuple(items) if isinstance(value,tuple) else items
        if value is None or isinstance(value,(bool,int,float,str)):
            return value
        raise TypeError(f"Unsupported output type: {type(value)}")

    def _copy_inputs(self,buffers,inputs,layout):
        if layout is not None:
            layout.copy_inputs(buffers,inputs)
        else:
            for name,value in inputs.items():
                buffers[name].copy_(value)

    def _capture(self,function,inputs,device,plan,layout):
        if layout is None:
            buffers={
                name:value.detach().clone()
                for name,value in inputs.items()
            }
        else:
            buffers={
                name:value.new_empty(plan["shapes"][name])
                for name,value in inputs.items()
            }
            self._copy_inputs(buffers,inputs,layout)

        current=torch.cuda.current_stream(device)
        stream=torch.cuda.Stream(device=device)
        stream.wait_stream(current)

        with torch.cuda.stream(stream):
            for _ in range(3):
                function(buffers)

        current.wait_stream(stream)
        graph=torch.cuda.CUDAGraph()

        with torch.cuda.graph(graph,stream=stream):
            outputs=function(buffers)

        current.wait_stream(stream)
        return {
            "graph":graph,
            "inputs":buffers,
            "outputs":outputs
        }

    @torch.no_grad()
    def run(self,function,inputs,layout=None):
        device=next(iter(inputs.values())).device

        if device.type!="cuda" or self.max_graphs==0:
            self.stats["eager"]+=1
            return function(inputs)

        if any(value.device!=device for value in inputs.values()):
            raise ValueError("Graph inputs must be on the same CUDA device")

        plan=layout.plan(inputs) if layout is not None else {
            "sizes":{},
            "shapes":{
                name:tuple(value.shape)
                for name,value in inputs.items()
            }
        }

        if plan is None:
            self.stats["eager"]+=1
            return function(inputs)

        signature=tuple(
            (name,plan["shapes"][name],value.dtype,value.device)
            for name,value in sorted(inputs.items())
        )
        key=(
            signature,
            id(layout),
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
                entry=self._capture(function,inputs,device,plan,layout)

            self.entries[key]=entry
            self.seen.pop(key,None)
            self.stats["captures"]+=1

        with torch.cuda.device(device):
            self._copy_inputs(entry["inputs"],inputs,layout)
            entry["graph"].replay()

            outputs=entry["outputs"]
            if layout is not None:
                outputs=layout.output_view(outputs,plan["sizes"])

            outputs=self._copy_outputs(outputs)

        self.stats["replays"]+=1
        return outputs