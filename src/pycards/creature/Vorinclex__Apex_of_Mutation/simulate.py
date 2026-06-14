from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Vorinclex__Apex_of_Mutation.model import Vorinclex__Apex_of_Mutation

@bind_card(Vorinclex__Apex_of_Mutation)
class Vorinclex__Apex_of_Mutation_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Trample, Infect. Whenever you cast a spell, proliferate for three random permanents. Whenever an opponent proliferates, they must pay 2 life for each permanent.",

        "Trample, Infect. Each time you cast a spell, proliferate for three random permanents. Whenever an opponent proliferates, they pay 2 life per permanent.",

        "Trample, Infect. When you cast a spell, proliferate for three random permanents. When an opponent proliferates, they must pay 2 life for each permanent.",

        "Trample, Infect. Whenever you cast a spell, proliferate three random permanents. Whenever an opponent proliferates, they must pay 2 life for each permanent.",

        "Trample, Infect. On casting a spell, proliferate for three random permanents. On opponent proliferating, they must pay 2 life per permanent.",

        "Trample, Infect. Whenever you cast a spell, proliferate for three random permanents. Whenever an opponent proliferates, they must pay two life for each permanent.",

        "Trample, Infect. Whenever you cast a spell, proliferate three random permanents. Whenever an opponent proliferates, they must pay 2 life for each permanent proliferated.",

        "Trample, Infect. Whenever you cast a spell, proliferate for three random permanents. Whenever an opponent proliferates, they must pay 2 life for each permanent affected.",

        "Trample, Infect. Whenever you cast a spell, proliferate for three random permanents. Whenever an opponent proliferates, they must pay 2 life for each permanent.",

    ]
