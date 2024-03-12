
from game.type_cards.instant import Instant


class Temporal_Manipulation(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Temporal Manipulation"

        self.type:str="Instant"

        self.mana_cost:str="3U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Mythic Rare"
        self.content:str="Take an extra turn after this one."
        self.image_path:str="cards/Instant/Temporal Manipulation/image.jpg"



        