
from game.type_cards.creature import Creature


class Raging_Firekin(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Raging Firekin"
        self.live:int=2
        self.power:int=3

        self.type_creature:str="Elemental Creature - Elemental"
        self.type:str="Creature"

        self.mana_cost:str="1R"
        self.color:str="red"
        self.type_card:str="Elemental Creature - Elemental"
        self.rarity:str="Uncommon"
        self.content:str="Trample (This creature can deal excess combat damage to the player or planeswalker it's attacking.)"
        self.image_path:str="cards/creature/Raging Firekin/image.jpg"



        