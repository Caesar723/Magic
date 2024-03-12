
from game.type_cards.instant import Instant


class Mystic_Reflection(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Mystic Reflection"

        self.type:str="Instant"

        self.mana_cost:str="1UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Choose target creature. If another creature with the same name is on the battlefield, transform that creature into a copy of the chosen creature until end of turn."
        self.image_path:str="cards/Instant/Mystic Reflection/image.jpg"



        