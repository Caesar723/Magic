from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Thornwood_Ranger.model import Thornwood_Ranger

@bind_card(Thornwood_Ranger)
class Thornwood_Ranger_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Reach. When [CARD_NAME] enters the battlefield, another target creature you control gets +1/+0 until end of turn.",

        "Reach. When [CARD_NAME] enters play, another target creature you control gets +1/+0 until end of turn.",

        "Reach. As [CARD_NAME] enters the battlefield, another target creature you control gets +1/+0 until end of turn.",

        "Reach. Upon entering the battlefield, [CARD_NAME] gives another target creature you control +1/+0 until end of turn.",

        "Reach. When [CARD_NAME] arrives, another target creature you control gets +1/+0 until end of turn.",

        "Reach. When [CARD_NAME] enters the battlefield, target another creature you control gets +1/+0 until end of turn.",

        "Reach. When [CARD_NAME] enters the battlefield, another creature you control gets +1/+0 until end of turn.",

        "Reach. When [CARD_NAME] enters the battlefield, another target creature you control gains +1/+0 until end of turn.",

        "Reach. When [CARD_NAME] enters the battlefield, another target creature you control receives +1/+0 until end of turn.",

    ]
