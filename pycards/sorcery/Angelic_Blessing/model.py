
from game.type_cards.sorcery import Sorcery


class Angelic_Blessing(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Angelic Blessing"

        self.type:str="Sorcery"

        self.mana_cost:str="1W"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Uncommon"
        self.content:str="Target creature gets +3/+3 and gains vigilance until end of turn."
        self.image_path:str="cards/sorcery/Angelic Blessing/image.jpg"



        