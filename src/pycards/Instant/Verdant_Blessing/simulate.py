from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Verdant_Blessing.model import Verdant_Blessing

@bind_card(Verdant_Blessing)
class Verdant_Blessing_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] allows you to search your library for a basic land card and put it onto the battlefield tapped. Then, shuffle your library.",
        "Search your library for a basic land and put it onto the battlefield tapped. Shuffle.",
        "[CARD_NAME] tutors a basic land onto the battlefield tapped, then shuffles.",
        "Find a basic land in your library, put it in play tapped, shuffle.",
        "With [CARD_NAME], search for basic land, play tapped, shuffle library.",
        "Search library for basic land, put onto battlefield tapped, shuffle.",
        "[CARD_NAME]: basic land tutor to battlefield tapped.",
        "Tutor basic land to battlefield tapped. Shuffle your library.",
        "Put a basic land from library onto battlefield tapped. Shuffle.",
        "[CARD_NAME] fetches a tapped basic land from your library.",
    ]
