from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Eldritch_Rebirth.model import Eldritch_Rebirth

@bind_card(Eldritch_Rebirth)
class Eldritch_Rebirth_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] allows you to return all creature cards with converted mana cost 3 or less from your graveyard to the battlefield. If [CARD_NAME] was cast from your graveyard, you may return all creature cards with converted mana cost 4 or greater from your graveyard to the battlefield instead.",

        "Return every creature card with mana value 3 or less from your graveyard to the battlefield. If you cast [CARD_NAME] from your graveyard, you may return all creature cards with mana value 4 or greater from your graveyard instead.",

        "[CARD_NAME] returns all creature cards with CMC 3 or less from your graveyard to the battlefield. When cast from your graveyard, you may return all creature cards with CMC 4 or greater instead.",

        "Put all creature cards with converted mana cost 3 or less from your graveyard onto the battlefield. If [CARD_NAME] was cast from your graveyard, you may put all creature cards with converted mana cost 4 or greater onto the battlefield instead.",

        "[CARD_NAME] lets you return all graveyard creature cards costing 3 or less to the battlefield. If cast from your graveyard, you may return all graveyard creature cards costing 4 or more instead.",

        "Return all creature cards with mana value 3 or less from your graveyard to play. If [CARD_NAME] was cast from your graveyard, you may return all creature cards with mana value 4 or greater instead.",

        "[CARD_NAME] brings back every creature card with converted mana cost 3 or less from your graveyard. If cast from your graveyard, you may bring back every creature card with converted mana cost 4 or greater instead.",

        "All creature cards with CMC 3 or less in your graveyard return to the battlefield. If [CARD_NAME] was cast from your graveyard, you may return all creature cards with CMC 4 or greater instead.",

        "[CARD_NAME] returns all creature cards costing 3 or less from your graveyard to the battlefield. When cast from your graveyard, you may return all creature cards costing 4 or more instead.",

        "Return each creature card with converted mana cost 3 or less from your graveyard to the battlefield. If [CARD_NAME] was cast from your graveyard, you may return each creature card with converted mana cost 4 or greater instead."
    ]
