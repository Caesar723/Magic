import os

import torch
import torch.nn as nn
import torch.nn.functional as F


class JinaTextEncoder(nn.Module):
    def __init__(self, config):
        super().__init__()

        self.model_name = config.get(
            "model_name",
            "jinaai/jina-embeddings-v5-text-small",
        )
        self.local_model_path = config.get("local_model_path")
        self.cache_dir = config.get("cache_dir")
        self.task = config.get("task", "text-matching")
        self.truncate_dim = config.get("truncate_dim", 128)
        self.normalize = config.get("normalize", True)
        self.trust_remote_code = config.get("trust_remote_code", True)
        self.local_files_only = config.get("local_files_only", False)

        self._encoder = None
        self._encoder_device = None

        if not config.get("lazy_load", True):
            self._load_encoder()

    def _load_encoder(self, device=None):
        if self._encoder is None:
            from transformers import AutoModel

            model_path = (
                self.local_model_path
                if self.local_model_path and os.path.isdir(self.local_model_path)
                else self.model_name
            )
            encoder = AutoModel.from_pretrained(
                model_path,
                cache_dir=self.cache_dir,
                trust_remote_code=self.trust_remote_code,
                local_files_only=self.local_files_only,
            )
            encoder.eval()
            encoder.requires_grad_(False)
            object.__setattr__(self, "_encoder", encoder)

        if device is not None and self._encoder_device != device:
            self._encoder.to(device)
            self._encoder_device = device

        return self._encoder

    def forward(
        self,
        texts,
        attention_mask=None,
        src_key_padding_mask=None,
        device=None,
    ):
        if isinstance(texts, torch.Tensor):
            raise TypeError(
                "JinaTextEncoder expects raw text strings, not token ids. "
                "Set CVAEDataset to keep card_used.description as raw text."
            )

        if isinstance(texts, str):
            texts = [texts]
        else:
            texts = list(texts)

        if device is None:
            device = self._infer_device(attention_mask, src_key_padding_mask)

        encoder = self._load_encoder(device=device)

        encode_kwargs = {"task": self.task}
        if self.truncate_dim is not None:
            encode_kwargs["truncate_dim"] = self.truncate_dim

        with torch.no_grad():
            embeddings = encoder.encode(texts, **encode_kwargs)

        if not isinstance(embeddings, torch.Tensor):
            embeddings = torch.as_tensor(embeddings, dtype=torch.float32)

        if device is not None:
            embeddings = embeddings.to(device=device, dtype=torch.float32)
        else:
            embeddings = embeddings.to(dtype=torch.float32)

        if self.normalize:
            embeddings = F.normalize(embeddings, dim=-1)

        return embeddings

    @staticmethod
    def _infer_device(*values):
        for value in values:
            if isinstance(value, torch.Tensor):
                return value.device
        return None
