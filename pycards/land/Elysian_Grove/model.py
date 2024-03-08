
from game.type_cards.land import Land


class Elysian_Grove(Land):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Elysian Grove"

        self.type:str="Land"

        self.mana_cost:str=""
        self.color:str="green"
        self.type_card:str="Land"
        self.rarity:str="Rare"
        self.content:str="Elysian Grove enters the battlefield untapped and adds one green mana to your mana pool. You may tap Elysian Grove to untap target land."
        self.image_path:str="cards/land/Elysian Grove/image.jpg"



        