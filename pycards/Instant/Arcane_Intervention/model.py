
from game.type_cards.instant import Instant


class Arcane_Intervention(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Arcane Intervention"

        self.type:str="Instant"

        self.mana_cost:str="2UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Return target permanent to its owner's hand. Draw a card."
        self.image_path:str="cards/Instant/Arcane Intervention/image.jpg"



        