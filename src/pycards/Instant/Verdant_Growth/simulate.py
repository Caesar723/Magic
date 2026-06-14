from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Verdant_Growth.model import Verdant_Growth

@bind_card(Verdant_Growth)
class Verdant_Growth_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Target creature gets +4/+4 until end of turn. If it's a Treefolk creature, it gains trample until end of turn.",
        "[CARD_NAME] gives +4/+4 until end of turn; Treefolk also gain trample.",
        "Choose a creature. +4/+4 this turn. Treefolk get trample too.",
        "Buff target creature +4/+4. Treefolk also trample until end of turn.",
        "[CARD_NAME]: +4/+4; Treefolk trample until end of turn.",
        "Target creature gets +4/+4. Treefolk creatures also gain trample.",
        "+4/+4 until end of turn. Treefolk gain trample.",
        "With [CARD_NAME], +4/+4 buff and trample for Treefolk.",
        "Give +4/+4 until end of turn. Treefolk also trample.",
        "[CARD_NAME] grows a creature +4/+4 and grants Treefolk trample.",
    ]
