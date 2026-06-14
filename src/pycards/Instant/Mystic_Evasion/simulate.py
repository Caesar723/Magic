from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Mystic_Evasion.model import Mystic_Evasion

@bind_card(Mystic_Evasion)
class Mystic_Evasion_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Return target attacking creature to its owner's hand. Draw a card.",
        "[CARD_NAME] bounces target attacking creature and lets you draw a card.",
        "Choose target attacking creature. Return it to hand. Draw a card.",
        "Bounce an attacking creature to its owner's hand. Draw a card.",
        "[CARD_NAME]: return attacking creature to hand, draw a card.",
        "Send target attacking creature back to hand. Draw a card.",
        "Return attacking creature to hand, then draw with [CARD_NAME].",
        "Target attacking creature returns to hand. You draw a card.",
        "With [CARD_NAME], bounce an attacker and draw a card.",
        "Return one attacking creature to its owner's hand. Draw a card.",
    ]
