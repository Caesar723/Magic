import torch


class TensorBucketLayout:
    def __init__(self,buckets,input_axes,output_axes,padding_values=None,padding_hook=None):
        self.buckets={
            name:tuple(sorted(set(values)))
            for name,values in buckets.items()
        }
        if any(not values or values[0]<=0 for values in self.buckets.values()):
            raise ValueError("Bucket capacities must be positive")

        self.input_axes=input_axes
        self.output_axes=output_axes
        self.padding_values=padding_values or {}
        self.padding_hook=padding_hook

    def plan(self,inputs):
        if inputs.keys()!=self.input_axes.keys():
            raise ValueError("Input names do not match the tensor layout")

        sizes={}
        for name,axes in self.input_axes.items():
            for axis,dimension in axes.items():
                size=inputs[name].shape[axis]
                if sizes.setdefault(dimension,size)!=size:
                    raise ValueError(f"Inconsistent size for {dimension}")

        capacities={}
        for dimension,size in sizes.items():
            capacity=next(
                (value for value in self.buckets[dimension] if value>=size),None
            )
            if capacity is None:
                return None
            capacities[dimension]=capacity

        shapes={}
        for name,value in inputs.items():
            shape=list(value.shape)
            for axis,dimension in self.input_axes[name].items():
                shape[axis]=capacities[dimension]
            shapes[name]=tuple(shape)

        return {"sizes":sizes,"shapes":shapes}

    def copy_inputs(self,buffers,inputs):
        for name,value in inputs.items():
            target=buffers[name]
            if target.shape!=value.shape:
                target.fill_(self.padding_values.get(name,0))

            slices=tuple(slice(0,size) for size in value.shape)
            target[slices].copy_(value)

        if self.padding_hook is not None:
            self.padding_hook(buffers,inputs)

    def output_view(self,outputs,sizes):
        return self._view(outputs,self.output_axes,sizes)

    def _view(self,value,axes,sizes):
        if torch.is_tensor(value):
            slices=[slice(None)]*value.ndim
            for axis,dimension in axes.items():
                slices[axis]=slice(0,sizes[dimension])
            return value[tuple(slices)]

        if isinstance(value,dict):
            if value.keys()!=axes.keys():
                raise ValueError("Output names do not match the tensor layout")
            return {
                name:self._view(item,axes[name],sizes)
                for name,item in value.items()
            }

        if isinstance(value,(tuple,list)):
            if len(value)!=len(axes):
                raise ValueError("Output structure does not match the tensor layout")
            items=[
                self._view(item,item_axes,sizes)
                for item,item_axes in zip(value,axes)
            ]
            return tuple(items) if isinstance(value,tuple) else items

        if value is None or isinstance(value,(bool,int,float,str)):
            return value

        raise TypeError(f"Unsupported output type: {type(value)}")