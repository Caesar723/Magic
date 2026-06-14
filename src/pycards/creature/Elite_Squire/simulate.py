from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Elite_Squire.model import Elite_Squire

@bind_card(Elite_Squire)
class Elite_Squire_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Vigilance (This creature doesn't tap when it attacks).",

        "Vigilance.",

        "Vigilance (doesn't tap to attack).",

        "Vigilance (this doesn't tap when attacking).",

        "Vigilance (attacks without tapping).",

        "Vigilance (can attack without tapping).",

        "Vigilance (untapped while attacking).",

        "Vigilance (this creature attacks without tapping).",

        "Vigilance (doesn't tap when it attacks).",

    ]
