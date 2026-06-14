from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Merfolk_Wayfinder.model import Merfolk_Wayfinder

@bind_card(Merfolk_Wayfinder)
class Merfolk_Wayfinder_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "When [CARD_NAME] enters the battlefield, you may scry 1.",

        "When [CARD_NAME] enters play, you may scry 1.",

        "As [CARD_NAME] enters the battlefield, you may scry 1.",

        "Upon entering the battlefield, [CARD_NAME] lets you scry 1.",

        "When [CARD_NAME] arrives, you may scry 1.",

        "When [CARD_NAME] enters the battlefield, you may scry one.",

        "When [CARD_NAME] enters the battlefield, you may look at the top card of your library and put it on the bottom.",

        "When [CARD_NAME] enters the battlefield, you may scry 1. (Look at the top card of your library. You may put it on the bottom.)",

        "When [CARD_NAME] enters the battlefield, you may scry 1 (look at the top of your library, optionally put it on the bottom).",

    ]
