
from game.type_cards.creature import Creature


class Mistweaver_Adept(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Mistweaver Adept"
        self.live:int=1
        self.power:int=2

        self.type_creature:str="Human Wizard"
        self.type:str="Creature"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Human Wizard"
        self.rarity:str="Uncommon"
        self.content:str="When Mistweaver Adept enters the battlefield, you may return target creature to its owner's hand. If you do, scry 2."
        self.image_path:str="cards/creature/Mistweaver Adept/image.jpg"



        