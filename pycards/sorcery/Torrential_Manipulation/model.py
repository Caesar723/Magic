
from game.type_cards.sorcery import Sorcery


class Torrential_Manipulation(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Torrential Manipulation"

        self.type:str="Sorcery"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Mythic Rare"
        self.content:str="Return target nonland permanent to its owner's hand. You may cast an instant or sorcery spell without paying its mana cost."
        self.image_path:str="cards/sorcery/Torrential Manipulation/image.jpg"



        