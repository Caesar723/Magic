import torch

from game.rlearning.pretrained.entity_transition import EntityTransitionFeatures
from game.rlearning.utils.cuda_graph import CudaGraphRunner
from game.rlearning.utils.tensor_bucket_layout import TensorBucketLayout


class EntityTransitionGraphFeatures(EntityTransitionFeatures):
    def __init__(self,models,config):
        super().__init__(models,config)
        card_names=(
            "text_embeddings","card_types","card_special_types",
            "card_mana_costs","card_color_identity","card_attacks",
            "card_defends","card_has_state","card_mask"
        )
        state_names=(
            "global_state","entity_card_types","entity_card_costs",
            "entity_card_color_identity","entity_card_special_types",
            "entity_card_atks","entity_card_hps","entity_card_has_state",
            "entity_card_is_attacker","entity_card_mask","stack_player_one_hot"
        )
        candidate_names=(
            "candidate_actions","candidate_text_embeddings","candidate_card_types",
            "candidate_special_types","candidate_mana_costs","candidate_color_identity",
            "candidate_attacks","candidate_defends","candidate_has_state",
            "candidate_has_card","candidate_mask"
        )

        self.card_graph=CudaGraphRunner(max_graphs=8,capture_after=3)
        self.action_graph=CudaGraphRunner(max_graphs=24,capture_after=3)

        self.card_layout=TensorBucketLayout(
            buckets={"card":(32,64,128,256,512,1024,2048,4096)},
            input_axes={name:{0:"card"} for name in card_names},
            output_axes={"card_embeddings":{0:"card"}}
        )

        action_axes={name:{0:"state"} for name in state_names}
        action_axes.update({
            name:{0:"state",1:"candidate"} for name in candidate_names
        })
        action_axes.update({
            name:{0:"item"}
            for name in ("_state_ids","_candidate_ids","_valid")
        })

        self.action_layout=TensorBucketLayout(
            buckets={
                "state":(8,32),
                "candidate":(4,8,32),
                "item":(8,32,128,512)
            },
            input_axes=action_axes,
            output_axes={
                name:{0:"state",1:"candidate"}
                for name in ("planner","mean_p","std_p")
            }
        )

    def _card_forward(self,inputs):
        return {"card_embeddings":self.encode_cards(**inputs)}

    def _action_forward(self,inputs):
        values={
            name:value
            for name,value in inputs.items()
            if not name.startswith("_")
        }
        layout={
            "state_ids":inputs["_state_ids"],
            "candidate_ids":inputs["_candidate_ids"],
            "valid":inputs["_valid"]
        }
        planner,mean,std=self.encode_actions(**values,candidate_layout=layout)
        return {"planner":planner,"mean_p":mean,"std_p":std}

    def run_inference(self,operation,inputs,candidate_layout=None):
        if operation=="card_embedding":
            return self.card_graph.run(
                self._card_forward,inputs,self.card_layout
            )

        if operation=="action_embedding" and candidate_layout is not None:
            values=dict(inputs)
            values["_state_ids"]=candidate_layout["state_ids"]
            values["_candidate_ids"]=candidate_layout["candidate_ids"]
            values["_valid"]=candidate_layout["valid"]
            return self.action_graph.run(
                self._action_forward,values,self.action_layout
            )

        planner,mean,std=self.encode_actions(
            **inputs,candidate_layout=candidate_layout
        )
        return {"planner":planner,"mean_p":mean,"std_p":std}