
from game.type_cards.instant import Instant


class Mystic_Reversal(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Mystic Reversal"

        self.type:str="Instant"

        self.mana_cost:str="1UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Counter target spell. If that spell is countered this way, its controller may cast it without paying its mana cost during their next turn."
        self.image_path:str="cards/Instant/Mystic Reversal/image.jpg"



        