
from game.type_cards.instant import Instant


class Ethereal_Convergence(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Ethereal Convergence"

        self.type:str="Instant"

        self.mana_cost:str="3UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Return all creatures to their owners' hands. You may search your library for a creature card, reveal it, put it into your hand, then shuffle your library."
        self.image_path:str="cards/Instant/Ethereal Convergence/image.jpg"



        