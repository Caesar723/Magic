from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Rogue_s_Trickery.model import Rogue_s_Trickery

@bind_card(Rogue_s_Trickery)
class Rogue_s_Trickery_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Counter target spell. If the spell is countered this way, you gain this card.",
        "[CARD_NAME] counters target spell; if countered, you gain control of [CARD_NAME].",
        "Counter a spell. If countered this way, you gain this card.",
        "With [CARD_NAME], counter target spell and keep the card if you counter it.",
        "Counter target spell. On counter, you gain [CARD_NAME].",
        "[CARD_NAME]: counter spell; gain this card when countered.",
        "Counter a spell. Successful counter lets you gain [CARD_NAME].",
        "Counter target spell. If countered, you gain this card permanently.",
        "[CARD_NAME] counters and rewards you with itself when counter succeeds.",
        "Counter spell; gain [CARD_NAME] if countered this way.",
    ]
