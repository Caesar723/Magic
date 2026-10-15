import torch

from game.rlearning.onnx_export.base import ONNXExportWrapper


class CardEmbeddingWrapper(ONNXExportWrapper):
    input_names=(
        "text_embeddings",
        "card_types",
        "card_special_types",
        "card_mana_costs",
        "card_color_identity",
        "card_attacks",
        "card_defends",
        "card_has_state",
        "card_mask"
    )
    output_names=("card_embeddings",)

    def __init__(self,models,training_config,export_config):
        super().__init__(models,training_config,export_config)
        required=("CardStateEncoder","CardFusion")
        missing=[name for name in required if name not in self.models]
        if missing:
            raise KeyError(f"CardEmbeddingWrapper missing models: {missing}")

    def forward(
        self,text_embeddings,card_types,card_special_types,
        card_mana_costs,card_color_identity,card_attacks,
        card_defends,card_has_state,card_mask
    ):
        card_attributes=self.models["CardStateEncoder"](
            card_types,
            card_special_types,
            card_mana_costs,
            card_attacks,
            card_defends,
            card_has_state,
            card_color_identity
        )
        card_embeddings=self.models["CardFusion"](text_embeddings,card_attributes)
        return card_embeddings.masked_fill(~card_mask.bool().unsqueeze(-1),0.0)

    def build_example_inputs(self):
        num_cards=8
        card_config=self.training_config["model"]["CardStateEncoder"]
        fusion_config=self.training_config["model"]["CardFusion"]

        text_embeddings=torch.zeros(num_cards,fusion_config["text_dim"],dtype=torch.float32)
        card_types=torch.zeros(num_cards,dtype=torch.long)
        card_special_types=torch.zeros(num_cards,card_config["num_special"],dtype=torch.float32)
        card_mana_costs=torch.zeros(num_cards,6,dtype=torch.float32)
        card_color_identity=torch.zeros(num_cards,5,dtype=torch.float32)
        card_attacks=torch.zeros(num_cards,dtype=torch.float32)
        card_defends=torch.zeros(num_cards,dtype=torch.float32)
        card_has_state=torch.zeros(num_cards,dtype=torch.float32)
        card_mask=torch.tensor([True,True,True,True,True,False,False,False],dtype=torch.bool)

        return (
            text_embeddings,card_types,card_special_types,
            card_mana_costs,card_color_identity,card_attacks,
            card_defends,card_has_state,card_mask
        )

    def get_dynamic_axes(self,dynamic_batch=True,dynamic_candidates=True):
        if not dynamic_batch:
            return {}

        axes={name:{0:"num_cards"} for name in self.input_names}
        axes["card_embeddings"]={0:"num_cards"}
        return axes