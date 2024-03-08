
from game.type_cards.instant import Instant


class Vengeful_Retribution(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Vengeful Retribution"

        self.type:str="Instant"

        self.mana_cost:str="4B"
        self.color:str="black"
        self.type_card:str="Instant"
        self.rarity:str="Mythic Rare"
        self.content:str="Target opponent sacrifices two creatures. If a creature was sacrificed this way, Vengeful Retribution deals damage to any target equal to the total power of the sacrificed creatures."
        self.image_path:str="cards/Instant/Vengeful Retribution/image.jpg"



        