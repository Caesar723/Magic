from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Thornwood_Sentinel.model import Thornwood_Sentinel

@bind_card(Thornwood_Sentinel)
class Thornwood_Sentinel_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Reach (This creature can block creatures with flying).",

        "Reach.",

        "Reach (can block creatures with flying).",

        "Reach (blocks flying creatures).",

        "Reach (this can block creatures with flying).",

        "Reach (able to block flying creatures).",

        "Reach (may block creatures with flying).",

        "Reach (can block flyers).",

        "Reach (this creature blocks creatures with flying).",

    ]
