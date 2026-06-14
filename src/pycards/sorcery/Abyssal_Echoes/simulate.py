from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Abyssal_Echoes.model import Abyssal_Echoes

@bind_card(Abyssal_Echoes)
class Abyssal_Echoes_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Search your library for a creature card with a mana value of 7 or greater and put it onto the battlefield.",

        "[CARD_NAME] lets you search your library for a creature card with mana value 7 or greater and put it onto the battlefield.",

        "Search your library for a creature card with converted mana cost 7 or greater and put it onto the battlefield.",

        "[CARD_NAME] searches your library for a creature with mana value 7 or greater and puts it onto the battlefield.",

        "Find a creature card with mana value 7 or greater in your library and put it onto the battlefield.",

        "[CARD_NAME] finds a creature card costing 7 or more in your library and puts it onto the battlefield.",

        "Search your library for a creature card with mana value 7 or greater, then put it onto the battlefield.",

        "[CARD_NAME] allows you to search for a creature card with mana value 7 or greater and put it onto the battlefield.",

        "Search for a creature card with mana value 7 or greater and put it onto the battlefield.",

        "[CARD_NAME] searches your library for a creature card with mana value 7 or greater and puts it onto the battlefield."
    ]
