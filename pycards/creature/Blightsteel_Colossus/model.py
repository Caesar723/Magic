
from game.type_cards.creature import Creature


class Blightsteel_Colossus(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Blightsteel Colossus"
        self.live:int=11
        self.power:int=11

        self.type_creature:str="Artifact Creature - Golem"
        self.type:str="Creature"

        self.mana_cost:str="12"
        self.color:str="colorless"
        self.type_card:str="Artifact Creature - Golem"
        self.rarity:str="Mythic Rare"
        self.content:str="Trample, Infect (This creature deals damage to creatures in the form of -1/-1 counters and to players in the form of poison counters.), Indestructible (This creature can't be destroyed by damage or effects that say \"destroy.\")"
        self.image_path:str="cards/creature/Blightsteel Colossus/image.jpg"



        