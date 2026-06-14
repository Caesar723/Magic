from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Nature_s_Embrace.model import Nature_s_Embrace

@bind_card(Nature_s_Embrace)
class Nature_s_Embrace_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Search your library for a creature card and put it onto the battlefield tapped. The creature enters as a 4/4. Then shuffle your library.",

        "[CARD_NAME] lets you search your library for a creature card, put it onto the battlefield tapped as a 4/4, then shuffle your library.",

        "Search your library for a creature card, put it onto the battlefield tapped with base power and toughness 4/4, then shuffle your library.",

        "[CARD_NAME] searches your library for a creature card, puts it onto the battlefield tapped as a 4/4 creature, then shuffles.",

        "Find a creature card in your library, put it onto the battlefield tapped as a 4/4, then shuffle your library.",

        "[CARD_NAME] finds a creature card in your library, puts it onto the battlefield tapped as a 4/4, then shuffles your library.",

        "Search your library for a creature card and put it onto the battlefield tapped. It enters the battlefield as a 4/4 creature. Shuffle your library.",

        "[CARD_NAME] allows you to search for a creature card, put it onto the battlefield tapped as a 4/4, and shuffle your library.",

        "Search for a creature card, put it onto the battlefield tapped as a 4/4 creature, then shuffle your library.",

        "[CARD_NAME] searches your library for a creature card, puts it onto the battlefield tapped with stats 4/4, then shuffles your library."
    ]
