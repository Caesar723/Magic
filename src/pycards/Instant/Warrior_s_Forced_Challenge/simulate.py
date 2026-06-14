from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Warrior_s_Forced_Challenge.model import Warrior_s_Forced_Challenge

@bind_card(Warrior_s_Forced_Challenge)
class Warrior_s_Forced_Challenge_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Counter target creature spell. Another target creature fights a creature you control.",
        "[CARD_NAME] counters a creature spell and makes another creature fight one you control.",
        "Counter creature spell. Another creature fights yours.",
        "With [CARD_NAME], counter creature spell and force a fight.",
        "Counter target creature spell. Another creature fights a creature you control.",
        "[CARD_NAME]: counter creature spell + fight.",
        "Counter a creature spell. Pick another creature to fight yours.",
        "Counter creature spell, then another target creature fights your creature.",
        "[CARD_NAME] counters creature spells and triggers a fight.",
        "Counter creature spell; another creature fights one you control.",
    ]
