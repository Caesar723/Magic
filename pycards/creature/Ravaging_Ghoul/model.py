
from game.type_cards.creature import Creature


class Ravaging_Ghoul(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Ravaging Ghoul"
        self.live:int=2
        self.power:int=2

        self.type_creature:str="Zombie Creature"
        self.type:str="Creature"

        self.mana_cost:str="1B"
        self.color:str="black"
        self.type_card:str="Zombie Creature"
        self.rarity:str="Uncommon"
        self.content:str="When Ravaging Ghoul enters the battlefield, target opponent loses 2 life unless they sacrifice a creature."
        self.image_path:str="cards/creature/Ravaging Ghoul/image.jpg"



        