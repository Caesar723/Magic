
from game.type_cards.sorcery import Sorcery


class Celestial_Renewal(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Celestial Renewal"

        self.type:str="Sorcery"

        self.mana_cost:str="3GW"
        self.color:str="gold"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Celestial Renewal allows you to return all creature cards from your graveyard to the battlefield. Those creatures gain hexproof until end of turn."
        self.image_path:str="cards/sorcery/Celestial Renewal/image.jpg"



        