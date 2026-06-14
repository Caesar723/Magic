from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Celestial_Convergence.model import Celestial_Convergence

@bind_card(Celestial_Convergence)
class Celestial_Convergence_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Exile target permanent. If that permanent's mana value is 3 or less, its controller gains life equal to its mana value.",
        "[CARD_NAME] exiles target permanent. If its mana value is 3 or less, its controller gains life equal to that value.",
        "Exile a permanent. If mana value 3 or less, its controller gains life equal to its mana value.",
        "Remove target permanent from the game. Controller gains life equal to mana value if it's 3 or less.",
        "[CARD_NAME]: exile target permanent; if mana value ≤3, controller gains life equal to mana value.",
        "Exile target permanent. When mana value is 3 or less, its controller gains life equal to that number.",
        "Banish target permanent. If its mana value is 3 or less, its controller gains life equal to its mana value.",
        "With [CARD_NAME], exile a permanent; low-cost permanents (MV 3 or less) grant life equal to mana value.",
        "Exile target permanent. Controller gains life equal to mana value if that value is 3 or less.",
        "[CARD_NAME] exiles a permanent and grants life equal to mana value when that value is 3 or less.",
    ]
