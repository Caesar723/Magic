from pathlib import Path

import torch
import torch.nn.functional as F

from game.game_function_tool import ORGPATH
from game.rlearning.pretrained.loader import PretrainedLoader
from game.rlearning.utils.baseAgent import BaseTrainer
from game.rlearning.utils.data import batch_to_cuda,detach_cuda,to_cpu
from game.rlearning.utils.cuda_graph import CudaGraphRunner
from game.rlearning.utils.tensor_bucket_layout import TensorBucketLayout

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
        device=torch.device(f"cuda:{self.rank}" if torch.cuda.is_available() else "cpu")
        root=Path(ORGPATH).resolve().parent
        pretrained=PretrainedLoader.get(self.config["extra"]["pretrained"],device,root)
        self.extra={
            "device":device,
            "card_embedding":pretrained.session("card_embedding"),
            "action_embedding":pretrained.session("action_embedding")
        }

    def _forward(self,batch,models,isTrain,step,epoch):
        batch=self.predict(batch,models,isTrain,step,epoch)
        mask=batch["valid_mask"].bool() & batch["time_mask"]
        loss={}

        value=batch["value"][mask]
        value_target=batch["value_target"][mask].detach()
        new_prob_log=batch["new_prob_log"][mask]
        old_prob_log=batch["old_prob_log"][mask].detach()
        advantage=batch["advantage"][mask].detach()
        entropy=batch["entropy"][mask]
        total_loss=value.new_zeros(())

        if self.config.get("w_val_loss",0)>0:
            val_loss=F.mse_loss(value,value_target)
            total_loss+=self.config["w_val_loss"]*val_loss
            loss["val_loss"]=val_loss

        log_ratio=new_prob_log-old_prob_log
        ratio=torch.exp(log_ratio)

        if self.config.get("w_act_loss",0)>0:
            surr1=ratio*advantage
            surr2=torch.clamp(ratio,1-self.config["ppo"]["clip_para"],1+self.config["ppo"]["clip_para"])*advantage
            act_loss=-torch.min(surr1,surr2).mean()
            total_loss+=self.config["w_act_loss"]*act_loss
            loss["act_loss"]=act_loss

        if self.config.get("w_kl_loss",0)>0:
            kl_loss=((ratio-1)-log_ratio).mean()
            total_loss+=self.config["w_kl_loss"]*kl_loss
            loss["kl_loss"]=kl_loss

        if self.config.get("w_entropy_loss",0)>0:
            entropy_loss=-entropy.mean()
            total_loss+=self.config["w_entropy_loss"]*entropy_loss
            loss["entropy_loss"]=entropy_loss

        loss["total_loss"]=total_loss
        return loss


    @staticmethod
    def _select_time(x,flat_time_mask):
        if flat_time_mask is None:
            return x[:,0]
        return x.flatten(0,1)[flat_time_mask]

    @staticmethod
    def _restore_time(x,valid_indices,batch_size,time_steps):
        if valid_indices is None:
            return x.unsqueeze(1)
        flat=x.new_zeros((batch_size*time_steps,)+x.shape[1:])
        flat=flat.index_copy(0,valid_indices,x)
        return flat.view(batch_size,time_steps,*x.shape[1:])

    @staticmethod
    def _build_time_layout(lengths,time_steps,device,single_step=False):
        lengths=lengths.to(device=device,dtype=torch.long)
        if single_step and time_steps==1:
            time_mask=torch.ones((lengths.shape[0],1),dtype=torch.bool,device=device)
            return lengths,time_mask,None,None

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
        if valid_indices is None:
            group,zone=zone_paths[0]
            indices=range(len(state[group][zone]["descriptions"]))
        else:
            indices=valid_indices.detach().cpu().tolist()

        for flat_index in indices:
            batch_index=flat_index//time_steps
            time_index=flat_index%time_steps
            for group,zone in zone_paths:
                descriptions.extend(state[group][zone]["descriptions"][batch_index][time_index])
        return descriptions

    @staticmethod
    def _flatten_candidate_descriptions(candidates,valid_indices,time_steps):
        descriptions=[]
        if valid_indices is None:
            indices=range(len(candidates["descriptions"]))
        else:
            indices=valid_indices.detach().cpu().tolist()

        for flat_index in indices:
            batch_index=flat_index//time_steps
            time_index=flat_index%time_steps
            descriptions.extend(candidates["descriptions"][batch_index][time_index])
        return descriptions

    def _build_entity_features(self,batch,models,flat_time_mask,valid_indices,batch_size,time_steps):
        state=batch["rl_state"]
        device=self.extra["device"]
        card_mask=self._select_zone_field(state,self.rl_zone_paths,"card_mask",flat_time_mask).bool()
        num_states,num_entities=card_mask.shape
        flat_mask=card_mask.reshape(-1)
        slots=flat_mask.nonzero(as_tuple=False).squeeze(-1)
        card_embeddings=torch.zeros((num_states*num_entities,self.embed_dim),dtype=torch.float32,device=device)

        if slots.numel()>0:
            descriptions=self._flatten_zone_descriptions(state,self.rl_zone_paths,valid_indices,time_steps)
            descriptions=[descriptions[index] for index in slots.detach().cpu().tolist()]
            feature_inputs={
                "text_embeddings":models["TextEncoder"](descriptions,device=device),
                "card_mask":flat_mask.index_select(0,slots)
            }
            fields={
                "card_types":("card_types",torch.long),
                "card_special_types":("card_special_types",torch.float32),
                "card_mana_costs":("card_costs",torch.float32),
                "card_color_identity":("card_color_identity",torch.float32),
                "card_attacks":("card_atks",torch.float32),
                "card_defends":("card_hps",torch.float32),
                "card_has_state":("card_has_state",torch.float32)
            }
            for name,(field,dtype) in fields.items():
                value=self._select_zone_field(state,self.rl_zone_paths,field,flat_time_mask)
                feature_inputs[name]=value.flatten(0,1).index_select(0,slots).to(dtype=dtype)

            output_specs={"card_embeddings":((slots.numel(),self.embed_dim),torch.float32)}
            encoded=self.extra["card_embedding"].run(feature_inputs,output_specs)["card_embeddings"]
            card_embeddings.index_copy_(0,slots,encoded)

        card_embeddings=card_embeddings.view(num_states,num_entities,self.embed_dim)
        dynamic_fields=("card_base_atks","card_base_hps","card_tapped","card_tapped_valid","card_is_attacker")
        dynamic_features=torch.stack([
            self._select_zone_field(state,self.rl_zone_paths,field,flat_time_mask)
            for field in dynamic_fields
        ],dim=-1).float()
        entity_features=torch.cat([card_embeddings,dynamic_features],dim=-1)
        entity_features=entity_features.masked_fill(~card_mask.unsqueeze(-1),0.0)
        entity_features=self._restore_time(entity_features,valid_indices,batch_size,time_steps)
        entity_mask=self._restore_time(card_mask,valid_indices,batch_size,time_steps)
        return entity_features,entity_mask

    @staticmethod
    def _build_candidate_layout(candidates):
        encoded=candidates["mask"][:,0].bool() & candidates["has_card"][:,0].bool() & (candidates["actions"][:,0]>=0)
        rows,cols=encoded.nonzero(as_tuple=True)
        count=rows.numel()
        capacity=1 << max(0,count-1).bit_length()
        layout={
            "state_ids":torch.zeros(capacity,dtype=torch.long),
            "candidate_ids":torch.zeros(capacity,dtype=torch.long),
            "valid":torch.arange(capacity)<count,
            "count":count
        }
        layout["state_ids"][:count]=rows
        layout["candidate_ids"][:count]=cols
        return layout

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

        feature_inputs={
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
        encode_mask=candidate_mask & candidate_has_card & (candidate_actions>=0)
        layout=batch.get("_candidate_layout")
        has_candidates=layout["count"]>0 if layout is not None else encode_mask.any().item()
        if has_candidates:
            feature_outputs=self.extra["action_embedding"].run(
                feature_inputs,output_specs,candidate_layout=layout
            )
        else:
            feature_outputs={
                name:torch.zeros(shape,dtype=dtype,device=device)
                for name,(shape,dtype) in output_specs.items()
            }

        planner=feature_outputs["planner"]
        mean_p=feature_outputs["mean_p"]
        std_p=feature_outputs["std_p"]

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

    def _policy_forward(self,inputs,models,single_step=False):
        state_transformer=models["StateTransformer"]
        if single_step:
            state_transformer=getattr(state_transformer,"forward_step",state_transformer)

        state_keys=(
            "global_scalars","entity_features","candidate_features",
            "planner","mean_p","std_p","lengths","six_available",
            "special_action_ids","entity_mask","candidate_mask",
            "stack_owner","stack_action"
        )
        state_result=state_transformer(**{
            key:inputs[key] for key in state_keys
        })

        actor_state=(inputs["actor_h"],inputs["actor_c"])
        critic_state=(inputs["critic_h"],inputs["critic_c"])

        actor_output,actor_state_out=models["TemporalBlockActor"](
            state_result["state_features"],inputs["lengths"],actor_state
        )
        critic_output,critic_state_out=models["TemporalBlockCritic"](
            state_result["state_features"],inputs["lengths"],critic_state
        )

        flat_time_mask=None if single_step else inputs["time_mask"].reshape(-1)

        actor_features=self._select_time(actor_output,flat_time_mask)
        critic_features=self._select_time(critic_output,flat_time_mask)
        candidate_features=self._select_time(state_result["all_candidates"],flat_time_mask)
        candidate_mask=self._select_time(inputs["candidate_mask"],flat_time_mask)

        logits=models["Actor"](actor_features,candidate_features,candidate_mask)
        value=models["Critic"](critic_features)

        return state_result,actor_output,actor_state_out,critic_output,critic_state_out,logits,value

    def _create_policy_graph_layout(self,settings):
        batch_names=(
            "global_scalars","entity_features","candidate_features",
            "planner","mean_p","std_p","lengths","six_available",
            "special_action_ids","entity_mask","candidate_mask",
            "stack_owner","stack_action","time_mask"
        )
        input_axes={name:{0:"batch"} for name in batch_names}

        for name in ("actor_h","actor_c","critic_h","critic_c"):
            input_axes[name]={1:"batch"}

        for name in ("candidate_features","candidate_mask"):
            input_axes[name][2]="candidate"

        state_axes={
            "state_features":{0:"batch"},
            "all_candidates":{0:"batch",2:"candidate"},
            "last_state_feature":{0:"batch"},
            "last_candidates":{0:"batch",1:"candidate"},
            "last_candidate_mask":{0:"batch",1:"candidate"},
            "time_mask":{0:"batch"}
        }
        output_axes={
            "state":state_axes,
            "actor_output":{0:"batch"},
            "actor_state":{"h":{1:"batch"},"c":{1:"batch"}},
            "critic_output":{0:"batch"},
            "critic_state":{"h":{1:"batch"},"c":{1:"batch"}},
            "logits":{0:"batch",1:"candidate"},
            "value":{0:"batch"}
        }

        return TensorBucketLayout(
            buckets={
                "batch":settings.get("batch_buckets",(8,32)),
                "candidate":settings.get("candidate_buckets",(4,8,32))
            },
            input_axes=input_axes,
            output_axes=output_axes,
            padding_values={
                "lengths":1,
                "time_mask":True,
                "special_action_ids":-1
            },
            padding_hook=self._fill_policy_graph_padding
        )

    def _fill_policy_graph_padding(self,buffers,inputs):
        batch=inputs["global_scalars"].shape[0]

        if buffers["global_scalars"].shape[0]>batch:
            buffers["candidate_mask"][batch:,:,0]=True

    def _policy_graph_forward(self,inputs,models):
        state,actor,actor_state,critic,critic_state,logits,value=self._policy_forward(
            inputs,models,single_step=True
        )
        return {
            "state":state,
            "actor_output":actor,
            "actor_state":{"h":actor_state[0],"c":actor_state[1]},
            "critic_output":critic,
            "critic_state":{"h":critic_state[0],"c":critic_state[1]},
            "logits":logits,
            "value":value
        }

    def clear_policy_graphs(self):
        self._policy_graph_runner=None
        self._policy_graph_layout=None
        self._policy_graph_models=None

    def _run_policy_forward(self,inputs,models,single_step=False):
        settings=self.config.get("extra",{}).get("cuda_graph",{})
        names=(
            "StateTransformer","TemporalBlockActor",
            "TemporalBlockCritic","Actor","Critic"
        )
        enabled=(
            settings.get("enabled",False)
            and single_step
            and not torch.is_grad_enabled()
            and inputs["global_scalars"].is_cuda
            and all(not models[name].training for name in names)
            and hasattr(models["StateTransformer"],"forward_step")
            and hasattr(models["TemporalBlockActor"],"forward_step")
            and hasattr(models["TemporalBlockCritic"],"forward_step")
        )

        if not enabled:
            return self._policy_forward(inputs,models,single_step=single_step)

        identity=tuple(id(models[name]) for name in names)

        if getattr(self,"_policy_graph_models",None)!=identity:
            self.clear_policy_graphs()
            self._policy_graph_models=identity

        if getattr(self,"_policy_graph_runner",None) is None:
            bucketed=settings.get("bucketed",False)
            self._policy_graph_layout=None

            if bucketed:
                self._policy_graph_layout=self._create_policy_graph_layout(settings)

            self._policy_graph_runner=CudaGraphRunner(
                max_graphs=settings.get("max_graphs",6 if bucketed else 2),
                capture_after=settings.get("capture_after",3)
            )

        def forward(static_inputs):
            return self._policy_graph_forward(static_inputs,models)

        result=self._policy_graph_runner.run(
            forward,inputs,layout=self._policy_graph_layout
        )

        return (
            result["state"],
            result["actor_output"],
            (result["actor_state"]["h"],result["actor_state"]["c"]),
            result["critic_output"],
            (result["critic_state"]["h"],result["critic_state"]["c"]),
            result["logits"],
            result["value"]
        )

    def predict(self,batch,models,isTrain,step,epoch):
        global_scalars=batch["rl_state"]["global_scalars"]
        batch_size,time_steps=global_scalars.shape[:2]
        device=global_scalars.device

        single_step=batch.get("_single_step",False) and not isTrain
        lengths,time_mask,flat_time_mask,valid_indices=self._build_time_layout(batch["lengths"],time_steps,device,single_step=single_step)
        entity_features,entity_mask=self._build_entity_features(batch,models,flat_time_mask,valid_indices,batch_size,time_steps)
        candidates=self._build_candidate_features(batch,models,flat_time_mask,valid_indices,batch_size,time_steps)

        stack_extra=batch["rl_state"]["stack_extra"]

        policy_inputs={
            "global_scalars":global_scalars,
            "entity_features":entity_features,
            "candidate_features":candidates["features"],
            "planner":batch["planner"],
            "mean_p":batch["mean_p"],
            "std_p":batch["std_p"],
            "lengths":lengths,
            "six_available":batch["six_available"],
            "special_action_ids":batch["special_action_ids"],
            "entity_mask":entity_mask,
            "candidate_mask":candidates["mask"],
            "stack_owner":stack_extra["player_one_hot"],
            "stack_action":stack_extra["action_number"],
            "actor_h":batch["actor_state_in"]["h"],
            "actor_c":batch["actor_state_in"]["c"],
            "critic_h":batch["critic_state_in"]["h"],
            "critic_c":batch["critic_state_in"]["c"],
            "time_mask":time_mask
        }

        state_result,actor_output,actor_state_out,critic_output,critic_state_out,logits,value=self._run_policy_forward(
            policy_inputs,models,single_step=single_step
        )

        dist=torch.distributions.Categorical(logits=logits)

        training_action = "action" in batch

        if training_action:
            # when PPO is updating, calculate the probability of the action in the sampled record
            candidate_slot = self._select_time(
                batch["action"], flat_time_mask
            ).long()

        elif getattr(self, "deterministic_actions", False):
            # official evaluation / player battle: select the action with the highest probability
            candidate_slot = logits.argmax(dim=-1)

        else:
            # training rollout：still use the distribution to sample the action
            candidate_slot = dist.sample()

        action_log_prob = dist.log_prob(candidate_slot)

        batch.update(state_result)
        batch["temporal_feature_actor"]=actor_output
        batch["temporal_feature_critic"]=critic_output
        batch["actor_state_out"]={"h":actor_state_out[0],"c":actor_state_out[1]}
        batch["critic_state_out"]={"h":critic_state_out[0],"c":critic_state_out[1]}
        batch["time_mask"]=time_mask
        batch["dist"]=dist

        batch["logits"]=self._restore_time(logits,valid_indices,batch_size,time_steps)
        batch["actions"]=self._restore_time(dist.probs,valid_indices,batch_size,time_steps)
        batch["entropy"]=self._restore_time(dist.entropy(),valid_indices,batch_size,time_steps)
        batch["value"]=self._restore_time(value,valid_indices,batch_size,time_steps)
        batch["candidate_slot"]=self._restore_time(candidate_slot,valid_indices,batch_size,time_steps)
        batch["new_prob_log"]=self._restore_time(action_log_prob,valid_indices,batch_size,time_steps)

        if training_action:
            return batch

        batch["sampled_log_prob"]=batch["new_prob_log"]
        row_indices=torch.arange(candidate_slot.shape[0],device=device)

        selected_planner=candidates["planner"][row_indices,candidate_slot]
        selected_mean=candidates["mean_p"][row_indices,candidate_slot]
        selected_std=candidates["std_p"][row_indices,candidate_slot]
        candidate_indices=self._select_time(batch["candidates"]["indices"],flat_time_mask)
        environment_action=candidate_indices[row_indices,candidate_slot]

        batch["selected_planner"]=self._restore_time(selected_planner,valid_indices,batch_size,time_steps)
        batch["selected_mean"]=self._restore_time(selected_mean,valid_indices,batch_size,time_steps)
        batch["selected_std"]=self._restore_time(selected_std,valid_indices,batch_size,time_steps)
        batch["environment_action"]=self._restore_time(environment_action,valid_indices,batch_size,time_steps)

        actions=batch["environment_action"][:,0]
        batch["action"]=int(actions[0].item()) if batch_size==1 else actions
        return batch

    @torch.no_grad()
    def choose_action(self,batch,extra_keys=None,isTrain=False):
        extra_keys=extra_keys or []
        models=self.models

        for model in models.values():
            model.train() if isTrain else model.eval()

        if isTrain:
            batch=[self.dataset.get_sample_preprocess(state,extra_keys) for state in batch]
            batch=self.dataset.collate_state(batch,extra_keys,prepared=True)
        else:
            batch=self.dataset.collate_inference(batch,extra_keys)

        batch["_single_step"]=(
            not isTrain
            and batch["rl_state"]["global_scalars"].shape[1]==1
            and bool((batch["lengths"]==1).all().item())
        )
        if batch["_single_step"]:
            batch["_candidate_layout"]=self._build_candidate_layout(batch["candidates"])
        batch=batch_to_cuda(batch,self.rank)
        return self.predict(batch,models,isTrain,self.step,self.epoch)

    def prepare_inference_results(self,batch):
        fields=(
            "environment_action","candidate_slot","selected_planner",
            "selected_mean","selected_std","sampled_log_prob","value"
        )
        result={name:batch[name].detach().cpu().numpy().copy() for name in fields}
        for name in ("actor_state_in","critic_state_in","actor_state_out","critic_state_out"):
            result[name]={
                key:batch[name][key].detach().cpu().numpy().copy()
                for key in ("h","c")
            }
        return result

    def build_inference_result(self,batch,index):
        if torch.is_tensor(batch["environment_action"]):
            batch=self.prepare_inference_results(batch)

        def get_lstm_state(key):
            return tuple(batch[key][name][:,index:index+1].copy() for name in ("h","c"))

        result={"action":int(batch["environment_action"][index,0])}
        fields=(
            "candidate_slot","selected_planner","selected_mean",
            "selected_std","sampled_log_prob","value"
        )
        for name in fields:
            result[name]=batch[name][index,0:1]
        for name in ("actor_state_in","critic_state_in","actor_state_out","critic_state_out"):
            result[name]=get_lstm_state(name)
        return result