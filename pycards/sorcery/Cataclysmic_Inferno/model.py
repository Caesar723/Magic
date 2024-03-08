
from game.type_cards.sorcery import Sorcery


class Cataclysmic_Inferno(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Cataclysmic Inferno"

        self.type:str="Sorcery"

        self.mana_cost:str="3R"
        self.color:str="red"
        self.type_card:str="Sorcery"
        self.rarity:str="Mythic Rare"
        self.content:str="Cataclysmic Inferno deals X damage to each creature your opponents control, where X is the number of Mountains you control. Then, for each creature destroyed this way, create a 1/1 red Elemental creature token with haste."
        self.image_path:str="cards/sorcery/Cataclysmic Inferno/image.jpg"



        