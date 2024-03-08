
from game.type_cards.instant import Instant


class Veiled_Concealment(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Veiled Concealment"

        self.type:str="Instant"

        self.mana_cost:str="U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Target creature is unblockable until end of turn. Draw a card."
        self.image_path:str="cards/Instant/Veiled Concealment/image.jpg"



        