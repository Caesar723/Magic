
from game.type_cards.instant import Instant


class Timeless_Intervention(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Timeless Intervention"

        self.type:str="Instant"

        self.mana_cost:str="4GW"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Exile all creatures and planeswalkers. Return all exiled creatures and planeswalkers to the battlefield under their owners' control at the beginning of the next end step."
        self.image_path:str="cards/Instant/Timeless Intervention/image.jpg"



        