
from game.type_cards.instant import Instant


class Naturalize(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Naturalize"

        self.type:str="Instant"

        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Destroy target artifact or enchantment."
        self.image_path:str="cards/Instant/Naturalize/image.jpg"



        