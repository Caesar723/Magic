
from game.type_cards.creature import Creature


class Flame_Tinkerer(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Flame Tinkerer"
        self.live:int=1
        self.power:int=2

        self.type_creature:str="Goblin Creature"
        self.type:str="Creature"

        self.mana_cost:str="1R"
        self.color:str="red"
        self.type_card:str="Goblin Creature"
        self.rarity:str="Common"
        self.content:str="When Flame Tinkerer enters the battlefield, you may pay R. If you do, it deals 1 damage to target creature."
        self.image_path:str="cards/creature/Flame Tinkerer/image.jpg"



        