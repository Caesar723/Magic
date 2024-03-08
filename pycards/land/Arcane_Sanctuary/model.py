
from game.type_cards.land import Land


class Arcane_Sanctuary(Land):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Arcane Sanctuary"

        self.type:str="Land"

        self.mana_cost:str=""
        self.color:str="black"
        self.type_card:str="Land"
        self.rarity:str="Rare"
        self.content:str="Arcane Sanctuary enters the battlefield untapped and adds one colorless mana to your mana pool. You may also tap Arcane Sanctuary and pay 2 mana to scry 1 and draw a card."
        self.image_path:str="cards/land/Arcane Sanctuary/image.jpg"



        