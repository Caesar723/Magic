
from game.type_cards.instant import Instant


class Shadow_Snare(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Shadow Snare"

        self.type:str="Instant"

        self.mana_cost:str="2B"
        self.color:str="black"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Target creature gets -3/-3 until end of turn."
        self.image_path:str="cards/Instant/Shadow Snare/image.jpg"



        