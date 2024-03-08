
from game.type_cards.instant import Instant


class Arcane_Inferno(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Arcane Inferno"

        self.type:str="Instant"

        self.mana_cost:str="3R"
        self.color:str="red"
        self.type_card:str="Instant"
        self.rarity:str="Mythic Rare"
        self.content:str="Arcane Inferno deals 3 damage to any target. If you control a creature with power 5 or greater, Arcane Inferno deals 5 damage instead."
        self.image_path:str="cards/Instant/Arcane Inferno/image.jpg"



        