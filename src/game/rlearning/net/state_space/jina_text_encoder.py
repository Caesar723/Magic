import os
import torch
import torch.nn as nn
import torch.nn.functional as F

from game.rlearning.utils.paths import ProjectPaths



class JinaTextEncoder(nn.Module):
    def __init__(self,config):
        super().__init__()
        self.model_name=config.get("model_name","jinaai/jina-embeddings-v5-text-small")
        paths=ProjectPaths.get()
        local_path=paths.model_path(config.get("local_model_path"))
        self.local_model_path=str(local_path) if local_path is not None else None
        self.cache_dir=str(paths.cache_path(config.get("cache_dir")))
        self.task=config.get("task","text-matching")
        self.truncate_dim=config.get("truncate_dim",128)
        self.max_length=config.get("max_length")
        self.normalize=config.get("normalize",True)
        self.trust_remote_code=config.get("trust_remote_code",True)
        self.local_files_only=config.get("local_files_only",False)
        self.cache_size=max(0,int(config.get("embedding_cache_size",6000)))
        self.trainable=False
        self.training=False
        self._encoder=None
        self._encoder_device=None
        self._embedding_dim=self.truncate_dim
        self._embedding_cache={}
        if not config.get("lazy_load",True):
            self._load_encoder()

    def train(self,mode=True):
        self.training=False
        return self

    def clear_cache(self):
        self._embedding_cache.clear()

    def _load_encoder(self, device=None):
        if device is not None:
            device = torch.device(device)
            if device.type == "cuda" and device.index is None:
                device = torch.device("cuda", torch.cuda.current_device())

        if self._encoder is None:
            from transformers import AutoModel

            model_path = self.local_model_path
            if not model_path or not os.path.isdir(model_path):
                model_path = self.model_name

            encoder = AutoModel.from_pretrained(
                model_path,
                cache_dir=self.cache_dir,
                trust_remote_code=self.trust_remote_code,
                local_files_only=self.local_files_only
            )
            encoder.requires_grad_(False)
            encoder.eval()
            object.__setattr__(self, "_encoder", encoder)
            self._encoder_device = next(encoder.parameters()).device

        if device is not None and self._encoder_device != device:
            self._encoder.to(device)
            self._encoder_device = device

        return self._encoder

    def _encode_texts(self,texts,device,prompt_name):
        encoder=self._load_encoder(device)
        kwargs={"task":self.task}
        if self.truncate_dim is not None:
            kwargs["truncate_dim"]=self.truncate_dim

        values=encoder.encode(texts,prompt_name=prompt_name,max_length=self.max_length,**kwargs)
        values=torch.as_tensor(values,dtype=torch.float32,device=device)
        if self.normalize:
            values=F.normalize(values,dim=-1)
        self._embedding_dim=values.shape[-1]
        return values

    @torch.no_grad()
    def forward(self,texts,attention_mask=None,src_key_padding_mask=None,device=None,prompt_name="document"):
        if torch.is_tensor(texts):
            raise TypeError("JinaTextEncoder expects text strings")

        texts=[texts] if isinstance(texts,str) else list(texts)
        device=device or self._infer_device(attention_mask,src_key_padding_mask)
        device=torch.device(device or self._encoder_device or "cpu")
        if device.type=="cuda" and device.index is None:
            device=torch.device("cuda",torch.cuda.current_device())

        if not texts:
            if self._embedding_dim is None:
                self._encode_texts([""],device,prompt_name)
            return torch.empty((0,self._embedding_dim),device=device,dtype=torch.float32)

        keys=[(prompt_name,text) for text in texts]
        unique=list(dict.fromkeys(keys))
        if self.cache_size==0 or len(unique)>self.cache_size:
            values=self._encode_texts([key[1] for key in unique],device,prompt_name)
            rows={key:index for index,key in enumerate(unique)}
            indices=torch.tensor([rows[key] for key in keys],device=device,dtype=torch.long)
            return values.index_select(0,indices)

        cache=self._embedding_cache.setdefault(device,{"rows":{},"values":None})
        rows=cache["rows"]
        missing=[key for key in unique if key not in rows]
        if len(rows)+len(missing)>self.cache_size:
            rows.clear()
            missing=unique

        if missing:
            values=self._encode_texts([key[1] for key in missing],device,prompt_name)
            if cache["values"] is None:
                cache["values"]=values.new_empty((self.cache_size,values.shape[-1]))

            start=len(rows)
            cache["values"][start:start+len(missing)].copy_(values)
            rows.update((key,start+index) for index,key in enumerate(missing))

        indices=torch.tensor([rows[key] for key in keys],device=device,dtype=torch.long)
        return cache["values"].index_select(0,indices)

    @staticmethod
    def _infer_device(*values):
        for value in values:
            if torch.is_tensor(value):
                return value.device
        return None