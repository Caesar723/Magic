
from game.type_cards.sorcery import Sorcery


class Mindful_Reflection(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Mindful Reflection"

        self.type:str="Sorcery"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Uncommon"
        self.content:str="Draw two cards, then discard a card."
        self.image_path:str="cards/sorcery/Mindful Reflection/image.jpg"



        