from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Night_Stalker__.model import Night_Stalker__

@bind_card(Night_Stalker__)
class Night_Stalker___Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Menace (This creature can't be blocked except by two or more creatures).",

        "Menace.",

        "Menace (can't be blocked except by two or more creatures).",

        "Menace (requires two or more blockers).",

        "Menace (must be blocked by two or more creatures).",

        "Menace (only blockable by two or more creatures).",

        "Menace (this can't be blocked except by two or more creatures).",

        "Menace (needs at least two creatures to block it).",

        "Menace (opponents need two or more creatures to block this).",

    ]
