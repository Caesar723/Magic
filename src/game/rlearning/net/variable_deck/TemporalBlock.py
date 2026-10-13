import torch
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence

class LSTMBlock(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config=config
        self.input_dim=config["input_dim"]
        self.hidden_dim=config["hidden_dim"]
        self.max_seq_len = config["max_seq_len"]
        self.lstm = nn.LSTM(
            input_size=self.input_dim,
            hidden_size=self.hidden_dim,
            batch_first=True
        )
    def forward(self, x,lengths):
        # x: [B, T, input_dim]
        # lengths: [B]
        lengths = torch.as_tensor(lengths, dtype=torch.long).cpu()

        packed_x = pack_padded_sequence(
            x,
            lengths,
            batch_first=True,
            enforce_sorted=False
        )
        output, (h, c) = self.lstm(packed_x)
        
        return h[-1]