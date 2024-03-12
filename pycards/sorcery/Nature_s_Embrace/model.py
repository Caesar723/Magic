
from game.type_cards.sorcery import Sorcery


class Nature_s_Embrace(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Nature's Embrace"

        self.type:str="Sorcery"

        self.mana_cost:str="3G"
        self.color:str="green"
        self.type_card:str="Sorcery"
        self.rarity:str="Mythic Rare"
        self.content:str="Search your library for a creature card and put it onto the battlefield tapped. Then shuffle your library."
        self.image_path:str="cards/sorcery/Nature's Embrace/image.jpg"



        