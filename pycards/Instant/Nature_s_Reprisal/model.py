
from game.type_cards.instant import Instant


class Nature_s_Reprisal(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Nature's Reprisal"

        self.type:str="Instant"

        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Destroy target artifact or enchantment."
        self.image_path:str="cards/Instant/Nature's Reprisal/image.jpg"



        