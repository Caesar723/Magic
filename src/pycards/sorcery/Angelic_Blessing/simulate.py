from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Angelic_Blessing.model import Angelic_Blessing

@bind_card(Angelic_Blessing)
class Angelic_Blessing_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Target creature gets +3/+3 and gains vigilance until end of turn.",

        "[CARD_NAME] gives target creature +3/+3 and vigilance until end of turn.",

        "Target creature gets +3/+3 and gains vigilance until the end of the turn.",

        "[CARD_NAME] grants target creature +3/+3 and vigilance until end of turn.",

        "Choose target creature. It gets +3/+3 and gains vigilance until end of turn.",

        "[CARD_NAME] causes target creature to get +3/+3 and gain vigilance until end of turn.",

        "Until end of turn, target creature gets +3/+3 and has vigilance.",

        "[CARD_NAME] buffs target creature with +3/+3 and vigilance until end of turn.",

        "Target creature receives +3/+3 and gains vigilance until end of turn.",

        "[CARD_NAME] gives a target creature +3/+3 and vigilance until end of turn."
    ]
