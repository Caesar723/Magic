from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Time_Reversal.model import Time_Reversal

@bind_card(Time_Reversal)
class Time_Reversal_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Undo all spells and effects from your opponent.",
        "[CARD_NAME] undoes all spells and effects from your opponent.",
        "Reverse all of your opponent's spells and effects.",
        "Undo opponent's spells and effects.",
        "[CARD_NAME]: undo opponent spells and effects.",
        "Roll back all opponent spells and effects.",
        "With [CARD_NAME], undo everything your opponent has cast or triggered.",
        "Cancel all opponent spells and effects.",
        "Reverse opponent's active spells and effects.",
        "[CARD_NAME] reverses all opponent spells and effects.",
    ]
