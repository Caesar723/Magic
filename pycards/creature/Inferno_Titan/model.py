
from game.type_cards.creature import Creature


class Inferno_Titan(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Inferno Titan"
        self.live:int=6
        self.power:int=6

        self.type_creature:str="Elemental Creature"
        self.type:str="Creature"

        self.mana_cost:str="3RR"
        self.color:str="red"
        self.type_card:str="Elemental Creature"
        self.rarity:str="Mythic Rare"
        self.content:str="When Inferno Titan enters the battlefield, it deals 3 damage divided as you choose among one, two, or three target creatures and/or players."
        self.image_path:str="cards/creature/Inferno Titan/image.jpg"



        