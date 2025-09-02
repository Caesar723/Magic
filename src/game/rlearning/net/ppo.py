

import torch
import torch.nn as nn


class Actor(nn.Module):
    
    def __init__(self,config):
        super().__init__()
        self.config=config
        self.input_dim=config["input_dim"]
        self.hidden_dim=config["hidden_dim"]
        self.output_dim=config["output_dim"]
        
        self.actor=nn.Sequential(
            nn.Linear(self.input_dim,self.hidden_dim),
            nn.Tanh(),
            nn.Linear(self.hidden_dim,self.hidden_dim),
            nn.Tanh(),
            nn.Linear(self.hidden_dim,self.output_dim),
            nn.Softmax(dim=-1)
        )
    def forward(self,x):
        return self.actor(x)


class Critic(nn.Module):
    def __init__(self,config):
        super().__init__()
        self.config=config
        self.input_dim=config["input_dim"]
        self.hidden_dim=config["hidden_dim"]
        self.output_dim=config["output_dim"]
        self.critic=nn.Sequential(
            nn.Linear(self.input_dim,self.hidden_dim),
            nn.Tanh(),
            nn.Linear(self.hidden_dim,self.hidden_dim),
            nn.Tanh(),
            nn.Linear(self.hidden_dim,self.output_dim),
            
        )
    def forward(self,x):
        return self.critic(x)

