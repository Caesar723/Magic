
import math, torch
import torch.nn as nn
import torch.nn.functional as F



class NoisyLinear(nn.Module):
    def __init__(self, in_features, out_features):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features

        self.weight_mu = nn.Parameter(torch.empty(self.out_features, self.in_features))
        self.weight_sigma = nn.Parameter(torch.empty(self.out_features, self.in_features))
        self.register_buffer('weight_epsilon', torch.empty(self.out_features, self.in_features))

        self.bias_mu = nn.Parameter(torch.empty(self.out_features))
        self.bias_sigma = nn.Parameter(torch.empty(self.out_features))
        self.register_buffer('bias_epsilon', torch.empty(self.out_features))

        self.reset_parameters()
        self.reset_noise()

    def reset_parameters(self):
        mu_range = 1.0 / math.sqrt(self.in_features)
        self.weight_mu.data.uniform_(-mu_range, mu_range)
        self.weight_sigma.data.fill_(0.5 / math.sqrt(self.in_features))
        self.bias_mu.data.uniform_(-mu_range, mu_range)
        self.bias_sigma.data.fill_(0.5 / math.sqrt(self.out_features))

    def _scale_noise(self, size):
        x = torch.randn(size, device=self.weight_mu.device)
        return x.sign().mul_(x.abs().sqrt_())

    def reset_noise(self):
        eps_in = self._scale_noise(self.in_features)
        eps_out = self._scale_noise(self.out_features)
        self.weight_epsilon.copy_(eps_out.ger(eps_in))
        self.bias_epsilon.copy_(eps_out)

    def forward(self, x):
        if self.training:
            weight = self.weight_mu + self.weight_sigma * self.weight_epsilon
            bias = self.bias_mu + self.bias_sigma * self.bias_epsilon
        else:
            weight = self.weight_mu
            bias = self.bias_mu
        return F.linear(x, weight, bias)


class RainbowMLP(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config=config
        self.input_dim=config["input_dim"]
        self.output_dim=config["output_dim"]
        self.atom_size=config["atom_size"]
        self.hidden_dim = self.config["hidden_dim"]
        self.deep = self.config["deep"]
        # 公共特征层
        self.hidden_layer=nn.Sequential(
            nn.Linear(self.input_dim,self.hidden_dim),
            nn.ReLU(),
            *[x for _ in range(self.deep-1) for x in [nn.Linear(self.hidden_dim,self.hidden_dim),nn.ReLU()]],
        )

        # Value stream (dueling 架构)
        self.value_fc = NoisyLinear(self.hidden_dim, self.hidden_dim)
        self.value_out = NoisyLinear(self.hidden_dim, self.atom_size)

        # Advantage stream (dueling 架构)
        self.adv_fc = NoisyLinear(self.hidden_dim, self.hidden_dim)
        self.adv_out = NoisyLinear(self.hidden_dim, self.output_dim * self.atom_size)


    def reset_noise(self):
        self.value_fc.reset_noise()
        self.value_out.reset_noise()
        self.adv_fc.reset_noise()
        self.adv_out.reset_noise()

    def forward(self, x):
        x = self.hidden_layer(x)

        v = F.relu(self.value_fc(x))
        v = self.value_out(v).view(-1, 1, self.atom_size)

        a = F.relu(self.adv_fc(x))
        a = self.adv_out(a).view(-1, self.output_dim, self.atom_size)

        # Dueling 合并
        q_atoms = v + (a - a.mean(dim=1, keepdim=True))
        softmax_q_atoms = F.softmax(q_atoms, dim=-1)
        return softmax_q_atoms  # (batch, action, atom)
