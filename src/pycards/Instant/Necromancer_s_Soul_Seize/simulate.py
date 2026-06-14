from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Necromancer_s_Soul_Seize.model import Necromancer_s_Soul_Seize

@bind_card(Necromancer_s_Soul_Seize)
class Necromancer_s_Soul_Seize_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Counter target creature spell. If the spell is countered this way, exile a card from your library, then return a card of the same type from your graveyard to your hand.",
        "[CARD_NAME] counters creature spells; on counter, exile a library card and return same-type card from graveyard to hand.",
        "Counter a creature spell. If countered, exile from library and return matching type from graveyard to hand.",
        "With [CARD_NAME], counter creature spell; exile library card and retrieve same type from graveyard.",
        "Counter target creature spell. On counter, exile library card, return same-type card from graveyard.",
        "[CARD_NAME]: counter creature spell; library exile + graveyard return of same type.",
        "Counter creature spells. If countered, exile from library and get same type back from graveyard.",
        "Counter a creature spell. Exile a library card and return a graveyard card of the same type.",
        "[CARD_NAME] counters creature spells and swaps library/graveyard cards of matching type.",
        "Counter creature spell; exile from library, return same-type card from graveyard to hand.",
    ]
