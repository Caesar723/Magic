
from game.type_cards.sorcery import Sorcery


class Chaotic_Eruption(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Chaotic Eruption"

        self.type:str="Sorcery"

        self.mana_cost:str="2R"
        self.color:str="red"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Destroy target land. For each land destroyed this way, its controller may discard a card. If they don't, create a 3/3 Elemental token."
        self.image_path:str="cards/sorcery/Chaotic Eruption/image.jpg"



        