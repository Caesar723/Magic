
from game.type_cards.sorcery import Sorcery


class Dark_Offering(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Dark Offering"

        self.type:str="Sorcery"

        self.mana_cost:str="1B"
        self.color:str="black"
        self.type_card:str="Sorcery"
        self.rarity:str="Common"
        self.content:str="Target player loses 2 life and you gain 2 life."
        self.image_path:str="cards/sorcery/Dark Offering/image.jpg"



        