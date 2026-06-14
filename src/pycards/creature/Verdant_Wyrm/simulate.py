from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Verdant_Wyrm.model import Verdant_Wyrm

@bind_card(Verdant_Wyrm)
class Verdant_Wyrm_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Trample. When [CARD_NAME] enters the battlefield, you may search your library for a land card, put it onto the battlefield tapped, then shuffle your library.",

        "Trample. When [CARD_NAME] enters play, you may search your library for a land, put it onto the battlefield tapped, then shuffle.",

        "Trample. As [CARD_NAME] enters the battlefield, you may search for a land, put it onto the battlefield tapped, then shuffle.",

        "Trample. Upon entering the battlefield, [CARD_NAME] lets you search for a land, put it onto the battlefield tapped, then shuffle.",

        "Trample. When [CARD_NAME] arrives, you may search your library for a land, put it onto the battlefield tapped, then shuffle.",

        "Trample. When [CARD_NAME] enters the battlefield, you may find a land, put it onto the battlefield tapped, then shuffle your library.",

        "Trample. When [CARD_NAME] enters the battlefield, you may search your library for a land card, place it onto the battlefield tapped, then shuffle.",

        "Trample. When [CARD_NAME] enters the battlefield, you may search for a land, put it on the battlefield tapped, then shuffle.",

        "Trample. When [CARD_NAME] enters the battlefield, you may search your library for a land card, put it onto the battlefield tapped, and shuffle.",

    ]
