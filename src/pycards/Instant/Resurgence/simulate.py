from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Resurgence.model import Resurgence

@bind_card(Resurgence)
class Resurgence_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Creatures you control gain double strike and lifelink until end of turn. Return random creature card with converted mana cost 3 or less from your graveyard to the battlefield.",
        "[CARD_NAME] gives your creatures double strike and lifelink, and reanimates a random CMC-3-or-less creature.",
        "Your creatures get double strike and lifelink this turn. Return random cheap creature from graveyard.",
        "Double strike and lifelink for your creatures. Reanimate random creature with CMC 3 or less.",
        "[CARD_NAME]: double strike + lifelink; reanimate random CMC≤3 creature.",
        "Buff your creatures with double strike and lifelink. Bring back random low-cost creature from graveyard.",
        "Until end of turn, double strike and lifelink on your creatures. Reanimate random CMC 3 or less creature.",
        "With [CARD_NAME], double strike and lifelink for your team plus random cheap reanimation.",
        "Your creatures gain double strike and lifelink. Return random creature (CMC ≤3) from graveyard.",
        "[CARD_NAME] empowers your creatures and reanimates a random cheap creature from graveyard.",
    ]
