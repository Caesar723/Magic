import torch
import torch.nn as nn
import torch.nn.functional as F

from game.rlearning.net.baseNets import AttnPool



class CardBoardEmbed(nn.Module):
    
    
    def __init__(self,config):
        super().__init__()
        self.config=config
        self.embed_dim=config["card_embed_dim"]
        self.card_special_types_embed=nn.Sequential(
            nn.Linear(config["card_special_types_len"],config["cat_emb_dim"]),
            nn.Tanh(),
        )#N*10*20->N*10*16

        # 连续路经：针对 [atk_n, hp_n, has_atk, has_hp, 交互项]
        cont_in = 4+2  # 基本4项 + 交互2项 
        self.cont_mlp = nn.Sequential(
            nn.Linear(cont_in, config["cont_hidden"]),
            nn.Tanh(),
            nn.Linear(config["cont_hidden"], config["id_dim"]),  # 对齐到 id_dim，方便与 ID 融合
            nn.Tanh()
        )#N*10*9->N*10*32

        self.role_embed = nn.Embedding(4, config["role_dim"])
        self.slot_embed = nn.Embedding(12, config["slot_dim"])
        self.fuse_mlp=nn.Sequential(
            nn.Linear(config["cat_emb_dim"]+config["id_dim"]+config["role_dim"]+config["slot_dim"],self.embed_dim),
            nn.Tanh()
        )

        

    def forward(self,card_special_types, atk_n, hp_n, has_atk, has_hp, role, slot):
        special_vec=self.card_special_types_embed(card_special_types)#N*10*16
        atk_n=atk_n.unsqueeze(-1)
        hp_n=hp_n.unsqueeze(-1)
        has_atk=has_atk.unsqueeze(-1)
        has_hp=has_hp.unsqueeze(-1)
        comb1 = atk_n + hp_n
        comb2 = atk_n * hp_n

        cont_vec=self.cont_mlp(torch.cat([atk_n, hp_n,has_atk, has_hp, comb1, comb2], dim=-1).float())
        
        role_vec=self.role_embed(role)
        slot_vec=self.slot_embed(slot)


        head_in=torch.cat([special_vec,cont_vec,role_vec,slot_vec],dim=-1)#N*10*(16+32+16+16)
        head_out=self.fuse_mlp(head_in)#N*10*128
        return head_out

       
class BoardTransformer(nn.Module):
    """
    现成 nn.TransformerEncoder：支持 padding mask
    """
    def __init__(self, config):
        super().__init__()
        layer = nn.TransformerEncoderLayer(
            d_model=config["d_model"], nhead=config["nhead"],
            dim_feedforward=4*config["d_model"], dropout=config["dropout"],
            batch_first=True
        )
        self.encoder = nn.TransformerEncoder(layer, num_layers=config["num_layers"], enable_nested_tensor=False)

        # 可学习 CLS token
        self.cls_param = nn.Parameter(torch.randn(1, 1, config["d_model"]) * 0.02)

        self.attention_pooling=Attention_pooling(config)

    def forward(self, x, pad_mask):
        """
        x:        [B, N, d_model]  # N 应该是 23，但还没拼CLS
        pad_mask: [B, N]  True=该位置是PAD需要屏蔽
        return:
          h_all:     [B, N+1, d_model]  # 含 CLS
          board_repr [B, d_model]       # 取 CLS 输出
        """
        B = x.size(0)
        cls_tok = self.cls_param.expand(B, 1, -1)       # [B,1,d_model]
        x = torch.cat([cls_tok, x], dim=1)              # [B,N+1,d_model]

        # CLS 不是 PAD，拼 False
        pad_mask = torch.cat([torch.zeros(B, 1, dtype=torch.bool, device=x.device), pad_mask], dim=1)

        h_all = self.encoder(x, src_key_padding_mask=pad_mask)  # [B,N+1,d_model]
        board_repr = h_all[:, 0, :]                              # CLS 输出
        tok = h_all[:, 1:, :]
        

        fused=self.attention_pooling(tok,board_repr,pad_mask[:,1:])

        return fused

class Attention_pooling(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config=config
        self.d_model=config["d_model"]

        self.q_proj = nn.Linear(self.d_model, self.d_model)
        self.k_proj = nn.Linear(self.d_model, self.d_model)
        self.v_proj = nn.Linear(self.d_model, self.d_model)

    @staticmethod
    def _ensure_bool_mask(mask: torch.Tensor) -> torch.Tensor:
        # 期望 True=要屏蔽；支持 {bool, byte, float} 输入
        if mask.dtype == torch.bool:
            return mask
        if mask.dtype.is_floating_point:
            return mask > 0.5
        return mask != 0

    def forward(self, token: torch.Tensor,board_repr: torch.Tensor, pad_mask):
        B = token.size(0)
        q = self.q_proj(board_repr).unsqueeze(1)
        k = self.k_proj(token)
        v = self.v_proj(token)

        score = torch.matmul(q, k.transpose(1, 2)).squeeze(1)
        score = score / (k.size(-1) ** 0.5)

        pad_mask = self._ensure_bool_mask(pad_mask).to(score.device)
        score = score.masked_fill(pad_mask, float('-inf'))

        all_masked = pad_mask.all(dim=1)                       # [B]
        if all_masked.any():
            fix_idx = torch.zeros(B, dtype=torch.long, device=score.device)
            score[all_masked, fix_idx[all_masked]] = 0.0       # 让它能 softmax 出一个合法权重

        attn_w = F.softmax(score, dim=-1)          # [B, N]（被 mask 的位置≈0）
        pooled = torch.sum(attn_w.unsqueeze(-1) * v, dim=1)  # [B, d]
        fused = torch.cat([board_repr, pooled], dim=-1)       # [B, 2d]
        return fused
        