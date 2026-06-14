from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Mist_Djinn.model import Mist_Djinn

@bind_card(Mist_Djinn)
class Mist_Djinn_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] can block any number of creatures.",

        "[CARD_NAME] may block any number of creatures.",

        "[CARD_NAME] is able to block any number of creatures.",

        "[CARD_NAME] can block as many creatures as needed.",

        "[CARD_NAME] can block any number of attacking creatures.",

        "[CARD_NAME] can block unlimited creatures.",

        "[CARD_NAME] can block any number of creatures simultaneously.",

        "[CARD_NAME] can block any number of creatures at once.",

        "[CARD_NAME] can block any number of creatures in combat.",

    ]
