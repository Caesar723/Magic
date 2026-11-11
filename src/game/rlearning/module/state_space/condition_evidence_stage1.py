import torch

from game.rlearning.module.state_space.condition_stage1 import ConditionStage1Trainer
from game.rlearning.module.state_space.EntityTransitionSupportPlanBirth import extract_entity_tokens
from game.rlearning.net.state_space.EntityTransition import squeeze_entity_time_dim
from game.rlearning.net.state_space.LatentEntitySelector import build_existing_change_targets,strict_topk_mask
from game.rlearning.datasets.state_space.condition_evidence_dataset import ConditionEvidenceDataset
from game.rlearning.synthesis.entity_transition import align_entity_transitions


class ConditionEvidenceStage1Trainer(ConditionStage1Trainer):
    @staticmethod
    def token_indices(batch,spans,prefix):
        zones=batch[prefix+"_zone"]
        slots=batch[prefix+"_slot"]
        result=torch.full_like(slots,-1)

        for zone_id,name in enumerate(ConditionEvidenceDataset.zone_names):
            start,end=spans[name]
            valid=(zones==zone_id)&(slots>=0)&(slots<end-start)
            result=torch.where(valid,slots+start,result)
        return result

    def encode(self,batch,models,isTrain,step,epoch):
        h_s,tokens_s,pad_s,spans_s=models["StateTransformerEncoder"](batch["state"])
        h_action=models["ActionEncoder"](batch["card_action_index"])
        card=batch["card_used"]

        primary=getattr(self,"models",models)
        encoder=primary.get("ConditionJinaTokenEncoder",models["ConditionJinaTokenEncoder"])
        pooled,raw_tokens,text_padding,offsets=encoder(card["description"],device=h_s.device)

        h_text=models["ConditionTextProjection"](pooled)
        text_tokens=models["ConditionTextProjection"](raw_tokens)
        h_attr,field_tokens,field_padding=models["CardStateEncoder"](
            card["card_type"].long(),
            card["special_type"],
            card["mana_cost"],
            card["attack"],
            card["defend"],
            card["has_state"].long(),
            card["color_identity"],
        )
        h_card=models["CardFusion"](h_text,h_attr)

        scanned,hidden=models["ConditionStateTextFusion"](
            state_tokens=tokens_s,
            text_tokens=text_tokens,
            state_padding=pad_s,
            text_padding=text_padding,
            return_hidden=True,
        )

        reader_padding=text_padding|~(offsets[...,1]>offsets[...,0]).to(h_s.device)
        source_index=self.token_indices(batch,spans_s,"source")
        target_index=self.token_indices(batch,spans_s,"target")

        fused,h_action,field_attention,text_attention=models["ConditionEvidenceReader"](
            scanned,h_action,field_tokens,text_tokens,
            pad_s,field_padding,reader_padding,source_index,target_index,
        )

        h_s=fused[:,0]
        plan=models["TransitionPlanner"](h_card,h_action,h_s,fused,pad_s)
        entity_tokens,entity_padding=extract_entity_tokens(fused,pad_s,spans_s)

        source=squeeze_entity_time_dim(batch["state"])
        target=squeeze_entity_time_dim(batch["next_state"])
        alignment=align_entity_transitions(source,target)
        changed,count,births=build_existing_change_targets(source,target,alignment)

        mean_p,std_p=models["PriorEncoder"](h_card,h_action,h_s)
        mean_q,std_q=models["TransitionSupportPosteriorEncoder"](
            h_card,h_action,h_s,entity_tokens,changed,entity_padding,births
        )
        mean,std=(mean_q,std_q) if isTrain else (mean_p,std_p)
        z=mean+std*torch.randn_like(mean)

        count_logits=models["ExistingTransitionCountHead"](plan,z)
        birth_logits=models["BirthCountHead"](plan,z)
        selection=models["LatentEntitySelector"](entity_tokens,plan,z,entity_padding)

        predicted_count=count_logits.argmax(dim=-1)
        predicted_mask=strict_topk_mask(selection,predicted_count,entity_padding)

        batch.update({
            "h_s":h_s,
            "tokens_s":fused,
            "pad_s":pad_s,
            "spans_s":spans_s,
            "h_action":h_action,
            "h_card":h_card,
            "transition_plan":plan,
            "fusion_hidden":hidden,
            "text_tokens":text_tokens,
            "text_padding":text_padding,
            "text_offsets":offsets,
            "field_padding":field_padding,
            "field_attention":field_attention,
            "text_attention":text_attention,
            "entity_tokens":entity_tokens,
            "entity_padding_mask":entity_padding,
            "entity_alignment":alignment,
            "changed_mask":changed,
            "existing_count":count,
            "birth_count":births,
            "mean_p":mean_p,
            "std_p":std_p,
            "mean_q":mean_q,
            "std_q":std_q,
            "z":z,
            "existing_count_logits":count_logits,
            "birth_count_logits":birth_logits,
            "selection_logits":selection,
            "predicted_existing_count":predicted_count,
            "predicted_selected_mask":predicted_mask,
        })
        return batch

    def evidence_loss(self,batch):
        field_names=("card_type","mana_cost","attack","defend","color_identity","special_type","has_state")
        field=batch["field_attention"]
        text=batch["text_attention"]
        field_target=torch.zeros_like(field)
        masks,rows=[],[]

        for row,label in enumerate(batch["supervision"]):
            indices=[
                field_names.index(name)
                for name in label.get("fields",[])
                if name in field_names
            ]
            field_target[row,indices]=1.0

            offsets=batch["text_offsets"][row]
            valid=offsets[:,1]>offsets[:,0]
            limit=int(offsets[:,1].max())
            spans=label.get("spans",{})

            for part in dict.fromkeys(label.get("text_parts",[])):
                ranges=spans.get(part,[])
                if not ranges or any(
                    start<0 or end<=start or end>limit
                    for start,end in ranges
                ):
                    continue

                mask=torch.zeros_like(valid)
                for start,end in ranges:
                    mask|=valid&(offsets[:,0]<end)&(offsets[:,1]>start)

                if mask.any():
                    masks.append(mask)
                    rows.append(row)

        field_target=field_target.masked_fill(batch["field_padding"],0.0)
        counts=field_target.sum(dim=-1)
        valid_fields=counts>0
        field_target=field_target/counts.unsqueeze(-1).clamp_min(1.0)

        values=-(field_target*field.clamp_min(1e-8).log()).sum(dim=-1)
        field_loss=(values*valid_fields).sum()/valid_fields.sum().clamp_min(1)

        text_loss=text.sum()*0.0
        text_samples=text.new_zeros(())

        if masks:
            indices=torch.tensor(rows,dtype=torch.long,device=text.device)
            selected=torch.stack(masks).to(device=text.device,dtype=text.dtype)
            mass=(text.index_select(0,indices)*selected).sum(dim=-1)
            losses=-mass.clamp_min(1e-8).log()

            totals=text.new_zeros(text.shape[0]).index_add(0,indices,losses)
            counts=text.new_zeros(text.shape[0]).index_add(
                0,indices,torch.ones_like(losses)
            )
            text_samples=(counts>0).sum()
            text_loss=(totals/counts.clamp_min(1)).sum()/text_samples.clamp_min(1)

        return {
            "text_attention_loss":text_loss,
            "field_attention_loss":field_loss,
            "text_supervised_samples":text_samples,
            "field_supervised_samples":valid_fields.sum(),
        }

    def _forward(self,batch,models,isTrain,step,epoch):
        loss=super()._forward(batch,models,isTrain,step,epoch)
        evidence=self.evidence_loss(batch)
        loss.update(evidence)

        loss["total_loss"]=(
            loss["total_loss"]
            + self.config.get("w_text_attention",0.05)*evidence["text_attention_loss"]
            + self.config.get("w_field_attention",0.05)*evidence["field_attention_loss"]
        )
        return loss

    def _write_card_fusion_space_artifact(self,step_dir,models,*,fallback_vectors,transition_records):
        primary=getattr(self,"models",models)
        encoder=primary.get("ConditionJinaTokenEncoder",models["ConditionJinaTokenEncoder"])

        def encode_text(texts,device=None):
            pooled,_,_,_=encoder(texts,device=device)
            return models["ConditionTextProjection"](pooled)

        def encode_fields(*args):
            pooled,_,_=models["CardStateEncoder"](*args)
            return pooled

        encode_text._load_encoder=encoder._load_encoder
        catalog_models=models.copy()
        catalog_models["TextEncoder"]=encode_text
        catalog_models["CardStateEncoder"]=encode_fields

        return super()._write_card_fusion_space_artifact(
            step_dir,catalog_models,
            fallback_vectors=fallback_vectors,
            transition_records=transition_records,
        )