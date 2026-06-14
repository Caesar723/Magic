from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Ethereal_Reversal.model import Ethereal_Reversal

@bind_card(Ethereal_Reversal)
class Ethereal_Reversal_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Return target nonland permanent to its owner's hand. You may cast a spell with converted mana cost equal to or less than the returned card's from your hand without paying its mana cost.",
        "[CARD_NAME] bounces a nonland permanent; you may cast a spell from hand for free if its CMC is equal or less.",
        "Return a nonland permanent to hand. You may cast a spell from your hand without paying mana if CMC is low enough.",
        "Bounce target nonland permanent. Cast a spell from hand for free if its mana cost is equal or less than the bounced card.",
        "[CARD_NAME]: bounce nonland permanent; free cast from hand if CMC ≤ returned card's.",
        "Return nonland permanent to hand. Optionally cast a spell from hand without paying if CMC is equal or lower.",
        "Send a nonland permanent back to hand. You may cast a cheaper-or-equal spell from hand for free.",
        "With [CARD_NAME], bounce a nonland permanent and possibly cast a spell from hand without paying.",
        "Return target nonland permanent to hand. Free cast a spell from hand with CMC equal or less.",
        "[CARD_NAME] returns a nonland permanent and may let you cast a spell from hand without paying mana.",
    ]
