from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Temporal_Reversal.model import Temporal_Reversal

@bind_card(Temporal_Reversal)
class Temporal_Reversal_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Return target nonland permanent to its owner's hand. You may untap up to two lands.",
        "[CARD_NAME] bounces a nonland permanent and lets you untap up to two lands.",
        "Return nonland permanent to hand. Untap up to two lands.",
        "Bounce target nonland permanent. Optionally untap two lands.",
        "[CARD_NAME]: bounce nonland; untap up to two lands.",
        "Send nonland permanent back to hand. You may untap two lands.",
        "Return a nonland to hand and untap up to two lands.",
        "With [CARD_NAME], bounce nonland permanent and untap lands.",
        "Target nonland permanent returns to hand. Untap up to two lands.",
        "[CARD_NAME] bounces a nonland and untaps up to two lands.",
    ]
