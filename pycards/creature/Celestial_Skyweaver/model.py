
from game.type_cards.creature import Creature


class Celestial_Skyweaver(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Celestial Skyweaver"
        self.live:int=5
        self.power:int=2

        self.type_creature:str="Spirit Creature - Spirit"
        self.type:str="Creature"

        self.mana_cost:str="2WW"
        self.color:str="gold"
        self.type_card:str="Spirit Creature - Spirit"
        self.rarity:str="Rare"
        self.content:str="Flying, Whenever you cast an enchantment spell, you may tap target creature an opponent controls."
        self.image_path:str="cards/creature/Celestial Skyweaver/image.jpg"



        