from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Voidwisp_Harbinger.model import Voidwisp_Harbinger

@bind_card(Voidwisp_Harbinger)
class Voidwisp_Harbinger_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Flash, Flying. When [CARD_NAME] enters the battlefield, you may scry 2.",

        "Flash, Flying. When [CARD_NAME] enters play, you may scry 2.",

        "Flash, Flying. As [CARD_NAME] enters the battlefield, you may scry 2.",

        "Flash, Flying. Upon entering the battlefield, [CARD_NAME] lets you scry 2.",

        "Flash, Flying. When [CARD_NAME] arrives, you may scry 2.",

        "Flash, Flying. When [CARD_NAME] enters the battlefield, you may scry two.",

        "Flash, Flying. When [CARD_NAME] enters the battlefield, you may look at the top two cards of your library and rearrange them.",

        "Flash, Flying. When [CARD_NAME] enters the battlefield, you may scry 2 (look at the top two cards, put any number on the bottom, rest on top).",

        "Flash, Flying. When [CARD_NAME] enters the battlefield, you may scry 2.",

    ]
