
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.player import Player
    from game.card import Card
 
from game.type_cards.instant import Instant


class Blazing_Reversal(Instant):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.name:str="Blazing Reversal"

        self.type:str="Instant"

        self.mana_cost:str="1UR"
        self.color:str="red"
        self.type_card:str="Instant"
        self.rarity:str="Rare"
        self.content:str="Change the target of target spell or ability with a single target. You may choose new targets for the redirection. If Blazing Reversal is in your graveyard, you may cast it by sacrificing a Mountain and paying its flashback cost. If you do, exile it as it resolves."
        self.image_path:str="cards/Instant/Blazing Reversal/image.jpg"



        