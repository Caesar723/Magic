
from game.type_cards.land import Land


class Sanctum_of_Eternal_Flames(Land):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Sanctum of Eternal Flames"

        self.type:str="Land"

        self.mana_cost:str=""
        self.color:str="red"
        self.type_card:str="Land"
        self.rarity:str="Rare"
        self.content:str="Sanctum of Eternal Flames enters the battlefield untapped and adds one red mana to your mana pool. You may also tap Sanctum of Eternal Flames and pay 2 mana to deal 2 damage to any target."
        self.image_path:str="cards/land/Sanctum of Eternal Flames/image.jpg"



        