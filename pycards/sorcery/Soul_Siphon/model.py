
from game.type_cards.sorcery import Sorcery


class Soul_Siphon(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Soul Siphon"

        self.type:str="Sorcery"

        self.mana_cost:str="1B"
        self.color:str="black"
        self.type_card:str="Sorcery"
        self.rarity:str="Uncommon"
        self.content:str="Target opponent sacrifices a creature. You gain life equal to that creature's power."
        self.image_path:str="cards/sorcery/Soul Siphon/image.jpg"



        