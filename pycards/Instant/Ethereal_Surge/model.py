
from game.type_cards.instant import Instant


class Ethereal_Surge(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Ethereal Surge"

        self.type:str="Instant"

        self.mana_cost:str="UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Counter target spell with converted mana cost X. If that spell is countered this way, return it to its owner's hand instead of putting it into their graveyard."
        self.image_path:str="cards/Instant/Ethereal Surge/image.jpg"



        