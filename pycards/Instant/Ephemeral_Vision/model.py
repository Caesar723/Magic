
from game.type_cards.instant import Instant


class Ephemeral_Vision(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Ephemeral Vision"

        self.type:str="Instant"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Draw a card. Scry 2."
        self.image_path:str="cards/Instant/Ephemeral Vision/image.jpg"



        