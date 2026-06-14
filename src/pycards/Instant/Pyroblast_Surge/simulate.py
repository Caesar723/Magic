from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Pyroblast_Surge.model import Pyroblast_Surge

@bind_card(Pyroblast_Surge)
class Pyroblast_Surge_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] deals 3 damage to target creature or player. If you control an untapped Mountain, [CARD_NAME] deals 1 additional damage.",
        "Deal 3 damage to creature or player. +1 damage if you control an untapped Mountain.",
        "[CARD_NAME] hits creature or player for 3, plus 1 if you have an untapped Mountain.",
        "Choose creature or player. Deal 3 damage, +1 with untapped Mountain.",
        "Fire 3 at creature or player; 4 total with untapped Mountain.",
        "[CARD_NAME]: 3 damage to creature or player; +1 with untapped Mountain.",
        "Deal 3 to creature or player. Untapped Mountain adds 1 damage.",
        "[CARD_NAME] deals 3 (+1 with untapped Mountain) to creature or player.",
        "Three damage to creature or player, four if Mountain is untapped.",
        "Target creature or player takes 3 damage, or 4 with an untapped Mountain.",
    ]
