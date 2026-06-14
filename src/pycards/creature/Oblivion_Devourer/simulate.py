from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Oblivion_Devourer.model import Oblivion_Devourer

@bind_card(Oblivion_Devourer)
class Oblivion_Devourer_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Menace. When [CARD_NAME] attacks, you may sacrifice another creature. If you do, target player discards two cards.",

        "Menace. When [CARD_NAME] attacks, you may sacrifice another creature you control. If you do, target player discards two cards.",

        "Menace. On attack, [CARD_NAME] lets you sacrifice another creature. If you do, target player discards two cards.",

        "Menace. Whenever [CARD_NAME] attacks, you may sacrifice another creature. If you do, target player discards two cards.",

        "Menace. When [CARD_NAME] attacks, you may sacrifice a different creature. If you do, target player discards two cards.",

        "Menace. When [CARD_NAME] attacks, you may sacrifice another creature. If you do, that target player discards two cards.",

        "Menace. When [CARD_NAME] attacks, you may sacrifice another creature. If you do, target player discards 2 cards.",

        "Menace. When [CARD_NAME] attacks, you may sacrifice another creature. If you do, a target player discards two cards.",

        "Menace. When [CARD_NAME] attacks, you may sacrifice another creature. If you do, target player must discard two cards.",

    ]
