import torch
import torch.nn as nn
import torch.nn.functional as F
import math

if __name__ == "__main__":
    import sys,os
    ORGPATH=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    sys.path.append(ORGPATH)
from game.rlearning.net.baseNets import AttnPool
from game.rlearning.net.RelationTransformer import RelationMultiHeadAttention,RelationTransformerLayer

class HeroEmbed(nn.Module):
    
    def __init__(self,config):
        super().__init__()
        self.config=config
        self.embed_dim=config["token_embed_dim"]
        self.len_life=config["len_life"]
        # 离散 embedding（学习每个血量的语义）
        self.embed = nn.Embedding(self.len_life, self.embed_dim)
        
        # 数值信息（保留大小关系）
        self.num_proj = nn.Linear(1, self.embed_dim)
        
        # 临界状态（关键！）
        self.critical_proj = nn.Linear(1, self.embed_dim)
        
        self.fusion = nn.Linear(self.embed_dim * 3, self.embed_dim)
    
        
    def forward(self,x):
        # embedding
        emb = self.embed(x)  # [B, D]
        
        # 数值（归一化）
        hp_norm = x.float().unsqueeze(-1) / 20.0
        num = self.num_proj(hp_norm)
        
        # 临界特征（低血量敏感）
        critical = (x <= 5).float().unsqueeze(-1)
        crit_feat = self.critical_proj(critical)
        
        return self.fusion(torch.cat([emb, num, crit_feat], dim=-1))
        

class ManaEmbed(nn.Module):
    def __init__(self,config):
        super().__init__()
        self.config=config
        self.embed_dim=config["embed_dim"]
        self.len_mana=config["len_mana"]
        self.max_mana=config["max_mana"]
        self.mana_embed=nn.Embedding(self.max_mana,self.embed_dim)#N*5>N*5*16

        self.num_proj = nn.Linear(1, self.embed_dim)
        self.fusion = nn.Linear(self.embed_dim * 2, self.embed_dim)

    def forward(self,x):
        emb=self.mana_embed(x.long())

        num = self.num_proj(x.float().unsqueeze(-1) / 10.0)
        
        return self.fusion(torch.cat([emb, num], dim=-1))

