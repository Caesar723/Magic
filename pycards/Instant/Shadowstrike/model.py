
from game.type_cards.instant import Instant


class Shadowstrike(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Shadowstrike"

        self.type:str="Instant"

        self.mana_cost:str="1B"
        self.color:str="black"
        self.type_card:str="Instant"
        self.rarity:str="Uncommon"
        self.content:str="Destroy target tapped creature. If a creature was destroyed this way, you may draw a card."
        self.image_path:str="cards/Instant/Shadowstrike/image.jpg"



        