from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Wizard_s_Time_Warp.model import Wizard_s_Time_Warp

@bind_card(Wizard_s_Time_Warp)
class Wizard_s_Time_Warp_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Counter target spell. Its controller discards a card.",
        "[CARD_NAME] counters target spell and makes its controller discard a card.",
        "Counter a spell. Controller discards a card.",
        "With [CARD_NAME], counter target spell; controller discards.",
        "Counter target spell. Its controller discards one card.",
        "[CARD_NAME]: counter spell; controller discards.",
        "Counter a spell. Force controller to discard.",
        "Counter target spell. Spell controller discards a card.",
        "[CARD_NAME] counters and forces a discard from the spell's controller.",
        "Counter spell; controller discards a card.",
    ]
