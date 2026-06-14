from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Astral_Resurgence.model import Astral_Resurgence

@bind_card(Astral_Resurgence)
class Astral_Resurgence_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Return a creature cards from your graveyard to the battlefield. It gains lifelink until end of turn.",
        "[CARD_NAME] returns a creature card from your graveyard to the battlefield with lifelink until end of turn.",
        "Put a creature card from your graveyard onto the battlefield. It has lifelink until end of turn.",
        "Return a creature from your graveyard to the battlefield. It gains lifelink this turn.",
        "[CARD_NAME] reanimates a creature from your graveyard; it gains lifelink until end of turn.",
        "Bring a creature card from your graveyard back to the battlefield with lifelink until end of turn.",
        "Return one creature card from your graveyard to the battlefield. It gains lifelink until end of turn.",
        "[CARD_NAME] puts a creature from your graveyard onto the battlefield with lifelink this turn.",
        "Reanimate a creature from your graveyard. It gains lifelink until end of turn.",
        "Return a creature card from graveyard to battlefield; it has lifelink until end of turn.",
    ]
