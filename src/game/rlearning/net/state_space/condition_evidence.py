import torch
import torch.nn as nn
import torch.nn.functional as F



from game.rlearning.net.state_space.condition_text_encoder import ConditionJinaTokenEncoder


class ConditionCardFieldEncoder(nn.Module):
    field_names=("card_type","mana_cost","attack","defend","color_identity","special_type","has_state")

    def __init__(self,max_card_type=5,num_special=20,output_dim=128):
        super().__init__()
        self.type_embedding=nn.Embedding(max_card_type,output_dim)
        self.field_embedding=nn.Embedding(len(self.field_names),output_dim)
        self.projections=nn.ModuleList([
            nn.Linear(size,output_dim) for size in (6,1,1,5,num_special,1)
        ])
        self.norm=nn.LayerNorm(output_dim)

    def forward(self,card_type,special_type,mana_cost,attack,defend,has_state,color_identity):
        values=(
            mana_cost,
            attack.unsqueeze(-1),
            defend.unsqueeze(-1),
            color_identity,
            special_type,
            has_state.unsqueeze(-1),
        )
        tokens=[self.type_embedding(card_type.long())]
        tokens.extend(layer(value.float()) for layer,value in zip(self.projections,values))
        tokens=torch.stack(tokens,dim=1)
        tokens=self.norm(tokens+self.field_embedding.weight.unsqueeze(0))

        padding=torch.zeros(tokens.shape[:2],dtype=torch.bool,device=tokens.device)
        padding[:,2:4]=~has_state.bool().unsqueeze(-1)
        tokens=tokens.masked_fill(padding.unsqueeze(-1),0.0)
        pooled=tokens.sum(dim=1)/(~padding).sum(dim=1,keepdim=True).clamp_min(1)

        return pooled,tokens,padding



class ConditionEvidenceTokenEncoder(ConditionJinaTokenEncoder):
    @torch.no_grad()
    def forward(self,texts,device=None):
        texts=[texts] if isinstance(texts,str) else list(texts)
        device=torch.device(device or "cpu")
        encoder,tokenizer=self._load_encoder(device)
        prefix="Document: "

        inputs=tokenizer(
            [prefix+text for text in texts],
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=self.max_length,
            return_offsets_mapping=True,
        )
        offsets=(inputs.pop("offset_mapping")-len(prefix)).clamp_min(0)
        inputs={key:value.to(device) for key,value in inputs.items()}

        if hasattr(encoder,"set_adapter"):
            encoder.set_adapter([self.task])
        encoder.eval()

        hidden=encoder(**inputs).last_hidden_state.float()
        valid=inputs["attention_mask"].bool()
        positions=torch.arange(hidden.shape[1],device=device).expand_as(valid)
        last=positions.masked_fill(~valid,-1).amax(dim=1).clamp_min(0)
        pooled=hidden[torch.arange(hidden.shape[0],device=device),last]

        return pooled,hidden,~valid,offsets




class ConditionEvidenceAttention(nn.Module):
    def __init__(self,d_model=128,nhead=4,supervised_head=0):
        super().__init__()
        self.nhead=nhead
        self.head_dim=d_model//nhead
        self.supervised_head=supervised_head
        self.query=nn.Linear(d_model,d_model,bias=False)
        self.key=nn.Linear(d_model,d_model,bias=False)
        self.value=nn.Linear(d_model,d_model,bias=False)
        self.output=nn.Linear(d_model,d_model,bias=False)

    def forward(self,queries,memory,padding):
        batch,length,dim=queries.shape
        empty=padding.all(dim=1)
        memory=memory.masked_fill(empty[:,None,None],0.0)
        padding=padding.clone()
        padding[empty,0]=False
        q=self.query(queries).view(batch,length,self.nhead,self.head_dim).transpose(1,2)
        k=self.key(memory).view(batch,-1,self.nhead,self.head_dim).transpose(1,2)
        v=self.value(memory).view(batch,-1,self.nhead,self.head_dim).transpose(1,2)
        context=F.scaled_dot_product_attention(
            q,k,v,attn_mask=(~padding)[:,None,None,:],dropout_p=0.0
        )
        context=context.transpose(1,2).reshape(batch,length,dim)
        context=self.output(context).masked_fill(empty[:,None,None],0.0)
        logits=q[:,self.supervised_head,:1]@k[:,self.supervised_head].transpose(-2,-1)
        logits=logits*self.head_dim**-0.5
        attention=logits.masked_fill(padding[:,None,:],float("-inf"))
        attention=attention.softmax(dim=-1,dtype=torch.float32).squeeze(1)
        return context,attention.masked_fill(empty[:,None],0.0)


class ConditionEvidenceReader(nn.Module):
    def __init__(self,d_model=128,nhead=4,supervised_head=0):
        super().__init__()
        self.action_context=nn.Linear(d_model*2,d_model)
        self.action_norm=nn.LayerNorm(d_model)
        self.action_projection=nn.Linear(d_model,d_model)
        self.state_projection=nn.Linear(d_model,d_model)
        self.role_embedding=nn.Embedding(4,d_model)
        self.query_norm=nn.LayerNorm(d_model)
        self.memory_type=nn.Embedding(2,d_model)
        self.reader=ConditionEvidenceAttention(d_model,nhead,supervised_head)
        self.output_norm=nn.LayerNorm(d_model)

    def forward(self,state_tokens,h_action,field_tokens,text_tokens,state_padding,field_padding,text_padding,source_index,target_index):
        batch,length,_=state_tokens.shape
        rows=torch.arange(batch,device=state_tokens.device)
        source=state_tokens[rows,source_index.clamp_min(0)]
        target=state_tokens[rows,target_index.clamp_min(0)]
        source=source*(source_index>=0).unsqueeze(-1)
        target=target*(target_index>=0).unsqueeze(-1)
        h_action=self.action_norm(h_action+self.action_context(torch.cat([source,target],dim=-1)))
        roles=torch.zeros(batch,length,dtype=torch.long,device=state_tokens.device)
        roles.scatter_add_(1,source_index.clamp_min(0).unsqueeze(-1),(source_index>=0).long().unsqueeze(-1))
        roles.scatter_add_(1,target_index.clamp_min(0).unsqueeze(-1),2*(target_index>=0).long().unsqueeze(-1))
        context=self.action_projection(h_action)+self.state_projection(state_tokens[:,0])
        queries=self.query_norm(state_tokens+context.unsqueeze(1)+self.role_embedding(roles))
        memory=torch.cat([
            field_tokens+self.memory_type.weight[0],
            text_tokens+self.memory_type.weight[1],
        ],dim=1)
        padding=torch.cat([field_padding,text_padding],dim=1)
        evidence,attention=self.reader(queries,memory,padding)
        evidence=evidence.masked_fill(state_padding.unsqueeze(-1),0.0)
        result=self.output_norm(state_tokens+evidence)
        result=result.masked_fill(state_padding.unsqueeze(-1),0.0)
        return result,h_action,evidence,attention
