
from game.type_cards.creature import Creature


class Mistweaver_Drake(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Mistweaver Drake"
        self.live:int=1
        self.power:int=2

        self.type_creature:str="Creature - Elemental"
        self.type:str="Creature"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Creature - Elemental"
        self.rarity:str="Common"
        self.content:str="Flash (You may cast this spell any time you could cast an instant)"
        self.image_path:str="cards/creature/Mistweaver Drake/image.jpg"



        