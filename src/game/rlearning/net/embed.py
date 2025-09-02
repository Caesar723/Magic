import torch
import torch.nn as nn
import torch.nn.functional as F


from game.rlearning.net.baseNets import AttnPool

class HeroEmbed(nn.Module):
    
    def __init__(self,config):
        super().__init__()
        self.config=config
        self.embed_dim=config["embed_dim"]
        self.len_life=config["len_life"]
        self.hero_embed=nn.Sequential(
            nn.Linear(self.len_life,self.embed_dim),
            nn.Tanh(),
        )
        
    def forward(self,x):
        return self.hero_embed(x)#N*21->N*16
        

class ManaEmbed(nn.Module):
    def __init__(self,config):
        super().__init__()
        self.config=config
        self.embed_dim=config["embed_dim"]
        self.len_mana=config["len_mana"]
        self.mana_embed=nn.Embedding(self.len_mana,self.embed_dim)#N*5>N*5*16

        self.mana_mlp=nn.Sequential(
            nn.Linear(self.len_mana*self.embed_dim,self.embed_dim),
            nn.Tanh(),
        )

    def forward(self,x):
        x=self.mana_embed(x.long())
        x=x.view(x.size(0),-1)
        x=self.mana_mlp(x)
        return x#N*6->N*16

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

        self.fuse_mlp=nn.Sequential(
            nn.Linear(config["cat_emb_dim"]+config["id_dim"],self.embed_dim),
            nn.Tanh()
        )

    def forward(self,card_special_types, atk_n, hp_n, has_atk, has_hp):
        special_vec=self.card_special_types_embed(card_special_types)#N*10*16
        atk_n=atk_n.unsqueeze(-1)
        hp_n=hp_n.unsqueeze(-1)
        has_atk=has_atk.unsqueeze(-1)
        has_hp=has_hp.unsqueeze(-1)
        comb1 = atk_n + hp_n
        comb2 = atk_n * hp_n

        cont_vec=self.cont_mlp(torch.cat([atk_n, hp_n,has_atk, has_hp, comb1, comb2], dim=-1).float())
        

        head_in=torch.cat([special_vec,cont_vec],dim=-1)#N*10*(16+32)
        head_out=self.fuse_mlp(head_in)#N*10*128
        return head_out



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

class BoardEmbed(nn.Module):
    def __init__(self,config):
        super().__init__()
        self.config=config
        self.card_board_embed=CardBoardEmbed(config)
        self.attn_pool=AttnPool(config["card_embed_dim"])
        self.head = nn.Sequential(
            nn.Linear(10*(config["card_embed_dim"] + (config["card_embed_dim"] if config.get("use_attn_pool",True) else 0)), config["card_embed_dim"]),
            nn.Tanh(),
        )
    def forward(self,card_special_types, atk_n, hp_n, has_atk, has_hp,mask):
        card_board_embed=self.card_board_embed(card_special_types, atk_n, hp_n, has_atk, has_hp)
        if self.config.get("use_attn_pool",True):
            B, N, D = card_board_embed.shape
            ctx=self.attn_pool(card_board_embed,mask)#N*128
            ctx_exp = ctx.unsqueeze(1).expand(B, N, ctx.shape[-1])
            x = torch.cat([card_board_embed,ctx_exp],dim=-1)
        else:
            x = card_board_embed
        x=x.view(x.size(0),-1)
        return self.head(x)

    

    





