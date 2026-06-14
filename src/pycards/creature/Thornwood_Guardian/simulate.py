from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Thornwood_Guardian.model import Thornwood_Guardian

@bind_card(Thornwood_Guardian)
class Thornwood_Guardian_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Reach, Trample (This creature can block creatures with flying, and it can deal excess combat damage to the player or planeswalker it's attacking).",

        "Reach, Trample.",

        "Reach, Trample (can block flyers and deal excess combat damage).",

        "Reach. Trample (blocks flying creatures and deals excess damage).",

        "Reach, Trample (can block creatures with flying and deal excess combat damage).",

        "Reach, Trample (blocks flying and deals excess damage to attacked player or planeswalker).",

        "Reach, Trample (can block flying creatures; excess damage goes to the player or planeswalker).",

        "Reach, Trample (can block flyers; deals excess combat damage to the player or planeswalker it's attacking).",

        "Reach, Trample (can block creatures with flying and deal excess combat damage to the attacked player or planeswalker).",

    ]
