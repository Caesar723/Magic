import torch
import torch.nn as nn
import torch.nn.functional as F
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

    def forward_step(self,x,state=None):
        if state is None:
            h=x.new_zeros((1,x.shape[0],self.hidden_dim))
            c=torch.zeros_like(h)
        else:
            h,c=state

        layer=self.lstm
        gates=F.linear(x[:,0],layer.weight_ih_l0,layer.bias_ih_l0)
        gates=gates+F.linear(h[0],layer.weight_hh_l0,layer.bias_hh_l0)
        input_gate,forget_gate,cell_gate,output_gate=gates.chunk(4,dim=-1)
        cell=forget_gate.sigmoid()*c[0]+input_gate.sigmoid()*cell_gate.tanh()
        hidden=output_gate.sigmoid()*cell.tanh()
        return hidden.unsqueeze(1),(hidden.unsqueeze(0),cell.unsqueeze(0))

    def forward(self,x,lengths,state=None):
        if not self.training and x.shape[1]==1:
            return self.forward_step(x,state)

        lengths=torch.as_tensor(lengths,dtype=torch.long).cpu()
        packed_x=pack_padded_sequence(x,lengths,batch_first=True,enforce_sorted=False)
        packed_output,state=self.lstm(packed_x,state)
        output,_=pad_packed_sequence(packed_output,batch_first=True,total_length=x.shape[1])
        return output,state
