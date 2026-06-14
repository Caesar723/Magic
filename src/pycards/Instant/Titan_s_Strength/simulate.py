from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Titan_s_Strength.model import Titan_s_Strength

@bind_card(Titan_s_Strength)
class Titan_s_Strength_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Until end of turn, your creatures get +4/+4 and Trample.",
        "[CARD_NAME] gives your creatures +4/+4 and trample until end of turn.",
        "Your creatures get +4/+4 and trample this turn.",
        "+4/+4 and trample for all creatures you control until end of turn.",
        "[CARD_NAME]: +4/+4 and trample on your creatures until end of turn.",
        "Buff all your creatures +4/+4 with trample this turn.",
        "Until end of turn, +4/+4 and trample on your creatures.",
        "With [CARD_NAME], your team gets +4/+4 and trample until end of turn.",
        "All creatures you control gain +4/+4 and trample until end of turn.",
        "[CARD_NAME] empowers your creatures with +4/+4 and trample this turn.",
    ]
