from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Primal_Surge.model import Primal_Surge

@bind_card(Primal_Surge)
class Primal_Surge_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Target player shuffles their hand and graveyard into their library, then draws that many cards. They may play an additional land this turn.",
        "[CARD_NAME] makes a player shuffle hand and graveyard into library, redraw, and play an extra land.",
        "Target player resets hand and graveyard into library, redraws, and may play an extra land.",
        "Shuffle hand and graveyard into library, draw that many. Extra land this turn.",
        "[CARD_NAME]: full hand/graveyard shuffle and redraw; extra land allowed.",
        "Target player shuffles hand and graveyard into deck, draws equal number, extra land this turn.",
        "Reset a player's hand and graveyard into library and redraw. They may play another land.",
        "With [CARD_NAME], shuffle hand/graveyard into library, redraw, play extra land.",
        "Target player shuffles hand and graveyard in, draws same count, may play additional land.",
        "[CARD_NAME] shuffles hand and graveyard into library, redraws, grants extra land play.",
    ]
