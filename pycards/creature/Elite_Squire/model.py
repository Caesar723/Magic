
from game.type_cards.creature import Creature


class Elite_Squire(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Elite Squire"
        self.live:int=2
        self.power:int=2

        self.type_creature:str="Human Knight"
        self.type:str="Creature"

        self.mana_cost:str="1W"
        self.color:str="gold"
        self.type_card:str="Human Knight"
        self.rarity:str="Uncommon"
        self.content:str="Vigilance (This creature doesn't tap when it attacks)"
        self.image_path:str="cards/creature/Elite Squire/image.jpg"



        