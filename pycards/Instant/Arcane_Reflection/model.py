
from game.type_cards.instant import Instant


class Arcane_Reflection(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Arcane Reflection"

        self.type:str="Instant"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Arcane Reflection allows you to return target instant or sorcery card from your graveyard to your hand."
        self.image_path:str="cards/Instant/Arcane Reflection/image.jpg"



        