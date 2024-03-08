
from game.type_cards.sorcery import Sorcery


class Temporal_Distortion(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Temporal Distortion"

        self.type:str="Sorcery"

        self.mana_cost:str="2UU"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Temporal Distortion allows you to take an extra turn after this one. Exile Temporal Distortion."
        self.image_path:str="cards/sorcery/Temporal Distortion/image.jpg"



        