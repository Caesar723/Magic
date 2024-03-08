
from game.type_cards.instant import Instant


class Celestial_Intervention(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Celestial Intervention"

        self.type:str="Instant"

        self.mana_cost:str="2WW"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Until end of turn, creatures you control gain indestructible. You may draw a card."
        self.image_path:str="cards/Instant/Celestial Intervention/image.jpg"



        