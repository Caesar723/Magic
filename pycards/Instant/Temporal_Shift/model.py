
from game.type_cards.instant import Instant


class Temporal_Shift(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Temporal Shift"

        self.type:str="Instant"

        self.mana_cost:str="2UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="You may take an extra turn after this one. Exile Temporal Shift."
        self.image_path:str="cards/Instant/Temporal Shift/image.jpg"



        