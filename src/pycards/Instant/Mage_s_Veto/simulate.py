from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Mage_s_Veto.model import Mage_s_Veto

@bind_card(Mage_s_Veto)
class Mage_s_Veto_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Counter target spell. If that spell's mana cost is less than 3, search your library for a Sorcery card and put it into your hand.",
        "[CARD_NAME] counters target spell; if mana cost under 3, tutor a Sorcery to hand.",
        "Counter a spell. If its mana cost is less than 3, search for a Sorcery and put it in your hand.",
        "With [CARD_NAME], counter target spell and tutor a Sorcery if the spell cost less than 3.",
        "Counter target spell. Cheap spells (cost <3) let you search for a Sorcery.",
        "[CARD_NAME]: counter spell; fetch Sorcery if countered spell cost less than 3.",
        "Counter target spell. When mana cost is under 3, find a Sorcery in your library.",
        "Counter a spell. If cost less than 3, search library for Sorcery to hand.",
        "[CARD_NAME] counters and may tutor a Sorcery when the spell's mana cost is less than 3.",
        "Counter target spell. Mana cost below 3 triggers a Sorcery search.",
    ]