class CardHandEmbed(nn.Module):
    def __init__(self,config):
        super().__init__()
        self.config=config

        self.embed_dim=config["card_embed_dim"]

        self.card_id_embed=nn.Embedding(config["max_card_id"],config["id_dim"])#N*10->N*10*32
        self.card_type_embed=nn.Embedding(config["max_card_type"],config["type_dim"])#N*10->N*10*16
        self.card_cost_embed=nn.Embedding(config["card_cost_len"],config["mana_dim"])#N*10*6->N*10*6*16

        self.card_special_types_embed=nn.Sequential(
            nn.Linear(config["card_special_types_len"],config["cat_emb_dim"]),
            nn.Tanh(),
        )#N*10*20->N*10*16

        # 连续路经：针对 [mana_n, atk_n, hp_n, has_atk, has_hp, 交互项]
        cont_in = 5 + 4  # 基本5项 + 简单交互4项：atk+hp, atk*hp, atk/mana, (atk+hp)/(mana+eps)
        self.cont_mlp = nn.Sequential(
            nn.Linear(cont_in, config["cont_hidden"]),
            nn.Tanh(),
            nn.Linear(config["cont_hidden"], config["id_dim"]),  # 对齐到 id_dim，方便与 ID 融合
            nn.Tanh()
        )#N*10*9->N*10*32



        self.type_head=nn.ModuleList([
            nn.Sequential(
                nn.Linear(config["id_dim"]+config["type_dim"]+config["mana_dim"]*6+config["cat_emb_dim"],self.embed_dim),
                nn.Tanh()
            )
            for _ in range(config["max_card_type"]+1)
        ])

        self.fuse_mlp=nn.Sequential(
            nn.Linear(self.embed_dim+config["id_dim"],self.embed_dim),
            nn.Tanh()
        )
        
        

        

    def forward(self,card_id, card_type,card_cost, card_special_types, atk_n, hp_n, has_atk, has_hp):
        B,N=card_id.shape
        id_vec=self.card_id_embed(card_id.long())#N*10*32
        type_vec=self.card_type_embed(card_type.long())#N*10*16

        cost_vec=self.card_cost_embed(card_cost.long())
        cost_vec=cost_vec.reshape(B,N,-1)#N*10*(6*16)
        special_vec=self.card_special_types_embed(card_special_types)#N*10*16

        eps=1e-6
        mana_n=card_cost.sum(dim=-1, keepdim=True)
        atk_n=atk_n.unsqueeze(-1)
        hp_n=hp_n.unsqueeze(-1)
        has_atk=has_atk.unsqueeze(-1)
        has_hp=has_hp.unsqueeze(-1)
        comb1 = atk_n + hp_n
        comb2 = atk_n * hp_n
        comb3 = atk_n / (mana_n + eps)
        comb4 = (atk_n + hp_n) / (mana_n + eps)
        cont_vec=self.cont_mlp(torch.cat([mana_n, atk_n, hp_n,has_atk, has_hp, comb1, comb2, comb3, comb4], dim=-1).float())


        
        head_in=torch.cat([id_vec,type_vec,cost_vec,special_vec],dim=-1)#N*10*(32+16+6*16+16)
        all_outs = torch.stack([head_i(head_in) for head_i in self.type_head],dim=2)#4*N*10*128
        
        mask_type = F.one_hot(card_type, num_classes=self.config["max_card_type"]+1).float()
        
        typed_out = torch.sum(mask_type.unsqueeze(-1) * all_outs, dim=2)  # [N*10*128]
        

        fused = self.fuse_mlp(torch.cat([typed_out, cont_vec], dim=-1))#N*10*128
        return fused
        
        
class StatEncoder(nn.Module):
    def __init__(self, embed_dim=32):
        super().__init__()
        self.embed_dim=embed_dim
        self.proj = nn.Linear(embed_dim + 1, embed_dim)
    
    def sinusoidal_encode(self, x):
        """
        x: [B, N]
        return: [B, N, D]
        """

        B, N = x.shape

        # ===== log 压缩 =====
        x_log = torch.log1p(x.float()).unsqueeze(-1)  # [B, N, 1]

        # ===== 频率 =====
        div_term = torch.exp(
            torch.arange(0, self.embed_dim, 2, device=x.device).float()
            * -(math.log(10000.0) / self.embed_dim)
        )  # [D/2]

        # ===== 构造 pe =====
        pe = torch.zeros(B, N, self.embed_dim, device=x.device)  # [B, N, D]

        # broadcasting:
        # x_log: [B, N, 1]
        # div_term: [D/2]
        # → [B, N, D/2]

        pe[..., 0::2] = torch.sin(x_log * div_term)
        pe[..., 1::2] = torch.cos(x_log * div_term)

        return pe, x_log
    
    def forward(self, stat):
        pe, x_log = self.sinusoidal_encode(stat)
        
        # sinusoidal + 原始数值一起输入
        combined = torch.cat([pe, x_log], dim=-1)  # [B, N, 33]
        print("combined.shape:",combined.shape)
        return self.proj(combined)                  # [B, N, 32]

class MinonTokenization(nn.Module):
    def __init__(self,config):
        super().__init__()
        self.config=config
        self.embed_dim=config["token_embed_dim"]
        self.atk_encoder=StatEncoder(self.embed_dim)
        self.hp_encoder=StatEncoder(self.embed_dim)
        
        self.card_special_types_embed=nn.Sequential(
            nn.Linear(config["card_special_types_len"],self.embed_dim),
            nn.Tanh(),
        )#N*10*20->N*10*16

        self.fusion = nn.Linear(self.embed_dim * 3, self.embed_dim)

        

    def forward(self,card_special_types,atk_n, hp_n):
        special_vec=self.card_special_types_embed(card_special_types)#N*10*16
        attack_embedding=self.atk_encoder(atk_n)
        hp_embedding=self.hp_encoder(hp_n)

        fused = self.fusion(torch.cat([special_vec,attack_embedding, hp_embedding], dim=-1))
        return fused
        
        

