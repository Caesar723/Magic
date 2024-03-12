
from game.type_cards.instant import Instant


class Mystic_Evasion(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Mystic Evasion"

        self.type:str="Instant"

        self.mana_cost:str="2UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Return target attacking creature to its owner's hand. Draw a card."
        self.image_path:str="cards/Instant/Mystic Evasion/image.jpg"



        