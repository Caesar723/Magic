
from game.type_cards.instant import Instant


class Phantasmal_Distortion(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Phantasmal Distortion"

        self.type:str="Instant"

        self.mana_cost:str="1UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Until end of turn, target creature you control becomes a copy of another target creature, except it retains its abilities. Return that creature to its owner's hand at the beginning of the next end step."
        self.image_path:str="cards/Instant/Phantasmal Distortion/image.jpg"



        