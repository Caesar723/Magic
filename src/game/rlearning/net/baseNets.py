import torch
import torch.nn as nn
import torch.nn.functional as F





class AttnPool(nn.Module):
    def __init__(self, d):
        super().__init__()
        self.q = nn.Parameter(torch.randn(d))  # 可学习的查询向量
        self.proj = nn.Linear(d, d)

    def forward(self, card_vecs, mask):
        # card_vecs: [B, N, D]
        B, N, D = card_vecs.shape

        # 投影到同一空间
        k = self.proj(card_vecs)  # [B, N, D]

        # 打分： q · k
        att = torch.matmul(k, self.q)  # [B, N]

        # 屏蔽掉 padding
        att = att.masked_fill(mask == 0, -1e9)

        # softmax 得到注意力权重
        w = F.softmax(att, dim=-1).unsqueeze(-1)  # [B, N, 1]

        # 加权求和
        hand_vec = (w * card_vecs).sum(dim=1)  # [B, D]

        return hand_vec

class Dense(nn.Module):
    def __init__(self,d_in,d_out):
        super().__init__()
        self.fc=nn.Linear(d_in,d_out)
    def forward(self,x):
        x=self.fc(x)
        return x