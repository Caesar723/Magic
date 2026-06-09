import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class TextEncoder(nn.Module):
    def __init__(self,config):
        super().__init__()
        self.config=config
        #vocab_size = 49408

        width = config["transformer_width"]
        self.token_embed=nn.Embedding(config["vocab_size"],width)
        

        self.positional_embedding = nn.Parameter(torch.empty(config["context_length"], width))
        nn.init.normal_(self.positional_embedding, std=0.01)

        encoder_layer=nn.TransformerEncoderLayer(
            d_model=width,
            nhead=config["n_heads"],
            dim_feedforward=width*4,
            dropout=config["dropout"],
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )


        
        self.encoder_layers=nn.TransformerEncoder(
            encoder_layer,
            num_layers=config["n_layers"]
        )

        self.ln_final = nn.LayerNorm(config["transformer_width"])
        
    
        self.text_projection = nn.Parameter(
            torch.empty(width, config["embed_dim"])
        )
        nn.init.normal_(self.text_projection, std=width ** -0.5)



    def forward(self, input_ids, src_key_padding_mask=None):
        x = self.token_embed(input_ids)

        batch_size, seq_len = input_ids.shape

        x = x + self.positional_embedding[:seq_len, :].to(
            dtype=x.dtype,
            device=x.device
        )

        causal_mask = self.build_causal_mask(seq_len, x.device)

        x = self.encoder_layers(
            x,
            mask=causal_mask,
            src_key_padding_mask=src_key_padding_mask,
        )

        x = self.ln_final(x)
        eot_indices = input_ids.argmax(dim=-1)
        x = x[torch.arange(batch_size, device=x.device), eot_indices]

        x = x @ self.text_projection
        x = F.normalize(x, dim=-1)
        return x

    def build_causal_mask(self, seq_len, device):
        mask = torch.empty(seq_len, seq_len, device=device)
        mask.fill_(float("-inf"))
        mask.triu_(1)
        return mask

class CardStateEncoder(nn.Module):
    def __init__(self, config):
        super().__init__()

        self.type_embed = nn.Embedding(config["max_card_type"], config["output_dim"])
        self.color_embed = nn.Embedding(config["num_colors"], config["output_dim"])
        self.mana_encoder = nn.Sequential(
            nn.Linear(6, config["output_dim"]),
            nn.LayerNorm(config["output_dim"]),
            nn.GELU(),
            nn.Linear(config["output_dim"], config["output_dim"]),
        )

        self.has_combat_embed = nn.Embedding(2, config["output_dim"])

        self.combat_mlp = nn.Sequential(
            nn.Linear(2, config["output_dim"]),
            nn.GELU(),
            nn.Linear(config["output_dim"], config["output_dim"])
        )

        self.out = nn.Sequential(
            nn.Linear(config["output_dim"] * 5, config["output_dim"]),
            nn.GELU(),
            nn.Linear(config["output_dim"], config["output_dim"])
        )


        


    def forward(self, card_type, color, mana_cost, attack, defense, has_combat):
        type_feat = self.type_embed(card_type)
        color_feat = self.color_embed(color)
        mana_feat = self.mana_encoder(mana_cost.unsqueeze(-1))

        combat_raw = torch.stack([attack, defense], dim=-1)
        combat_feat = self.combat_mlp(combat_raw)

        combat_feat = combat_feat * has_combat.unsqueeze(-1).float()

        has_combat_feat = self.has_combat_embed(has_combat.long())

        x = torch.cat([
            type_feat,
            color_feat,
            mana_feat,
            combat_feat,
            has_combat_feat,
        ], dim=-1)

        return self.out(x)

class ActionEncoder(nn.Module):
    def __init__(self, config):
        super().__init__()

        d = config["output_dim"]

        self.action_embed = nn.Embedding(
            config["action_size"],  # 33
            d
        )

        self.out = nn.Sequential(
            nn.LayerNorm(d),
            nn.Linear(d, d),
            nn.GELU(),
            nn.Linear(d, d),
        )

    def forward(self, action):
        action_feat = self.action_embed(action.long())
        return self.out(action_feat)

if __name__ == "__main__":
    from transformers import CLIPTokenizer
    config = {
        "vocab_size": 49408,
        "context_length": 77,
        "transformer_width": 512,
        "n_heads": 8,
        "n_layers": 6,
        "dropout": 0.1,
        "embed_dim": 512,
    }

    model = TextEncoder(config)

    tokenizer = CLIPTokenizer.from_pretrained(
        "openai/clip-vit-base-patch32"
    )

    text = ""

    tokens = tokenizer(
        text,
        padding="max_length",
        truncation=True,
        max_length=77,
        return_tensors="pt"
    )

    print(tokens["input_ids"].shape)

    print(tokens["input_ids"])
    input_ids = tokens["input_ids"]
    attention_mask = tokens["attention_mask"]
    src_key_padding_mask = attention_mask == 0

    output = model(input_ids, src_key_padding_mask)
    print(output.shape)
    print(output)

