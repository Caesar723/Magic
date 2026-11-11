import os
import torch
import torch.nn as nn
from transformers import AutoModel, AutoTokenizer


class ConditionJinaTokenEncoder(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.model_name = config.get("model_name")
        self.local_model_path = config.get("local_model_path")
        self.cache_dir = config.get("cache_dir")
        self.task = config.get("task", "text-matching")
        self.max_length = config.get("max_length")
        self.local_files_only = config.get("local_files_only", False)
        self._encoder = None
        self._tokenizer = None
        self._encoder_device = None

    def _load_encoder(self, device):
        if self._encoder is None:
            model_path = self.local_model_path if (
                self.local_model_path and os.path.isdir(self.local_model_path)
            ) else self.model_name
            encoder = AutoModel.from_pretrained(
                model_path,
                cache_dir=self.cache_dir,
                local_files_only=self.local_files_only,
                trust_remote_code=True,
            )
            tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                cache_dir=self.cache_dir,
                local_files_only=self.local_files_only,
                trust_remote_code=True,
            )
            encoder.requires_grad_(False)
            encoder.eval()
            object.__setattr__(self, "_encoder", encoder)
            object.__setattr__(self, "_tokenizer", tokenizer)

        if self._encoder_device != device:
            self._encoder.to(device)
            self._encoder_device = device

        return self._encoder, self._tokenizer

    @torch.no_grad()
    def forward(self, texts, device=None):
        texts = [texts] if isinstance(texts, str) else list(texts)
        device = device or torch.device("cpu")
        encoder, tokenizer = self._load_encoder(device)

        inputs = tokenizer(
            ["Document: " + text for text in texts],
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=self.max_length,
        )
        inputs = {key: value.to(device) for key, value in inputs.items()}

        if hasattr(encoder, "set_adapter"):
            encoder.set_adapter([self.task])

        hidden = encoder(**inputs).last_hidden_state.float()
        attention_mask = inputs["attention_mask"].bool()
        padding_mask = ~attention_mask
        last_index = attention_mask.sum(dim=1).long().sub(1).clamp_min(0)
        batch_index = torch.arange(hidden.shape[0], device=device)
        pooled = hidden[batch_index, last_index]

        return pooled, hidden, padding_mask


class ConditionTextProjection(nn.Module):
    def __init__(self, input_dim=1024, d_model=128):
        super().__init__()
        self.projection = nn.Sequential(
            nn.Linear(input_dim, d_model),
            nn.LayerNorm(d_model),
            nn.GELU(),
            nn.Linear(d_model, d_model),
        )

    def forward(self, value):
        return self.projection(value)