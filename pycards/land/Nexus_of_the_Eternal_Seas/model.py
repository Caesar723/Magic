
from game.type_cards.land import Land


class Nexus_of_the_Eternal_Seas(Land):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Nexus of the Eternal Seas"

        self.type:str="Land"

        self.mana_cost:str=""
        self.color:str="blue"
        self.type_card:str="Land"
        self.rarity:str="Rare"
        self.content:str="Nexus of the Eternal Seas enters the battlefield untapped and adds one blue mana to your mana pool. You may tap Nexus of the Eternal Seas to return target creature to its owner's hand."
        self.image_path:str="cards/land/Nexus of the Eternal Seas/image.jpg"



        