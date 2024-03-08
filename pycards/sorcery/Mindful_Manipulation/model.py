
from game.type_cards.sorcery import Sorcery


class Mindful_Manipulation(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Mindful Manipulation"

        self.type:str="Sorcery"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Uncommon"
        self.content:str="Draw two cards, then put one card from your hand on top of your library."
        self.image_path:str="cards/sorcery/Mindful Manipulation/image.jpg"



        