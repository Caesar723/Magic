
from game.type_cards.sorcery import Sorcery


class Mystic_Reversal(Sorcery):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Mystic Reversal"

        self.type:str="Sorcery"

        self.mana_cost:str="1U"
        self.color:str="blue"
        self.type_card:str="Sorcery"
        self.rarity:str="Rare"
        self.content:str="Counter target spell unless its controller pays 3. If the spell is countered this way, exile it instead of putting it into its owner's graveyard. "
        self.image_path:str="cards/sorcery/Mystic Reversal/image.jpg"



        