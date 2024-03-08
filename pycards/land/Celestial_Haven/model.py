
from game.type_cards.land import Land


class Celestial_Haven(Land):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Celestial Haven"

        self.type:str="Land"

        self.mana_cost:str=""
        self.color:str="gold"
        self.type_card:str="Land"
        self.rarity:str="Rare"
        self.content:str="Celestial Haven enters the battlefield untapped and adds one white mana to your mana pool. Additionally, you may pay 3 life and tap Celestial Haven to prevent all combat damage that would be dealt this turn."
        self.image_path:str="cards/land/Celestial Haven/image.jpg"



        