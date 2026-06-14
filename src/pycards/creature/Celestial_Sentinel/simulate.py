from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Celestial_Sentinel.model import Celestial_Sentinel

@bind_card(Celestial_Sentinel)
class Celestial_Sentinel_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Flying, Vigilance.",

        "Flying and Vigilance.",

        "Flying. Vigilance.",

        "Flying, Vigilance (this creature doesn't tap when attacking).",

        "Flying, Vigilance — can attack without tapping.",

        "Flying, Vigilance (attacks without tapping).",

        "Flying, Vigilance (doesn't tap to attack).",

        "Flying, Vigilance (this doesn't tap when it attacks).",

        "Flying, Vigilance (untapped while attacking).",

    ]
