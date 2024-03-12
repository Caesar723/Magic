
from game.type_cards.creature import Creature


class Vorinclex__Apex_of_Mutation(Creature):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Vorinclex, Apex of Mutation"
        self.live:int=6
        self.power:int=6

        self.type_creature:str="Legendary Creature - Phyrexian Mutant"
        self.type:str="Creature"

        self.mana_cost:str="3GG"
        self.color:str="green"
        self.type_card:str="Legendary Creature - Phyrexian Mutant"
        self.rarity:str="Mythic Rare"
        self.content:str="Trample, Infect, and whenever you cast a spell, proliferate. Whenever an opponent proliferates, they must pay 2 life for each permanent type they've chose (Artifact, creature, enchantment, land, planeswalker, or any combination thereof)."
        self.image_path:str="cards/creature/Vorinclex, Apex of Mutation/image.jpg"



        