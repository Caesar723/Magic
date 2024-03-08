
from game.type_cards.creature import Creature


class Aetherweaver(Creature):
    
    
    def __init__(self) -> None:#
        super().__init__()

        self.name:str="Aetherweaver"
        self.live:int=2
        self.power:int=2

        self.type_creature:str="Human Wizard"
        self.type:str="Creature"

        self.mana_cost:str="3U"
        self.color:str="blue"
        self.type_card:str="Human Wizard"
        self.rarity:str="Mythic Rare"
        self.content:str="When Aetherweaver enters the battlefield, you may return target artifact or enchantment from your graveyard to your hand."
        self.image_path:str="cards/creature/Aetherweaver/image.jpg"



        