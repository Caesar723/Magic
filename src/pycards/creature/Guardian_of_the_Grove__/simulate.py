from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Guardian_of_the_Grove__.model import Guardian_of_the_Grove__

@bind_card(Guardian_of_the_Grove__)
class Guardian_of_the_Grove___Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Whenever [CARD_NAME] enters the battlefield, you may search your library for a basic Forest card and put it onto the battlefield tapped.",

        "When [CARD_NAME] enters the battlefield, you may search your library for a basic Forest and put it onto the battlefield tapped.",

        "As [CARD_NAME] enters the battlefield, you may search your library for a basic Forest card and put it onto the battlefield tapped.",

        "Upon entering the battlefield, [CARD_NAME] lets you search for a basic Forest and put it onto the battlefield tapped.",

        "When [CARD_NAME] arrives, you may search your library for a basic Forest card and put it onto the battlefield tapped.",

        "When [CARD_NAME] enters the battlefield, you may find a basic Forest in your library and put it onto the battlefield tapped.",

        "When [CARD_NAME] enters the battlefield, you may search your library for a basic Forest and place it onto the battlefield tapped.",

        "When [CARD_NAME] enters the battlefield, you may search for a basic Forest card and put it onto the battlefield tapped.",

        "When [CARD_NAME] enters the battlefield, you may search your library for a basic Forest and put it on the battlefield tapped.",

    ]
