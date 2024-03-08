
from game.type_cards.sorcery import Sorcery


class Divine_Offering(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Divine Offering"

        self.type:str="Sorcery"

        self.mana_cost:str="1W"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Common"
        self.content:str="Destroy target artifact. Its controller gains 3 life."
        self.image_path:str="cards/sorcery/Divine Offering/image.jpg"



        