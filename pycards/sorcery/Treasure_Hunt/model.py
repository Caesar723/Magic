
from game.type_cards.sorcery import Sorcery


class Treasure_Hunt(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Treasure Hunt"

        self.type:str="Sorcery"

        self.mana_cost:str="U"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Common"
        self.content:str="Reveal the top X cards of your library. Put all land cards revealed this way into your hand and the rest on the bottom of your library in any order."
        self.image_path:str="cards/sorcery/Treasure Hunt/image.jpg"



        