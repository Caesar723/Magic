
from game.type_cards.sorcery import Sorcery


class Temporal_Flux(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Temporal Flux"

        self.type:str="Sorcery"

        self.mana_cost:str="3U"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Mythic Rare"
        self.content:str="Take an extra turn after this one."
        self.image_path:str="cards/sorcery/Temporal Flux/image.jpg"



        