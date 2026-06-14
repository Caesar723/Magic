from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Sage_of_the_Ancient_Grove.model import Sage_of_the_Ancient_Grove

@bind_card(Sage_of_the_Ancient_Grove)
class Sage_of_the_Ancient_Grove_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Reach. When [CARD_NAME] enters the battlefield, you may search your library for a basic land card, put it onto the battlefield tapped, then shuffle your library.",

        "Reach. When [CARD_NAME] enters play, you may search your library for a basic land, put it onto the battlefield tapped, then shuffle.",

        "Reach. As [CARD_NAME] enters the battlefield, you may search for a basic land, put it onto the battlefield tapped, then shuffle.",

        "Reach. Upon entering the battlefield, [CARD_NAME] lets you search for a basic land, put it onto the battlefield tapped, then shuffle.",

        "Reach. When [CARD_NAME] arrives, you may search your library for a basic land, put it onto the battlefield tapped, then shuffle.",

        "Reach. When [CARD_NAME] enters the battlefield, you may find a basic land, put it onto the battlefield tapped, then shuffle your library.",

        "Reach. When [CARD_NAME] enters the battlefield, you may search your library for a basic land card, place it onto the battlefield tapped, then shuffle.",

        "Reach. When [CARD_NAME] enters the battlefield, you may search for a basic land card, put it on the battlefield tapped, then shuffle.",

        "Reach. When [CARD_NAME] enters the battlefield, you may search your library for a basic land, put it onto the battlefield tapped, and shuffle.",

    ]
