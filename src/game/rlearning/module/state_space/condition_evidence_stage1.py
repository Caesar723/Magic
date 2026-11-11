import torch

from game.rlearning.module.state_space.condition_stage1 import ConditionStage1Trainer
from game.rlearning.module.state_space.EntityTransitionSupportPlanBirth import extract_entity_tokens
from game.rlearning.net.state_space.EntityTransition import squeeze_entity_time_dim
from game.rlearning.net.state_space.LatentEntitySelector import build_existing_change_targets,strict_topk_mask
from game.rlearning.datasets.state_space.condition_evidence_dataset import ConditionEvidenceDataset
from game.rlearning.net.state_space.condition_evidence import ConditionCardFieldEncoder
from game.rlearning.synthesis.artifacts import write_card_fusion_space_artifact
from game.rlearning.synthesis.entity_transition import align_entity_transitions


class ConditionEvidenceStage1Trainer(ConditionStage1Trainer):
    def restore_checkpoint(self,restore_step):
        if restore_step!=0:
            suffix="last" if restore_step==-1 else str(restore_step)
            checkpoint=f"{self.logdir}/ckpt/g_{suffix}"
            state=torch.load(checkpoint,map_location="cpu",weights_only=True)
            if "reader.query.weight" not in state.get("ConditionEvidenceReader",{}):
                raise ValueError("This checkpoint predates the unified Evidence Reader. Start this architecture with -r 0.")
        return super().restore_checkpoint(restore_step)

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
        _,raw_tokens,text_padding,offsets=encoder(card["description"],device=h_s.device)

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
        reader_padding=text_padding|~(offsets[...,1]>offsets[...,0]).to(h_s.device)
        source_index=self.token_indices(batch,spans_s,"source")
        target_index=self.token_indices(batch,spans_s,"target")

        fused,h_action,evidence,attention=models["ConditionEvidenceReader"](
            tokens_s,h_action,field_tokens,text_tokens,
            pad_s,field_padding,reader_padding,source_index,target_index,
        )

        h_card=models["CardFusion"](evidence[:,0],h_attr)
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
            "fusion_hidden":[],
            "text_tokens":text_tokens,
            "text_padding":text_padding,
            "text_offsets":offsets,
            "field_padding":field_padding,
            "evidence_attention":attention,
            "field_attention":attention[:,:field_tokens.shape[1]],
            "text_attention":attention[:,field_tokens.shape[1]:],
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
        field_names=ConditionCardFieldEncoder.field_names
        attention=batch["evidence_attention"]
        field=batch["field_attention"]
        text=batch["text_attention"]
        target=torch.zeros_like(attention)
        field_target=torch.zeros_like(field)
        text_losses=[]
        text_rows=[]

        for row,label in enumerate(batch["supervision"]):
            groups=[]
            for name in dict.fromkeys(label.get("fields",[])):
                if name not in field_names:
                    continue
                index=field_names.index(name)
                if batch["field_padding"][row,index]:
                    continue
                group=torch.zeros_like(attention[row])
                group[index]=1.0
                groups.append(group)
                field_target[row,index]=1.0

            offsets=batch["text_offsets"][row].to(text.device)
            valid=(offsets[:,1]>offsets[:,0])&~batch["text_padding"][row]
            limit=int(offsets[:,1].max()) if offsets.numel() else 0
            spans=label.get("spans",{})
            for part in dict.fromkeys(label.get("text_parts",[])):
                ranges=spans.get(part,[])
                if not ranges or any(start<0 or end<=start or end>limit for start,end in ranges):
                    continue
                mask=torch.zeros_like(valid)
                for start,end in ranges:
                    mask|=valid&(offsets[:,0]<end)&(offsets[:,1]>start)
                if not mask.any():
                    continue
                group=torch.zeros_like(attention[row])
                group[field.shape[1]:]=mask.to(group.dtype)/mask.sum()
                groups.append(group)
                conditional=text[row]/text[row].sum().clamp_min(1e-8)
                text_losses.append(-(conditional*mask).sum().clamp_min(1e-8).log())
                text_rows.append(row)

            if groups:
                target[row]=torch.stack(groups).mean(dim=0)

        supervised=target.sum(dim=-1)>0
        # KL removes the target entropy, including the different number/length of spans.
        values=(target*(target.clamp_min(1e-8).log()-attention.clamp_min(1e-8).log())).sum(dim=-1)
        evidence_loss=(values*supervised).sum()/supervised.sum().clamp_min(1)
        counts=field_target.sum(dim=-1)
        valid_fields=counts>0
        field_target=field_target/counts.unsqueeze(-1).clamp_min(1)
        conditional=field/field.sum(dim=-1,keepdim=True).clamp_min(1e-8)
        values=-(field_target*conditional.clamp_min(1e-8).log()).sum(dim=-1)
        field_loss=(values*valid_fields).sum()/valid_fields.sum().clamp_min(1)
        text_loss=attention.sum()*0.0
        text_samples=attention.new_zeros(())
        if text_losses:
            rows=torch.tensor(text_rows,dtype=torch.long,device=attention.device)
            totals=attention.new_zeros(attention.shape[0]).index_add(0,rows,torch.stack(text_losses))
            counts=attention.new_zeros(attention.shape[0]).index_add(0,rows,torch.ones_like(rows,dtype=attention.dtype))
            text_samples=(counts>0).sum()
            text_loss=(totals/counts.clamp_min(1)).sum()/text_samples.clamp_min(1)
        return {
            "evidence_attention_loss":evidence_loss,
            "evidence_supervised_samples":supervised.sum(),
            "text_attention_loss":text_loss,
            "field_attention_loss":field_loss,
            "text_supervised_samples":text_samples,
            "field_supervised_samples":valid_fields.sum(),
            "field_attention_mass":field.sum(dim=-1).mean(),
            "text_attention_mass":text.sum(dim=-1).mean(),
        }

    def _forward(self,batch,models,isTrain,step,epoch):
        loss=super()._forward(batch,models,isTrain,step,epoch)
        evidence=self.evidence_loss(batch)
        loss.update(evidence)
        loss["total_loss"]+=self.config.get("w_evidence_attention",0.05)*evidence["evidence_attention_loss"]
        return loss

    def _write_card_fusion_space_artifact(self,step_dir,models,*,fallback_vectors,transition_records):
        # h_card now depends on scene/action-selected evidence, so use actual replay encodings.
        return write_card_fusion_space_artifact(
            step_dir,step=self.step,fused_vectors=fallback_vectors,records=transition_records
        )
