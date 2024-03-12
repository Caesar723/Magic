
from game.type_cards.creature import Creature


class Emberheart_Salamander(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Emberheart Salamander"
        self.live:int=2
        self.power:int=4

        self.type_creature:str="Salamander Creature - Salamander"
        self.type:str="Creature"

        self.mana_cost:str="2RR"
        self.color:str="red"
        self.type_card:str="Salamander Creature - Salamander"
        self.rarity:str="Uncommon"
        self.content:str="Trample (This creature can deal excess combat damage to the player or planeswalker it's attacking.), When Emberheart Salamander enters the battlefield, it deals 2 damage to any target."
        self.image_path:str="cards/creature/Emberheart Salamander/image.jpg"



        