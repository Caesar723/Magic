
from game.type_cards.instant import Instant


class Mystic_Tides(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Mystic Tides"

        self.type:str="Instant"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Counter target creature spell unless its controller pays 2."
        self.image_path:str="cards/Instant/Mystic Tides/image.jpg"
        
    
    def card_ability(self):
        super().card_ability()

        print("Mystic_Tides")
        


        