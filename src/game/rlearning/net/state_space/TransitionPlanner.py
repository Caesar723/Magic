"""State-conditioned deterministic transition-plan modules."""

import torch
import torch.nn as nn
import torch.nn.functional as F

from game.rlearning.net.state_space.EntityTransitionBirth import EntityTransitionBirthStateDecoder


class PlannerSwiGLU(nn.Module):
    """Gate planner features with a compact SwiGLU feed-forward block."""
    def __init__(self, d_model, expansion=4):
        """Build the gated feature projection."""
        super().__init__()
        hidden = d_model * expansion
        self.input = nn.Linear(d_model, hidden * 2)
        self.output = nn.Linear(hidden, d_model)

    def forward(self, value):
        """Return the gated residual feature update."""
        gate, content = self.input(value).chunk(2, dim=-1)
        return self.output(F.silu(gate) * content)


class PlannerBlock(nn.Module):
    """Mix plan tokens, read state tokens, then restore the card/action condition."""
    def __init__(self, d_model, nhead, expansion=4, dropout=0.1):
        """Build one plan self-attention, state cross-attention and SwiGLU block."""
        super().__init__()
        self.self_norm = nn.RMSNorm(d_model)
        self.state_norm = nn.RMSNorm(d_model)
        self.ffn_norm = nn.RMSNorm(d_model)
        self.self_attn = nn.MultiheadAttention(d_model, nhead, dropout, batch_first=True)
        self.state_attn = nn.MultiheadAttention(d_model, nhead, dropout, batch_first=True)
        self.ffn = PlannerSwiGLU(d_model, expansion)
        self.condition_gate = nn.Sequential(nn.RMSNorm(d_model), nn.Linear(d_model, d_model), nn.Sigmoid())

    def forward(self, plan, state_tokens, state_padding_mask, condition):
        """Update plan tokens using global condition and entity-level state context."""
        update = self.self_attn(self.self_norm(plan), self.self_norm(plan), self.self_norm(plan), need_weights=False)[0]
        plan = plan + update
        query = self.state_norm(plan)
        update = self.state_attn(query, state_tokens, state_tokens, key_padding_mask=state_padding_mask, need_weights=False)[0]
        plan = plan + update + self.ffn(self.ffn_norm(plan))
        return plan + self.condition_gate(plan) * condition.unsqueeze(1)


class TransitionPlanner(nn.Module):
    """Create four deterministic plan tokens from card, action and current state."""
    def __init__(self, d_model=128, num_plan_tokens=4, nhead=4, num_layers=4, expansion=4, dropout=0.1):
        """Build the learned plan queries and repeated planner blocks."""
        super().__init__()
        self.queries = nn.Parameter(torch.empty(1, num_plan_tokens, d_model))
        nn.init.normal_(self.queries, std=0.02)
        self.card_proj = nn.Sequential(nn.RMSNorm(d_model), nn.Linear(d_model, d_model))
        self.action_proj = nn.Sequential(nn.RMSNorm(d_model), nn.Linear(d_model, d_model))
        self.state_proj = nn.Sequential(nn.RMSNorm(d_model), nn.Linear(d_model, d_model))
        self.blocks = nn.ModuleList([PlannerBlock(d_model, nhead, expansion, dropout) for _ in range(num_layers)])
        self.final_norm = nn.RMSNorm(d_model)

    def forward(self, h_card, h_action, h_state, state_tokens, state_padding_mask):
        """Return the four-token plan without sampling any stochastic latent."""
        condition = self.card_proj(h_card) + self.action_proj(h_action) + self.state_proj(h_state)
        plan = self.queries.expand(h_card.shape[0], -1, -1) + condition.unsqueeze(1)
        for block in self.blocks:
            plan = block(plan, state_tokens, state_padding_mask, condition)
        return self.final_norm(plan)


class PlanConditionedEntityTransitionBirthStateDecoder(EntityTransitionBirthStateDecoder):
    """Decode source and birth entities from deterministic plans plus stochastic memory."""
    def forward(self, state_tokens, state_padding_mask, spans, transition_vec, transition_plan):
        """Join plan tokens and z-derived tokens before the existing entity decoder."""
        memory = torch.cat([transition_plan, self.make_transition_memory(transition_vec)], dim=1)
        batch_size = state_tokens.shape[0]
        birth_queries = self.birth_queries.expand(batch_size, -1, -1)
        birth_mask = torch.zeros(batch_size, self.num_birth_slots, dtype=torch.bool, device=state_tokens.device)
        tokens = torch.cat([state_tokens, birth_queries], dim=1)
        padding_mask = torch.cat([state_padding_mask, birth_mask], dim=1)
        hidden = self.final_norm(self.decoder(tgt=tokens, memory=memory, tgt_key_padding_mask=padding_mask))
        source_count = state_tokens.shape[1]
        prediction = self.decode_by_spans(hidden[:, :source_count], spans)
        prediction["births"] = self.decode_birth_slots(hidden[:, source_count:])
        return prediction
