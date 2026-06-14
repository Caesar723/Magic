from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Natural_Harmony.model import Natural_Harmony

@bind_card(Natural_Harmony)
class Natural_Harmony_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Search your library for a basic land card and put it onto the battlefield tapped, then shuffle your library. You gain 2 life.",

        "[CARD_NAME] lets you search for a basic land, put it onto the battlefield tapped, shuffle, and gain 2 life.",

        "Search your library for a basic land card, put it onto the battlefield tapped, shuffle your library, and gain 2 life.",

        "[CARD_NAME] searches your library for a basic land, puts it onto the battlefield tapped, shuffles, and you gain 2 life.",

        "Find a basic land in your library, put it onto the battlefield tapped, shuffle, then gain 2 life.",

        "[CARD_NAME] finds a basic land, puts it onto the battlefield tapped, shuffles your library, and you gain 2 life.",

        "Search for a basic land card, put it onto the battlefield tapped, shuffle your library. You gain 2 life.",

        "[CARD_NAME] allows you to search for a basic land, put it onto the battlefield tapped, shuffle, and gain 2 life.",

        "Search your library for a basic land and put it onto the battlefield tapped. Shuffle. Gain 2 life.",

        "[CARD_NAME] searches for a basic land, puts it onto the battlefield tapped, shuffles your library, and you gain 2 life."
    ]
