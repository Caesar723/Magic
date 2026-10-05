from torch import nn
import torch

from game.rlearning.net.state_space.CVAE_residual import PosteriorEncoder
from game.rlearning.synthesis.entity_transition import align_entity_transitions



def _field_changed(source_value, target_value, atol=1e-6):
    if source_value.is_floating_point():
        changed = ~torch.isclose(
            source_value,
            target_value,
            atol=atol,
            rtol=0.0,
        )
    else:
        changed = source_value != target_value

    if changed.ndim > 2:
        changed = changed.flatten(start_dim=2).any(dim=-1)
    return changed

@torch.no_grad()
def build_existing_change_targets(source, next_state, alignment=None):
    """source/next -> changed_mask and existing_count and birth_count."""
    alignment = alignment or align_entity_transitions(source, next_state)
    source_entities, aligned_next, _, birth_mask = alignment

    source_valid = source_entities["card_mask"].bool()
    matched = aligned_next["matched"].bool()

    disappeared = source_valid & ~matched

    moved = matched&(source_entities["zone_indices"]!=aligned_next["destination_zone"])

    attribute_changed = torch.zeros_like(source_valid)
    for field in ("card_types","card_costs","card_color_identity","card_special_types","card_atks","card_hps","card_has_state","card_tapped","card_tapped_valid","card_is_attacker"):
        attribute_changed |= matched & _field_changed(source_entities[field],aligned_next[field])


    changed_mask = source_valid & (disappeared | moved | attribute_changed)
    existing_count = changed_mask.sum(dim=-1).long()

    birth_count = birth_mask.sum(dim=-1).long()

    return changed_mask, existing_count, birth_count

def strict_topk_mask(selection_logits, counts, padding_mask):
    """K -> selected_mask."""
    batch_size, entity_count = selection_logits.shape
    device = selection_logits.device

    counts = counts.to(device=device,dtype=torch.long).reshape(batch_size)

    padding_mask = padding_mask.to(device=device,dtype=torch.bool)
    valid_mask = ~padding_mask
    valid_counts = valid_mask.sum(dim=-1)

    effective_counts = torch.minimum(counts.clamp_min(0),valid_counts)

    masked_logits = selection_logits.masked_fill(padding_mask,float("-inf"))

    sorted_indices = masked_logits.argsort(dim=-1,descending=True)

    ranks = torch.empty_like(sorted_indices)
    rank_values = torch.arange(entity_count,device=device,dtype=torch.long).unsqueeze(0).expand(batch_size, -1)
    ranks.scatter_(dim=-1,index=sorted_indices,src=rank_values)

    selected_mask =(ranks < effective_counts.unsqueeze(-1)) & valid_mask
    return selected_mask

class ExistingTransitionSupportEncoder(nn.Module):
    """source_entity_tokens + changed_mask + existing_count -> existing_support"""

    def __init__(self,d_model=128,max_count=128):
        super().__init__()
        self.d_model = d_model
        self.max_count = max_count

        self.entity_proj = nn.Sequential(
            nn.RMSNorm(d_model),
            nn.Linear(d_model, d_model),
            nn.GELU(),
        )

        self.count_embedding = nn.Embedding(max_count + 1,d_model)

        self.no_change_embedding = nn.Parameter(torch.empty(1, d_model))
        nn.init.normal_(self.no_change_embedding,std=0.02,mean=0.0)

        self.output = nn.Sequential(
            nn.Linear(d_model * 2, d_model * 2),
            nn.GELU(),
            nn.RMSNorm(d_model * 2),
            nn.Linear(d_model * 2, d_model),
            nn.RMSNorm(d_model),
        )

    def forward(self,entity_tokens,changed_mask,padding_mask):

        valid_changed_mask=changed_mask&~padding_mask

        existing_count=valid_changed_mask.sum(dim=-1).long()

        encoded_entities=self.entity_proj(entity_tokens)
        pooling_weights = valid_changed_mask.unsqueeze(-1).to(encoded_entities.dtype)
        changed_sum = (encoded_entities * pooling_weights).sum(dim=1)

        denominator= existing_count.clamp_min(1).unsqueeze(-1)

        changed_summary=changed_sum/denominator


        count_indices = existing_count.clamp(min=0,max=self.max_count)
        count_summary = self.count_embedding(count_indices)


        combined = torch.cat([changed_summary,count_summary],dim=-1)

        existing_support = self.output(combined)

        return existing_support
        

class BirthTransitionSupportEncoder(nn.Module):
    """birth_count -> birth_support"""

    def __init__(self,d_model=128,max_birth_count=10):
        super().__init__()
        self.d_model = d_model
        self.max_birth_count = max_birth_count

        self.count_embedding = nn.Embedding(max_birth_count + 1,d_model)

        self.output = nn.Sequential(
            nn.RMSNorm(d_model),
            nn.Linear(d_model, d_model * 2),
            nn.GELU(),
            nn.Linear(d_model * 2, d_model),
            nn.RMSNorm(d_model),
        )

    def forward(self,birth_count):
        count_indices = birth_count.clamp(min=0,max=self.max_birth_count)
        count_summary = self.count_embedding(count_indices)
        birth_support = self.output(count_summary)
        return birth_support

