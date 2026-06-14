from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Mystic_Convergence.model import Mystic_Convergence

@bind_card(Mystic_Convergence)
class Mystic_Convergence_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Prevent all combat damage that would be dealt this turn. At the beginning of your next main phase, add X mana in any combination of colors to your mana pool, where X is the amount of combat damage prevented this way.",
        "[CARD_NAME] prevents all combat damage this turn; next main phase add X mana of any colors, X = damage prevented.",
        "Prevent all combat damage this turn. Next main phase, add mana equal to damage prevented in any colors.",
        "With [CARD_NAME], stop all combat damage; gain mana next main phase equal to damage prevented.",
        "No combat damage this turn. Next main phase, add X mana (any colors), X = prevented combat damage.",
        "[CARD_NAME]: fog all combat damage; mana reward next main phase based on prevented damage.",
        "Prevent all combat damage. At your next main phase, add X mana in any combination, X = prevented damage.",
        "Combat damage is prevented this turn. Next main phase, gain mana equal to prevented damage.",
        "[CARD_NAME] fogs combat and converts prevented damage into mana next main phase.",
        "Prevent combat damage this turn; add X colored mana next main phase where X is damage prevented.",
    ]
