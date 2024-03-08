
from game.type_cards.instant import Instant


class Mystic_Evocation(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Mystic Evocation"

        self.type:str="Instant"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Counter target noncreature spell unless its controller pays 1. If that spell is countered this way, scry 1."
        self.image_path:str="cards/Instant/Mystic Evocation/image.jpg"



        