class TransitionSupportEncoder(nn.Module):
    """existing_support + birth_support -> transition_summary"""

    def __init__(self, d_model=128):
        super().__init__()

        self.d_model = d_model

        self.existing_norm = nn.RMSNorm(d_model)
        self.birth_norm = nn.RMSNorm(d_model)

        self.fusion = nn.Sequential(
            nn.Linear(d_model * 2, d_model * 2),
            nn.GELU(),
            nn.RMSNorm(d_model * 2),
            nn.Linear(d_model * 2, d_model),
            nn.RMSNorm(d_model),
        )
    def forward(self,existing_support,birth_support):
        existing_support = self.existing_norm(existing_support)
        birth_support = self.birth_norm(birth_support)
        combined = torch.cat([existing_support,birth_support],dim=-1)
        transition_summary = self.fusion(combined)
        return transition_summary

class ExistingTransitionCountHead(nn.Module):
    """state/card/action , z_q -> count logits"""

    def __init__(self,d_model=128,latent_dim=128,max_count=160):
        super().__init__()

        self.plan_proj = nn.Sequential(nn.RMSNorm(d_model), nn.Linear(d_model, d_model))
        self.z_proj = nn.Sequential(nn.RMSNorm(latent_dim), nn.Linear(latent_dim, d_model), nn.GELU())
        self.output = nn.Sequential(
            nn.Linear(d_model * 3, d_model * 2),
            nn.GELU(),
            nn.RMSNorm(d_model * 2),
            nn.Linear(d_model * 2, max_count + 1),
        )

    def forward(self,plans,z):
        plan = self.plan_proj(plans).mean(dim=1)  # [B,4,D] -> [B,D]
        latent = self.z_proj(z)
        return self.output(torch.cat([plan, latent, plan * latent], dim=-1))

class BirthCountHead(ExistingTransitionCountHead):
    """state/card/action , z_q -> birth_count logits"""
    def __init__(self,d_model=128,latent_dim=128,max_birth_count=10):
        super().__init__(d_model=d_model,latent_dim=latent_dim,max_count=max_birth_count)

class LatentEntitySelector(nn.Module):
    """entity_tokens + condition + z -> selection logits"""

    def __init__(self,d_model=128,latent_dim=32):
        super().__init__()

        self.scale = d_model ** -0.5
        self.plan_proj = nn.Sequential(
            nn.RMSNorm(d_model), 
            nn.Linear(d_model, d_model)
        )
        self.z_proj = nn.Sequential(
            nn.RMSNorm(latent_dim), 
            nn.Linear(latent_dim, d_model), 
            nn.GELU()
        )
        self.query_proj = nn.Sequential(
            nn.Linear(d_model * 3, d_model * 2),
            nn.GELU(),
            nn.RMSNorm(d_model * 2),
            nn.Linear(d_model * 2, d_model),
            nn.RMSNorm(d_model),
        )
        self.entity_proj = nn.Sequential(
            nn.RMSNorm(d_model), 
            nn.Linear(d_model, d_model)
        )

    
    def forward(self,entity_tokens, plans, z, padding_mask):
        plan = self.plan_proj(plans).mean(dim=1)
        latent = self.z_proj(z)
        query = self.query_proj(torch.cat([plan, latent, plan * latent], dim=-1))
        keys = self.entity_proj(entity_tokens)
        logits = (keys * query.unsqueeze(1)).sum(dim=-1) * self.scale
        return logits.masked_fill(padding_mask, float("-inf"))


class TransitionSupportPosteriorEncoder(nn.Module):
    """state/card/action , transition_support_summary -> z_p"""

    def __init__(self,config):
        super().__init__()

        self.d_model = int(config.get("d_model", 128))
        self.latent_dim = int(config.get("latent_dim", 32))
        self.max_existing_count = int(config.get("max_existing_count", 128))
        self.max_birth_count = int(config.get("max_birth_count", 10))

        self.existing_transition_support_encoder = ExistingTransitionSupportEncoder(
            d_model=self.d_model,
            max_count=self.max_existing_count,
        )
        self.birth_transition_support_encoder = BirthTransitionSupportEncoder(
            d_model=self.d_model,
            max_birth_count=self.max_birth_count,
        )
        self.transition_support_encoder = TransitionSupportEncoder(
            d_model=self.d_model,
        )


        self.posterior_encoder = PosteriorEncoder(config)

    def forward(self,h_card,h_action,h_state,entity_tokens,changed_mask,entity_padding_mask,birth_count):

        existing_support = self.existing_transition_support_encoder(entity_tokens,changed_mask,entity_padding_mask)
        birth_support = self.birth_transition_support_encoder(birth_count)
        transition_support = self.transition_support_encoder(existing_support,birth_support)
        mean_q, std_q  = self.posterior_encoder(h_card,h_action,h_state,transition_support)
        return mean_q, std_q
