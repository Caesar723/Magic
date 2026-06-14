from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Chronostrider.model import Chronostrider

@bind_card(Chronostrider)
class Chronostrider_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Flash, Haste. When [CARD_NAME] enters the battlefield, you may take an extra turn after this one.",

        "Flash, Haste. When [CARD_NAME] enters play, you may take an extra turn after this one.",

        "Flash, Haste. As [CARD_NAME] enters the battlefield, you may take an extra turn after this one.",

        "Flash, Haste. Upon entering the battlefield, [CARD_NAME] lets you take an extra turn after this one.",

        "Flash, Haste. When [CARD_NAME] arrives, you may take an extra turn after this one.",

        "Flash, Haste. When [CARD_NAME] enters the battlefield, you may gain an extra turn after this one.",

        "Flash, Haste. When [CARD_NAME] enters the battlefield, you may take another turn after this one ends.",

        "Flash, Haste. When [CARD_NAME] enters the battlefield, you may take an additional turn after this one.",

        "Flash, Haste. When [CARD_NAME] enters the battlefield, you may take an extra turn following this one.",

    ]