class CardBoardEmbed(nn.Module):
    
    
    def __init__(self,config):
        super().__init__()
        self.config=config
        
        self.token_embed_dim=config["token_embed_dim"]
        self.num_heads=config["num_heads"]
        self.num_layers=config["num_layers"]
        self.embed_dim=config["card_embed_dim"]
        self.max_tokens=config["max_tokens"]

        self.side_embed = nn.Embedding(2, self.token_embed_dim)
        self.minon_tokenization=MinonTokenization(config)
        self.cls = nn.Parameter(torch.randn(1, 1, self.token_embed_dim))

        self.layers = nn.ModuleList([
            RelationTransformerLayer(self.token_embed_dim, self.num_heads)
            for _ in range(self.num_layers)
        ])

        self.hero_hp_encoder=HeroEmbed(self.config)
        self.enemy_hp_encoder=HeroEmbed(self.config)

    def forward(self,
        hero_hp,
        enemy_hp,
        card_special_types, 
        atk_n, 
        hp_n,
        side,
        relation_graph,
        valid_mask
    ):
        
        # ===== 1. tokenization =====
        tokens = self.minon_tokenization(
            card_special_types, atk_n, hp_n
        ) 
        
        tokens+=self.side_embed(side.long())
        hero_hp_embedding=self.hero_hp_encoder(hero_hp)
        enemy_hp_embedding=self.enemy_hp_encoder(enemy_hp)
        hero_hp_embedding = hero_hp_embedding  # [B,1,D]
        enemy_hp_embedding = enemy_hp_embedding  # [B,1,D]

        tokens=torch.cat([hero_hp_embedding,enemy_hp_embedding,tokens],dim=-2)

        B, N, D = tokens.shape


        # ===== 2. CLS =====
        cls_token = self.cls.expand(B, 1, D)
        x = torch.cat([cls_token, tokens], dim=1)  # [B, N+1, D]

        # ===== 3. mask =====
        cls_mask = torch.ones(B, 1, device=tokens.device)
        hero_mask = torch.ones(B, 2, device=tokens.device)
        valid_mask = torch.cat([cls_mask, hero_mask, valid_mask], dim=1)


        padding_mask = ~valid_mask.bool()
        # ===== graph bias =====
        cls_pad = torch.zeros(B, 1, relation_graph.shape[-1], device=relation_graph.device)
        relation_graph = torch.cat([cls_pad, relation_graph], dim=1)

        cls_pad = torch.zeros(B, relation_graph.shape[1], 1, device=relation_graph.device)
        relation_graph = torch.cat([cls_pad, relation_graph], dim=2)
        attn_bias = self.build_attention_bias(relation_graph, valid_mask)
        # ===== 4. Transformer =====
        for layer in self.layers:
            x = layer(x, padding_mask, attn_bias)

        board_vec = x[:, 0]
        minion_context = x[:, 1:]
        return board_vec, minion_context

    def build_attention_bias(self, relation_graph, valid_mask):
        """
        relation_graph: [B, N, N]
        valid_mask: [B, N]
        """

        B, N, _ = relation_graph.shape

        
        # ===== bias 初始化 =====
        bias = torch.zeros(B, N, N, device=relation_graph.device)

        # 可以交互的：强关注
        bias = bias + relation_graph.float() * 0.2

        # ===== padding 屏蔽 =====
        valid_i = valid_mask.unsqueeze(2).bool()
        valid_j = valid_mask.unsqueeze(1).bool()

        valid_pair = valid_i & valid_j

        bias = bias.masked_fill(~valid_pair, float('-inf'))

        return bias



