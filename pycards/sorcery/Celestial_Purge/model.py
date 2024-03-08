
from game.type_cards.sorcery import Sorcery


class Celestial_Purge(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Celestial Purge"

        self.type:str="Sorcery"

        self.mana_cost:str="1W"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Exile target black or red permanent."
        self.image_path:str="cards/sorcery/Celestial Purge/image.jpg"



        