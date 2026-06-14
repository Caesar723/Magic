from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Mystic_Rupture.model import Mystic_Rupture

@bind_card(Mystic_Rupture)
class Mystic_Rupture_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Return all nonland permanents to their owner's hands. Each player may search their library for a basic land card, put it onto the battlefield tapped, then shuffle their library.",
        "[CARD_NAME] bounces all nonlands; each player may fetch a basic land tapped.",
        "All nonland permanents return to hand. Each player may put a basic land onto the battlefield tapped.",
        "Mass bounce nonlands. Each player may search for a basic land and play it tapped.",
        "[CARD_NAME]: bounce all nonlands; optional basic land for each player tapped.",
        "Return every nonland permanent to hand. Players may tutor basic lands onto battlefield tapped.",
        "Bounce all nonlands. Each player may find a basic land and put it in play tapped.",
        "With [CARD_NAME], return all nonlands to hand; each player may drop a tapped basic land.",
        "All nonland permanents to hand. Each player may search library for tapped basic land.",
        "[CARD_NAME] returns nonlands to hand and lets each player fetch a tapped basic land.",
    ]
