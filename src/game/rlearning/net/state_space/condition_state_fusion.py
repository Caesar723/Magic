import torch
import torch.nn as nn


class ConditionStateFusionBlock(nn.Module):
    def __init__(self, d_model=128, nhead=4, dropout=0.1):
        super().__init__()
        self.state_norm = nn.LayerNorm(d_model)
        self.text_norm = nn.LayerNorm(d_model)
        self.output_norm = nn.LayerNorm(d_model)
        self.cross_attention = nn.MultiheadAttention(
            d_model,
            nhead,
            dropout=dropout,
            batch_first=True,
        )
        self.feed_forward = nn.Sequential(
            nn.Linear(d_model, d_model * 4),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(d_model * 4, d_model),
        )

    def forward(self, state_tokens, text_tokens, text_padding):
        query = self.state_norm(state_tokens)
        key_value = self.text_norm(text_tokens)
        context, _ = self.cross_attention(
            query,
            key_value,
            key_value,
            key_padding_mask=text_padding,
            need_weights=False,
        )
        state_tokens = state_tokens + context
        state_tokens = state_tokens + self.feed_forward(
            self.output_norm(state_tokens)
        )
        return state_tokens


class ConditionStateTextFusion(nn.Module):
    def __init__(self, d_model=128, nhead=4, num_layers=2, dropout=0.1):
        super().__init__()
        self.layers = nn.ModuleList([
            ConditionStateFusionBlock(d_model, nhead, dropout)
            for _ in range(num_layers)
        ])
        self.final_norm = nn.LayerNorm(d_model)

    def forward(
        self,
        state_tokens,
        text_tokens,
        state_padding,
        text_padding,
        return_hidden=False,
    ):
        hidden_states = []

        for layer in self.layers:
            state_tokens = layer(
                state_tokens,
                text_tokens,
                text_padding,
            )
            state_tokens = state_tokens.masked_fill(
                state_padding.unsqueeze(-1),
                0.0,
            )
            hidden_states.append(state_tokens)

        state_tokens = self.final_norm(state_tokens)
        state_tokens = state_tokens.masked_fill(
            state_padding.unsqueeze(-1),
            0.0,
        )

        if return_hidden:
            return state_tokens, hidden_states
        return state_tokens