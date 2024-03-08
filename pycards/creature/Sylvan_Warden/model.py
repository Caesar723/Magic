
from game.type_cards.creature import Creature


class Sylvan_Warden(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Sylvan Warden"
        self.live:int=4
        self.power:int=2

        self.type_creature:str="Elf Shaman"
        self.type:str="Creature"

        self.mana_cost:str="4G"
        self.color:str="green"
        self.type_card:str="Elf Shaman"
        self.rarity:str="Rare"
        self.content:str="When Sylvan Warden enters the battlefield, you may search your library for a basic land card and put it onto the battlefield tapped. If you do, shuffle your library."
        self.image_path:str="cards/creature/Sylvan Warden/image.jpg"



        