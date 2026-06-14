from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Ethereal_Surge.model import Ethereal_Surge

@bind_card(Ethereal_Surge)
class Ethereal_Surge_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Counter target spell. If that spell is countered this way, return it to its owner's hand instead of putting it into their graveyard.",
        "[CARD_NAME] counters target spell and returns it to its owner's hand instead of the graveyard.",
        "Counter a spell. If countered this way, it goes to hand instead of graveyard.",
        "With [CARD_NAME], counter target spell; countered spells return to hand rather than graveyard.",
        "Counter target spell. On counter, return it to hand instead of graveyard.",
        "[CARD_NAME]: counter spell; bounced to hand instead of graveyard when countered.",
        "Counter target spell. If countered this way, owner puts it into their hand, not graveyard.",
        "Counter a spell and return it to its owner's hand if countered by [CARD_NAME].",
        "Target spell is countered and returned to its owner's hand instead of going to graveyard.",
        "[CARD_NAME] counters a spell and sends it back to hand rather than the graveyard.",
    ]
