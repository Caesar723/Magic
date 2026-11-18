from collections import OrderedDict

import torch


class CudaInputBuffer:
    def __init__(self,max_entries=16):
        self.max_entries=max(1,int(max_entries))
        self.entries=OrderedDict()

    def _leaves(self,value,path=()):
        if torch.is_tensor(value):
            yield path,value
        elif isinstance(value,dict):
            for name,item in value.items():
                yield from self._leaves(item,path+(name,))

    @torch.no_grad()
    def run(self,batch,device):
        device=torch.device(device)
        stream=torch.cuda.current_stream(device)
        leaves=list(self._leaves(batch))
        specs={}
        sizes={}

        for path,value in leaves:
            dtype=torch.float32 if value.dtype==torch.float64 else value.dtype
            item_size=4 if dtype==torch.float32 else value.element_size()
            alignment=max(1,256//item_size)
            offset=(sizes.get(dtype,0)+alignment-1)//alignment*alignment
            count=value.numel()
            specs[path]=(dtype,offset,count,tuple(value.shape))
            sizes[dtype]=offset+count

        capacities=tuple(
            (dtype,1 << (max(size,1)-1).bit_length())
            for dtype,size in sizes.items()
        )
        key=(device,stream.cuda_stream,capacities)
        entry=self.entries.get(key)

        if entry is None:
            groups={}
            for dtype,capacity in capacities:
                host=torch.zeros(capacity,dtype=dtype,pin_memory=True)
                view=host.view(torch.uint16) if dtype==torch.bfloat16 else host
                groups[dtype]={
                    "host":host,
                    "array":view.numpy(),
                    "device":torch.empty(capacity,dtype=dtype,device=device)
                }

            entry={
                "groups":groups,
                "event":torch.cuda.Event(),
                "recorded":False
            }
            self.entries[key]=entry

            if len(self.entries)>self.max_entries:
                _,retired=self.entries.popitem(last=False)
                if retired["recorded"]:
                    retired["event"].synchronize()
        else:
            self.entries.move_to_end(key)

        if entry["recorded"]:
            entry["event"].synchronize()

        for path,value in leaves:
            dtype,offset,count,shape=specs[path]
            source=value.detach().contiguous()
            if dtype==torch.bfloat16:
                source=source.view(torch.uint16)
            entry["groups"][dtype]["array"][offset:offset+count]=source.numpy().reshape(-1)

        for dtype,size in sizes.items():
            group=entry["groups"][dtype]
            group["device"][:size].copy_(
                group["host"][:size],non_blocking=True
            )

        entry["event"].record(stream)
        entry["recorded"]=True

        def restore(value,path=()):
            if torch.is_tensor(value):
                dtype,offset,count,shape=specs[path]
                return entry["groups"][dtype]["device"][offset:offset+count].view(shape)
            if isinstance(value,dict):
                return {
                    name:restore(item,path+(name,))
                    for name,item in value.items()
                }
            return value

        return restore(batch)