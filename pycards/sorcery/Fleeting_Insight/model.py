
from game.type_cards.sorcery import Sorcery


class Fleeting_Insight(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Fleeting Insight"

        self.type:str="Sorcery"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Common"
        self.content:str="Draw a card, then discard a card."
        self.image_path:str="cards/sorcery/Fleeting Insight/image.jpg"



        