
from game.type_cards.sorcery import Sorcery


class Call_to_Unity(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Call to Unity"

        self.type:str="Sorcery"

        self.mana_cost:str="1W"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Common"
        self.content:str="Create two 1/1 white Human creature tokens."
        self.image_path:str="cards/sorcery/Call to Unity/image.jpg"



        