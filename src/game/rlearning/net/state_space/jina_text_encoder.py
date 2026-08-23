import os
from transformers import AutoModel

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
        self.max_length = config.get("max_length")
        self.normalize = config.get("normalize", True)
        self.trust_remote_code = config.get("trust_remote_code", True)
        self.local_files_only = config.get("local_files_only", False)
        # Default False: frozen encoder (current behavior).
        self.trainable = config.get("trainable", False)

        self._encoder = None
        self._encoder_device = None

        # A trainable encoder must be registered before ModelTrainer creates
        # its optimizer. Frozen encoders can still keep lazy loading.
        if self.trainable or not config.get("lazy_load", True):
            self._load_encoder()

    def _apply_trainability(self, encoder):
        if self.trainable:
            encoder.requires_grad_(True)
            encoder.train(self.training)
        else:
            encoder.requires_grad_(False)
            encoder.eval()

    def _load_encoder(self, device=None):
        if self._encoder is None:
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
            self._apply_trainability(encoder)
            if self.trainable:
                # Register as submodule so parameters appear in self.parameters().
                self._encoder = encoder
            else:
                # Keep out of the module tree (frozen feature extractor).
                object.__setattr__(self, "_encoder", encoder)

        if device is not None and self._encoder_device != device:
            self._encoder.to(device)
            self._encoder_device = device

        return self._encoder

    def train(self, mode=True):
        super().train(mode)
        if self._encoder is not None:
            self._apply_trainability(self._encoder)
        return self

    def forward(
        self,
        texts,
        attention_mask=None,
        src_key_padding_mask=None,
        device=None,
        prompt_name="document",
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

        if self.trainable:
            embeddings = self._encode_with_grad(
                encoder,
                texts,
                device=device,
                prompt_name=prompt_name,
            )
        else:
            with torch.no_grad():
                embeddings = encoder.encode(
                    texts,
                    prompt_name=prompt_name,
                    max_length=self.max_length,
                    **encode_kwargs,
                )

        if not isinstance(embeddings, torch.Tensor):
            embeddings = torch.as_tensor(embeddings, dtype=torch.float32)

        if device is not None:
            embeddings = embeddings.to(device=device, dtype=torch.float32)
        else:
            embeddings = embeddings.to(dtype=torch.float32)

        if self.normalize:
            embeddings = F.normalize(embeddings, dim=-1)

        return embeddings

    def _encode_with_grad(self, encoder, texts, device, prompt_name):
        """Run Jina's embedding steps without its inference-only ``encode``."""
        if device is None:
            device = next(encoder.parameters()).device

        prefix = "Query: " if prompt_name == "query" else "Document: "
        token_kwargs = {
            "return_tensors": "pt",
            "padding": True,
            "truncation": True,
        }
        if self.max_length is not None:
            token_kwargs["max_length"] = int(self.max_length)

        token_batch = encoder.tokenizer(
            [f"{prefix}{text}" for text in texts],
            **token_kwargs,
        )
        token_batch = {
            key: value.to(device)
            for key, value in token_batch.items()
        }

        encoder.set_adapter([self.task])
        outputs = encoder(**token_batch)
        hidden = outputs.last_hidden_state
        token_mask = token_batch.get("attention_mask")
        if token_mask is None:
            embeddings = hidden[:, -1]
        else:
            last_token = token_mask.sum(dim=1) - 1
            embeddings = hidden[
                torch.arange(hidden.shape[0], device=hidden.device),
                last_token,
            ]

        if self.truncate_dim is not None:
            embeddings = embeddings[:, : self.truncate_dim]
        return embeddings

    @staticmethod
    def _infer_device(*values):
        for value in values:
            if isinstance(value, torch.Tensor):
                return value.device
        return None
