
from game.type_cards.sorcery import Sorcery


class Mystic_Insight(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Mystic Insight"

        self.type:str="Sorcery"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Common"
        self.content:str="Scry 2, then draw a card."
        self.image_path:str="cards/sorcery/Mystic Insight/image.jpg"



        