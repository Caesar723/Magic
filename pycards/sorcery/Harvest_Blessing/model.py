
from game.type_cards.sorcery import Sorcery


class Harvest_Blessing(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Harvest Blessing"

        self.type:str="Sorcery"

        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Sorcery"
        self.rarity:str="Uncommon"
        self.content:str="Search your library for a basic land card, put it onto the battlefield tapped, then shuffle your library."
        self.image_path:str="cards/sorcery/Harvest Blessing/image.jpg"



        