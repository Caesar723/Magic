from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Mystic_Insight.model import Mystic_Insight

@bind_card(Mystic_Insight)
class Mystic_Insight_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Scry 3, then draw a card.",
        "[CARD_NAME] lets you scry 3, then draw a card.",
        "Scry three, then draw one.",
        "With [CARD_NAME], look at the top three cards, then draw.",
        "Scry 3 and draw a card.",
        "[CARD_NAME]: scry 3, draw a card.",
        "Look at top three, arrange them, then draw a card.",
        "Scry 3, then draw with [CARD_NAME].",
        "You scry 3, then draw a card.",
        "[CARD_NAME] scrys 3 then draws you a card.",
    ]
