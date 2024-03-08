
from game.type_cards.instant import Instant


class Temporal_Reversal(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Temporal Reversal"

        self.type:str="Instant"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Mythic Rare"
        self.content:str="Return target nonland permanent to its owner's hand. You may untap up to two lands."
        self.image_path:str="cards/Instant/Temporal Reversal/image.jpg"



        