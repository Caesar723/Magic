from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Blightsteel_Colossus.model import Blightsteel_Colossus

@bind_card(Blightsteel_Colossus)
class Blightsteel_Colossus_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Trample, Infect, Indestructible.",

        "Infect, Indestructible, Trample (damage to creatures is -1/-1 counters; damage to players is poison counters).",

        "Indestructible, Trample, Infect (can't be destroyed by damage or effects that say destroy).",

        "Infect. Trample. Indestructible.",

        "Indestructible, Infect, and Trample.",

        "Infect, Trample (this deals damage as -1/-1 counters to creatures and poison counters to players), Indestructible.",

        "Trample, Indestructible, Infect — this creature can't be destroyed by damage or destroy effects.",

        "Indestructible, Infect, Trample (immune to damage-based destruction and destroy effects).",

        "Infect, Indestructible, Trample (this creature can't be destroyed by damage or destroy effects).",

    ]
