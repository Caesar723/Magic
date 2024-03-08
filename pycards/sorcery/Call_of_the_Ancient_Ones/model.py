
from game.type_cards.sorcery import Sorcery


class Call_of_the_Ancient_Ones(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Call of the Ancient Ones"

        self.type:str="Sorcery"

        self.mana_cost:str="3BB"
        self.color:str="black"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Call of the Ancient Ones allows you to return target creature card from a graveyard to the battlefield under your control. That creature gains haste until end of turn and must be sacrificed at the beginning of the next end step."
        self.image_path:str="cards/sorcery/Call of the Ancient Ones/image.jpg"



        