class HandEmbed(nn.Module): 
    
    def __init__(self,config):
        super().__init__()
        self.config=config
        print(config)
        self.card_hand_embed=CardHandEmbed(config)
        self.attn_pool=AttnPool(config["card_embed_dim"])
        self.head = nn.Sequential(
            nn.Linear(10*(config["card_embed_dim"] + config["card_embed_dim"] if config.get("use_attn_pool",True) else 0), config["card_embed_dim"]),
            nn.Tanh(),
            
        )


    def forward(self,card_id, card_type,card_cost, card_special_types, atk_n, hp_n, has_atk, has_hp,mask):
        
        card_hand_embed=self.card_hand_embed(card_id, card_type,card_cost, card_special_types, atk_n, hp_n, has_atk, has_hp)
        
        if self.config.get("use_attn_pool",True):
            B, N = card_id.shape
            
            ctx=self.attn_pool(card_hand_embed,mask)#N*128
            ctx_exp = ctx.unsqueeze(1).expand(B, N, ctx.shape[-1])
            x = torch.cat([card_hand_embed,ctx_exp],dim=-1)
        else:
            x = card_hand_embed
        x=x.view(x.size(0),-1)
        return self.head(x)




class ActionEmbed(nn.Module):
    def __init__(self,config):
        super().__init__()
        self.config=config
        self.head = nn.Embedding(config["action_dim"],config["action_embed_dim"])#N*5>N*5*16
    def forward(self,x):
        x=self.head(x)
        return x



class HistoryEmbed(nn.Module):
    def __init__(self,config):
        super().__init__()
        self.config=config
        self.lstm = nn.LSTM(config["history_dim"], config["history_embed_dim"], batch_first=True)
        
    def forward(self,x):
        x, (h, c) = self.lstm(x)
        
        return x


if __name__ == "__main__":
    config = {
        "token_embed_dim": 128,
        "num_heads": 4,
        "num_layers": 2,
        "card_embed_dim": 128,
        "max_tokens": 10,
        "card_special_types_len": 20,
        "len_life": 21,
    }

    # ===== 创建模型 =====
    model = CardBoardEmbed(config)

    # ===== 构造假数据 =====
    B = 2
    N = 15   
    M = 20# max_tokens

    hero_hp = torch.randint(1, 20, (B,1))
    enemy_hp = torch.randint(1, 20, (B,1))

    card_special_types = torch.randn(B, N, 20)
    atk_n = torch.randint(0, 10, (B, N))
    hp_n = torch.randint(0, 10, (B, N))
    side = torch.randint(0, 2, (B, N))

    card_special_types_padding=torch.zeros(B, M, 20)
    card_special_types_padding[:,:N]=card_special_types

    atk_n_padding=torch.zeros(B, M)
    atk_n_padding[:,:N]=atk_n

    hp_n_padding=torch.zeros(B, M)
    hp_n_padding[:,:N]=hp_n

    side_padding=torch.zeros(B, M)
    side_padding[:,:N]=side
    


    mask=torch.zeros(B, M)
    mask[:,:N]=1

    

    print(hero_hp.shape, enemy_hp.shape)
    print(card_special_types.shape, atk_n.shape, hp_n.shape)
    print(side.shape)
    print(card_special_types_padding.shape, atk_n_padding.shape, hp_n_padding.shape, side_padding.shape)
    

    # ===== relation graph =====
    relation_graph = torch.randint(0, 2, (B, M+2, M+2))  # ⚠️注意 +2（hero）

    # ===== forward =====
    board_vec, minion_context = model(
        hero_hp,
        enemy_hp,
        card_special_types_padding,
        atk_n_padding,
        hp_n_padding,
        side_padding,
        relation_graph,
        mask
    )

    # ===== 打印结果 =====
    print("board_vec shape:", board_vec.shape)
    print("minion_context shape:", minion_context.shape)