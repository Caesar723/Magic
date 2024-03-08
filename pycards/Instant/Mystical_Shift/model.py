
from game.type_cards.instant import Instant


class Mystical_Shift(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Mystical Shift"

        self.type:str="Instant"

        self.mana_cost:str="U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Counter target spell unless its controller pays X. If X is 3 or more, draw a card."
        self.image_path:str="cards/Instant/Mystical Shift/image.jpg"



        