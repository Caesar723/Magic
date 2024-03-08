
from game.type_cards.instant import Instant


class Avenging_Light(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Avenging Light"

        self.type:str="Instant"

        self.mana_cost:str="3W"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Exile target nonland permanent. If it was a creature, you gain life equal to its power."
        self.image_path:str="cards/Instant/Avenging Light/image.jpg"



        