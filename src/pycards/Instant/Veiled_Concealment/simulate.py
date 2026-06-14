from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Veiled_Concealment.model import Veiled_Concealment

@bind_card(Veiled_Concealment)
class Veiled_Concealment_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Target creature is unblockable until end of turn. Draw a card.",
        "[CARD_NAME] makes target creature unblockable until end of turn and lets you draw a card.",
        "Choose a creature. It can't be blocked this turn. Draw a card.",
        "Target creature gains unblockable until end of turn. Draw a card.",
        "[CARD_NAME]: unblockable until end of turn, draw a card.",
        "Make a creature unblockable this turn. Draw a card.",
        "Target creature can't be blocked until end of turn. Draw a card.",
        "With [CARD_NAME], grant unblockable and draw a card.",
        "Unblockable on target creature this turn. Draw a card.",
        "[CARD_NAME] conceals a creature (unblockable) and draws you a card.",
    ]
