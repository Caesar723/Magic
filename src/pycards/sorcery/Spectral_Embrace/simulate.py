from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Spectral_Embrace.model import Spectral_Embrace

@bind_card(Spectral_Embrace)
class Spectral_Embrace_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] gives all creatures you control +2/+2 until end of turn and prevents all damage that would be dealt to them this turn.",

        "Creatures you control get +2/+2 until end of turn and can't be dealt damage this turn.",

        "[CARD_NAME] grants all creatures you control +2/+2 until end of turn and prevents damage dealt to them this turn.",

        "Until end of turn, creatures you control get +2/+2 and prevent all damage that would be dealt to them.",

        "[CARD_NAME] buffs all creatures you control with +2/+2 until end of turn and shields them from all damage this turn.",

        "All creatures you control get +2/+2 until end of turn. Prevent all damage that would be dealt to them this turn.",

        "[CARD_NAME] gives your creatures +2/+2 until end of turn and prevents all damage dealt to them this turn.",

        "Creatures you control gain +2/+2 until end of turn. All damage that would be dealt to them this turn is prevented.",

        "[CARD_NAME] causes creatures you control to get +2/+2 until end of turn and prevents all damage to them this turn.",

        "Until end of turn, all creatures you control get +2/+2 and prevent all damage that would be dealt to them."
    ]
