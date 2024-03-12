
from game.type_cards.creature import Creature


class Thornroot_Druid(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Thornroot Druid"
        self.live:int=2
        self.power:int=2

        self.type_creature:str="Elf Druid"
        self.type:str="Creature"

        self.mana_cost:str="1G"
        self.color:str="green"
        self.type_card:str="Elf Druid"
        self.rarity:str="Uncommon"
        self.content:str="When Thornroot Druid enters the battlefield, you may search your library for a basic land card, reveal it, put it into your hand, then shuffle your library."
        self.image_path:str="cards/creature/Thornroot Druid/image.jpg"



        