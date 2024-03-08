
from game.type_cards.land import Land


class Luminous_Glade(Land):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Luminous Glade"

        self.type:str="Land"

        self.mana_cost:str=""
        self.color:str="gold"
        self.type_card:str="Land"
        self.rarity:str="Rare"
        self.content:str="Luminous Glade enters the battlefield untapped and adds one white mana to your mana pool. You may tap Luminous Glade to prevent the next 1 damage that would be dealt to target creature or player this turn."
        self.image_path:str="cards/land/Luminous Glade/image.jpg"



        