
from game.type_cards.instant import Instant


class Swift_Ward(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Swift Ward"

        self.type:str="Instant"

        self.mana_cost:str="1W"
        self.color:str="gold"
        self.type_card:str="Instant"
        self.rarity:str="Common"
        self.content:str="Target creature gets +1/+1 until end of turn and gains hexproof until end of turn."
        self.image_path:str="cards/Instant/Swift Ward/image.jpg"



        