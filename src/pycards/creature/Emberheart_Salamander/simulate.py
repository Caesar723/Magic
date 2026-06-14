from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Emberheart_Salamander.model import Emberheart_Salamander

@bind_card(Emberheart_Salamander)
class Emberheart_Salamander_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Trample. When [CARD_NAME] enters the battlefield, it deals 2 damage to any target.",

        "Trample. When [CARD_NAME] enters play, it deals 2 damage to any target.",

        "Trample. As [CARD_NAME] enters the battlefield, it deals 2 damage to any target.",

        "Trample. Upon entering the battlefield, [CARD_NAME] deals 2 damage to any target.",

        "Trample. When [CARD_NAME] arrives, it deals 2 damage to any target.",

        "Trample. When [CARD_NAME] enters the battlefield, deal 2 damage to any target.",

        "Trample. When [CARD_NAME] enters the battlefield, it deals two damage to any target.",

        "Trample. When [CARD_NAME] enters the battlefield, it inflicts 2 damage on any target.",

        "Trample. When [CARD_NAME] enters the battlefield, it deals 2 damage to a target of your choice.",

    ]
