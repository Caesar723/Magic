
from game.type_cards.creature import Creature


class Celestial_Seraph(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Celestial Seraph"
        self.live:int=5
        self.power:int=5

        self.type_creature:str="Angel Creature - Angel"
        self.type:str="Creature"

        self.mana_cost:str="3WWW"
        self.color:str="gold"
        self.type_card:str="Angel Creature - Angel"
        self.rarity:str="Mythic Rare"
        self.content:str="Flying, Lifelink (Damage dealt by this creature also causes you to gain that much life), Whenever Celestial Seraph attacks, you may exile target nonland permanent an opponent controls until Celestial Seraph leaves the battlefield."
        self.image_path:str="cards/creature/Celestial Seraph/image.jpg"



        