from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Sylvan_Harmonist.model import Sylvan_Harmonist

@bind_card(Sylvan_Harmonist)
class Sylvan_Harmonist_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "When [CARD_NAME] enters the battlefield, you may search your library for a basic land card and put it onto the battlefield tapped. If you do, shuffle your library.",

        "When [CARD_NAME] enters play, you may search your library for a basic land and put it onto the battlefield tapped. If you do, shuffle.",

        "As [CARD_NAME] enters the battlefield, you may search for a basic land, put it onto the battlefield tapped, then shuffle if you do.",

        "Upon entering the battlefield, [CARD_NAME] lets you search for a basic land, put it onto the battlefield tapped, and shuffle if you do.",

        "When [CARD_NAME] arrives, you may search your library for a basic land, put it onto the battlefield tapped, then shuffle.",

        "When [CARD_NAME] enters the battlefield, you may find a basic land, put it onto the battlefield tapped, then shuffle your library if you do.",

        "When [CARD_NAME] enters the battlefield, you may search your library for a basic land card, place it onto the battlefield tapped, then shuffle if you do.",

        "When [CARD_NAME] enters the battlefield, you may search for a basic land, put it on the battlefield tapped, and shuffle if you do.",

        "When [CARD_NAME] enters the battlefield, you may search your library for a basic land card, put it onto the battlefield tapped. Shuffle if you do.",

    ]
