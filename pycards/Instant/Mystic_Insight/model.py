
from game.type_cards.instant import Instant


class Mystic_Insight(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Mystic Insight"

        self.type:str="Instant"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Scry 3, then draw a card."
        self.image_path:str="cards/Instant/Mystic Insight/image.jpg"



        