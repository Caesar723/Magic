
from game.type_cards.sorcery import Sorcery


class Divine_Intervention(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Divine Intervention"

        self.type:str="Sorcery"

        self.mana_cost:str="2W"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Mythic Rare"
        self.content:str="Exile all nonland permanents. For each permanent exiled this way, its controller may search their library for a basic land card and put it onto the battlefield tapped."
        self.image_path:str="cards/sorcery/Divine Intervention/image.jpg"



        