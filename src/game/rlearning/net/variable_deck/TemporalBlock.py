import torch
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence,pad_packed_sequence

class LSTMBlock(nn.Module):
    def __init__(self,config):
        super().__init__()
        self.config=config
        self.input_dim=config["input_dim"]
        self.hidden_dim=config["hidden_dim"]
        self.lstm=nn.LSTM(
            input_size=self.input_dim,
            hidden_size=self.hidden_dim,
            batch_first=True
        )

    def forward(self,x,lengths,state=None):
        # x: [B,T,input_dim]
        # lengths: [B]
        # state: (h,c)
        lengths=torch.as_tensor(lengths,dtype=torch.long).cpu()
        packed_x=pack_padded_sequence(x,lengths,batch_first=True,enforce_sorted=False)
        packed_output,state=self.lstm(packed_x,state)
        output,_=pad_packed_sequence(packed_output,batch_first=True,total_length=x.shape[1])
        return output,state
