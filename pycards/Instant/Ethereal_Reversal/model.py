
from game.type_cards.instant import Instant


class Ethereal_Reversal(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Ethereal Reversal"

        self.type:str="Instant"

        self.mana_cost:str="2UU"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Return target nonland permanent to its owner's hand. You may cast a spell with converted mana cost equal to or less than the returned card's from your hand without paying its mana cost."
        self.image_path:str="cards/Instant/Ethereal Reversal/image.jpg"



        