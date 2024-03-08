
from game.type_cards.land import Land


class Volcanic_Fumaroles(Land):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Volcanic Fumaroles"

        self.type:str="Land"

        self.mana_cost:str=""
        self.color:str="red"
        self.type_card:str="Land"
        self.rarity:str="Rare"
        self.content:str="Volcanic Fumaroles enters the battlefield untapped and adds one red mana to your mana pool. You may tap Volcanic Fumaroles to deal 1 damage to target creature or player."
        self.image_path:str="cards/land/Volcanic Fumaroles/image.jpg"



        