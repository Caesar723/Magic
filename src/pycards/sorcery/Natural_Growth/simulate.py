from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Natural_Growth.model import Natural_Growth

@bind_card(Natural_Growth)
class Natural_Growth_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Target creature gets +2/+2 until end of turn.",

        "[CARD_NAME] gives target creature +2/+2 until end of turn.",

        "Target creature gets +2/+2 until the end of the turn.",

        "[CARD_NAME] grants target creature +2/+2 until end of turn.",

        "Choose target creature. It gets +2/+2 until end of turn.",

        "[CARD_NAME] causes target creature to get +2/+2 until end of turn.",

        "Until end of turn, target creature gets +2/+2.",

        "[CARD_NAME] buffs target creature with +2/+2 until end of turn.",

        "Target creature receives +2/+2 until end of turn.",

        "[CARD_NAME] gives a target creature +2/+2 until end of turn."
    ]
