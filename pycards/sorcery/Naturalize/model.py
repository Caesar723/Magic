
from game.type_cards.sorcery import Sorcery


class Naturalize(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Naturalize"

        self.type:str="Sorcery"

        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Sorcery"
        self.rarity:str="Common"
        self.content:str="Destroy target artifact or enchantment."
        self.image_path:str="cards/sorcery/Naturalize/image.jpg"



        