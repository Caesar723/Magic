
from game.type_cards.land import Land


class Mystic_Reflection_Pool(Land):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Mystic Reflection Pool"

        self.type:str="Land"

        self.mana_cost:str=""
        self.color:str="blue"
        self.type_card:str="Land"
        self.rarity:str="Rare"
        self.content:str="Mystic Reflection Pool enters the battlefield untapped and adds one blue mana to your mana pool. Additionally, you may tap Mystic Reflection Pool and pay 1 mana to scry 2, then draw a card."
        self.image_path:str="cards/land/Mystic Reflection Pool/image.jpg"



        