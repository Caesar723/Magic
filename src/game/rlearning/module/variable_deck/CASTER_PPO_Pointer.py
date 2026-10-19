from pathlib import Path

import onnxruntime as ort
import torch
import torch.nn.functional as F

from game.game_function_tool import ORGPATH
from game.rlearning.onnx_export.torch_session import TorchONNXSession
from game.rlearning.utils.baseAgent import BaseTrainer
from game.rlearning.utils.data import batch_to_cuda,detach_cuda,to_cpu


class CASTER_PPO_Pointer(BaseTrainer):
    def __init__(self, config,restore_step, rank=0, n_gpus=1,name="main"):
        super().__init__(config,restore_step, rank, n_gpus,name)

        self.embed_dim=config["model"]["CandidateEncoder"]["embed_dim"]
        self.planner_dim=config["planner_dim"]
        self.q_dim=config["q_dim"]
        self.rl_zone_paths=(
            ("card_zones","hand"),
            ("card_zones","graveyard"),
            ("card_zones","stack_cards"),
            ("board_zones","self_board"),
            ("board_zones","oppo_board"),
            ("board_zones","self_land"),
            ("board_zones","oppo_land")
        )
        self.action_zone_paths=(
            ("card_zones","hand"),
            ("card_zones","library"),
            ("card_zones","graveyard"),
            ("card_zones","stack_cards"),
            ("board_zones","self_board"),
            ("board_zones","oppo_board"),
            ("board_zones","self_land"),
            ("board_zones","oppo_land")
        )
    def _init_extra(self):
        super()._init_extra()

        config=self.config["extra"]["onnx"]
        root=Path(ORGPATH).resolve().parent
        device=torch.device(f"cuda:{self.rank}" if torch.cuda.is_available() else "cpu")

        self.extra={
            "device":device,
            "action_embedding":TorchONNXSession(
                root/config["action_embedding"]["path"],
                device,
                config["providers"]
            ),
            "card_embedding":TorchONNXSession(
                root/config["card_embedding"]["path"],
                device,
                config["providers"]
            )
        }
    def _forward(self,batch,models,isTrain,step,epoch):
        batch=self.predict(batch,models,isTrain,step,epoch)
        loss={}
        total_loss=batch["value"].new_zeros(())

        if self.config.get("w_val_loss",0)>0:
            val_loss=F.mse_loss(batch["value"],batch["value_target"].detach())
            total_loss+=self.config["w_val_loss"]*val_loss
            loss["val_loss"]=val_loss

        log_ratio=batch["new_prob_log"]-batch["old_prob_log"].detach()
        ratio=torch.exp(log_ratio)

        if self.config.get("w_act_loss",0)>0:
            advantage=batch["advantage"].detach()
            surr1=ratio*advantage
            surr2=torch.clamp(
                ratio,
                1-self.config["ppo"]["clip_para"],
                1+self.config["ppo"]["clip_para"]
            )*advantage
            act_loss=-torch.min(surr1,surr2).mean()
            total_loss+=self.config["w_act_loss"]*act_loss
            loss["act_loss"]=act_loss

        if self.config.get("w_kl_loss",0)>0:
            kl_loss=((ratio-1)-log_ratio).mean()
            total_loss+=self.config["w_kl_loss"]*kl_loss
            loss["kl_loss"]=kl_loss

        if self.config.get("w_entropy_loss",0)>0:
            entropy_loss=-batch["entropy"].mean()
            total_loss+=self.config["w_entropy_loss"]*entropy_loss
            loss["entropy_loss"]=entropy_loss

        loss["total_loss"]=total_loss
        return loss


    @staticmethod
    def _select_time(x,flat_time_mask):
        return x.flatten(0,1)[flat_time_mask]

    @staticmethod
    def _restore_time(x,valid_indices,batch_size,time_steps):
        flat=x.new_zeros((batch_size*time_steps,)+x.shape[1:])
        flat=flat.index_copy(0,valid_indices,x)
        return flat.view(batch_size,time_steps,*x.shape[1:])

    @staticmethod
    def _build_time_layout(lengths,time_steps,device):
        lengths=lengths.to(device=device,dtype=torch.long)
        time_mask=torch.arange(time_steps,device=device).unsqueeze(0)<lengths.unsqueeze(1)
        flat_time_mask=time_mask.reshape(-1)
        valid_indices=flat_time_mask.nonzero(as_tuple=False).squeeze(-1)
        return lengths,time_mask,flat_time_mask,valid_indices

    @staticmethod
    def _concat_zone_field(state,zone_paths,field):
        return torch.cat([state[group][zone][field] for group,zone in zone_paths],dim=2)

    def _select_zone_field(self,state,zone_paths,field,flat_time_mask):
        return self._select_time(self._concat_zone_field(state,zone_paths,field),flat_time_mask)

    def _flatten_zone_descriptions(self,state,zone_paths,valid_indices,time_steps):
        descriptions=[]
        for flat_index in valid_indices.detach().cpu().tolist():
            batch_index=flat_index//time_steps
            time_index=flat_index%time_steps
            for group,zone in zone_paths:
                descriptions.extend(state[group][zone]["descriptions"][batch_index][time_index])
        return descriptions

    @staticmethod
    def _flatten_candidate_descriptions(candidates,valid_indices,time_steps):
        descriptions=[]
        for flat_index in valid_indices.detach().cpu().tolist():
            batch_index=flat_index//time_steps
            time_index=flat_index%time_steps
            descriptions.extend(candidates["descriptions"][batch_index][time_index])
        return descriptions

    def _build_entity_features(self,batch,models,flat_time_mask,valid_indices,batch_size,time_steps):
        state=batch["rl_state"]
        device=self.extra["device"]

        card_mask=self._select_zone_field(state,self.rl_zone_paths,"card_mask",flat_time_mask).bool()
        num_states,num_entities=card_mask.shape

        descriptions=self._flatten_zone_descriptions(state,self.rl_zone_paths,valid_indices,time_steps)
        text_embeddings=models["TextEncoder"](descriptions,device=device)

        card_types=self._select_zone_field(state,self.rl_zone_paths,"card_types",flat_time_mask)
        card_special_types=self._select_zone_field(state,self.rl_zone_paths,"card_special_types",flat_time_mask)
        card_mana_costs=self._select_zone_field(state,self.rl_zone_paths,"card_costs",flat_time_mask)
        card_color_identity=self._select_zone_field(state,self.rl_zone_paths,"card_color_identity",flat_time_mask)
        card_attacks=self._select_zone_field(state,self.rl_zone_paths,"card_atks",flat_time_mask)
        card_defends=self._select_zone_field(state,self.rl_zone_paths,"card_hps",flat_time_mask)
        card_has_state=self._select_zone_field(state,self.rl_zone_paths,"card_has_state",flat_time_mask)

        num_cards=num_states*num_entities
        onnx_inputs={
            "text_embeddings":text_embeddings.reshape(num_cards,-1),
            "card_types":card_types.reshape(num_cards).long(),
            "card_special_types":card_special_types.reshape(num_cards,card_special_types.shape[-1]),
            "card_mana_costs":card_mana_costs.reshape(num_cards,card_mana_costs.shape[-1]),
            "card_color_identity":card_color_identity.reshape(num_cards,card_color_identity.shape[-1]),
            "card_attacks":card_attacks.reshape(num_cards).float(),
            "card_defends":card_defends.reshape(num_cards).float(),
            "card_has_state":card_has_state.reshape(num_cards).float(),
            "card_mask":card_mask.reshape(num_cards)
        }
        output_specs={"card_embeddings":((num_cards,self.embed_dim),torch.float32)}
        card_embeddings=self.extra["card_embedding"].run(onnx_inputs,output_specs)["card_embeddings"]
        card_embeddings=card_embeddings.view(num_states,num_entities,self.embed_dim)

        card_base_atks=self._select_zone_field(state,self.rl_zone_paths,"card_base_atks",flat_time_mask)
        card_base_hps=self._select_zone_field(state,self.rl_zone_paths,"card_base_hps",flat_time_mask)
        card_tapped=self._select_zone_field(state,self.rl_zone_paths,"card_tapped",flat_time_mask)
        card_tapped_valid=self._select_zone_field(state,self.rl_zone_paths,"card_tapped_valid",flat_time_mask)
        card_is_attacker=self._select_zone_field(state,self.rl_zone_paths,"card_is_attacker",flat_time_mask)

        dynamic_features=torch.stack([card_base_atks,card_base_hps,card_tapped,card_tapped_valid,card_is_attacker],dim=-1).float()
        entity_features=torch.cat([card_embeddings,dynamic_features],dim=-1)
        entity_features=entity_features.masked_fill(~card_mask.unsqueeze(-1),0.0)

        entity_features=self._restore_time(entity_features,valid_indices,batch_size,time_steps)
        entity_mask=self._restore_time(card_mask,valid_indices,batch_size,time_steps)
        return entity_features,entity_mask


    def _build_candidate_features(self,batch,models,flat_time_mask,valid_indices,batch_size,time_steps):
        state=batch["action_embedding_state"]
        candidates=batch["candidates"]
        device=self.extra["device"]

        global_state=self._select_time(state["global_state"],flat_time_mask)
        entity_card_types=self._select_zone_field(state,self.action_zone_paths,"card_types",flat_time_mask)
        entity_card_costs=self._select_zone_field(state,self.action_zone_paths,"card_costs",flat_time_mask)
        entity_card_color_identity=self._select_zone_field(state,self.action_zone_paths,"card_color_identity",flat_time_mask)
        entity_card_special_types=self._select_zone_field(state,self.action_zone_paths,"card_special_types",flat_time_mask)
        entity_card_atks=self._select_zone_field(state,self.action_zone_paths,"card_atks",flat_time_mask)
        entity_card_hps=self._select_zone_field(state,self.action_zone_paths,"card_hps",flat_time_mask)
        entity_card_has_state=self._select_zone_field(state,self.action_zone_paths,"card_has_state",flat_time_mask)
        entity_card_is_attacker=self._select_zone_field(state,self.action_zone_paths,"card_is_attacker",flat_time_mask)
        entity_card_mask=self._select_zone_field(state,self.action_zone_paths,"card_mask",flat_time_mask).bool()
        stack_player_one_hot=self._select_time(state["stack_extra"]["player_one_hot"],flat_time_mask)

        candidate_actions=self._select_time(candidates["actions"],flat_time_mask).long()
        candidate_card_types=self._select_time(candidates["card_types"],flat_time_mask).long()
        candidate_special_types=self._select_time(candidates["special_types"],flat_time_mask).float()
        candidate_mana_costs=self._select_time(candidates["mana_costs"],flat_time_mask).float()
        candidate_color_identity=self._select_time(candidates["color_identity"],flat_time_mask).float()
        candidate_attacks=self._select_time(candidates["attacks"],flat_time_mask).float()
        candidate_defends=self._select_time(candidates["defends"],flat_time_mask).float()
        candidate_has_state=self._select_time(candidates["has_state"],flat_time_mask).float()
        candidate_has_card=self._select_time(candidates["has_card"],flat_time_mask).bool()
        candidate_mask=self._select_time(candidates["mask"],flat_time_mask).bool()
        candidate_indices=self._select_time(candidates["indices"],flat_time_mask).long()

        num_states,num_candidates=candidate_actions.shape
        descriptions=self._flatten_candidate_descriptions(candidates,valid_indices,time_steps)
        candidate_text_embeddings=models["TextEncoder"](descriptions,device=device).view(num_states,num_candidates,-1)

        onnx_inputs={
            "global_state":global_state.float(),
            "entity_card_types":entity_card_types.long(),
            "entity_card_costs":entity_card_costs.float(),
            "entity_card_color_identity":entity_card_color_identity.float(),
            "entity_card_special_types":entity_card_special_types.float(),
            "entity_card_atks":entity_card_atks.float(),
            "entity_card_hps":entity_card_hps.float(),
            "entity_card_has_state":entity_card_has_state.float(),
            "entity_card_is_attacker":entity_card_is_attacker.float(),
            "entity_card_mask":entity_card_mask,
            "stack_player_one_hot":stack_player_one_hot.float(),
            "candidate_actions":candidate_actions,
            "candidate_text_embeddings":candidate_text_embeddings,
            "candidate_card_types":candidate_card_types,
            "candidate_special_types":candidate_special_types,
            "candidate_mana_costs":candidate_mana_costs,
            "candidate_color_identity":candidate_color_identity,
            "candidate_attacks":candidate_attacks,
            "candidate_defends":candidate_defends,
            "candidate_has_state":candidate_has_state,
            "candidate_has_card":candidate_has_card,
            "candidate_mask":candidate_mask
        }
        output_specs={
            "planner":((num_states,num_candidates,4,self.planner_dim),torch.float32),
            "mean_p":((num_states,num_candidates,self.q_dim),torch.float32),
            "std_p":((num_states,num_candidates,self.q_dim),torch.float32)
        }
        onnx_outputs=self.extra["action_embedding"].run(onnx_inputs,output_specs)

        planner=onnx_outputs["planner"]
        mean_p=onnx_outputs["mean_p"]
        std_p=onnx_outputs["std_p"]

        special_action_ids=torch.where(candidate_indices<=1,candidate_indices,torch.full_like(candidate_indices,-1))

        candidate_features=models["CandidateEncoder"](
            planner.reshape(num_states*num_candidates,4,self.planner_dim),
            mean_p.reshape(num_states*num_candidates,self.q_dim),
            std_p.reshape(num_states*num_candidates,self.q_dim),
            special_action_ids.reshape(-1)
        )
        candidate_features=candidate_features.view(num_states,num_candidates,self.embed_dim)
        candidate_features=candidate_features.masked_fill(~candidate_mask.unsqueeze(-1),0.0)

        return {
            "features":self._restore_time(candidate_features,valid_indices,batch_size,time_steps),
            "mask":self._restore_time(candidate_mask,valid_indices,batch_size,time_steps),
            "planner":planner,
            "mean_p":mean_p,
            "std_p":std_p
        }


    def predict(self,batch,models,isTrain,step,epoch):
        global_scalars=batch["rl_state"]["global_scalars"]
        batch_size,time_steps=global_scalars.shape[:2]
        device=global_scalars.device

        lengths,time_mask,flat_time_mask,valid_indices=self._build_time_layout(batch["lengths"],time_steps,device)
        entity_features,entity_mask=self._build_entity_features(batch,models,flat_time_mask,valid_indices,batch_size,time_steps)
        candidates=self._build_candidate_features(batch,models,flat_time_mask,valid_indices,batch_size,time_steps)

        state_result=models["StateTransformer"](
            global_scalars=global_scalars,
            entity_features=entity_features,
            candidate_features=candidates["features"],
            planner=batch["planner"],
            mean_p=batch["mean_p"],
            std_p=batch["std_p"],
            lengths=lengths,
            six_available=batch["six_available"],
            special_action_ids=batch["special_action_ids"],
            entity_mask=entity_mask,
            candidate_mask=candidates["mask"]
        )

        temporal_feature_actor=models["TemporalBlockActor"](state_result["state_features"],lengths)
        temporal_feature_critic=models["TemporalBlockCritic"](state_result["state_features"],lengths)
        logits=models["Actor"](temporal_feature_actor,state_result["last_candidates"],state_result["last_candidate_mask"])
        dist=torch.distributions.Categorical(logits=logits)
        value=models["Critic"](temporal_feature_critic)

        batch.update(state_result)
        batch["temporal_feature_actor"]=temporal_feature_actor
        batch["temporal_feature_critic"]=temporal_feature_critic
        batch["logits"]=logits
        batch["actions"]=dist.probs
        batch["dist"]=dist
        batch["entropy"]=dist.entropy()
        batch["value"]=value
        batch["time_mask"]=time_mask

        training_action="action" in batch
        candidate_slot=batch["action"].long().reshape(-1) if training_action else dist.sample()
        batch["candidate_slot"]=candidate_slot

        batch["new_prob_log"]=dist.log_prob(candidate_slot)
        if not training_action:
            batch["sampled_log_prob"]=batch["new_prob_log"]

        batch_indices=torch.arange(batch_size,device=device)
        last_time_indices=lengths-1
        last_valid_indices=lengths.cumsum(0)-1

        batch["selected_planner"]=candidates["planner"][last_valid_indices,candidate_slot]
        batch["selected_mean"]=candidates["mean_p"][last_valid_indices,candidate_slot]
        batch["selected_std"]=candidates["std_p"][last_valid_indices,candidate_slot]

        environment_action=batch["candidates"]["indices"][batch_indices,last_time_indices,candidate_slot]
        batch["environment_action"]=environment_action

        if not training_action:
            batch["action"]=environment_action.item() if batch_size==1 else environment_action

        return batch

    @torch.no_grad()
    def choose_action(self,batch,extra_keys=None,isTrain=False):
        extra_keys=extra_keys or []
        models=self.models

        for model in models.values():
            model.train() if isTrain else model.eval()

        batch=[self.dataset.get_sample_preprocess(b,extra_keys) for b in batch]

        batch=self.dataset.collate_state(batch,extra_keys)
        batch=batch_to_cuda(batch,self.rank)
        return self.predict(batch,models,isTrain,self.step,self.epoch)

    def build_inference_result(self,batch,index):
        action=batch["environment_action"][index]
        return {
            "action":int(action.detach().cpu().item()),
            "candidate_slot":batch["candidate_slot"][index:index+1].detach().cpu().numpy(),
            "selected_planner":batch["selected_planner"][index:index+1].detach().cpu().numpy(),
            "selected_mean":batch["selected_mean"][index:index+1].detach().cpu().numpy(),
            "selected_std":batch["selected_std"][index:index+1].detach().cpu().numpy(),
            "sampled_log_prob":batch["sampled_log_prob"][index:index+1].detach().cpu().numpy(),
            "value":batch["value"][index:index+1].detach().cpu().numpy()
        }