from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Earthquake_Tremor.model import Earthquake_Tremor

@bind_card(Earthquake_Tremor)
class Earthquake_Tremor_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Destroy three creature permanents randomly. For each permanent destroyed this way, create a 3/3 Elemental creature token.",

        "[CARD_NAME] randomly destroys three creature permanents. For each one destroyed this way, create a 3/3 Elemental creature token.",

        "Destroy three random creature permanents. For each permanent destroyed this way, create a 3/3 Elemental creature token.",

        "[CARD_NAME] destroys three creature permanents at random. For each permanent destroyed, create a 3/3 Elemental creature token.",

        "Three random creature permanents are destroyed. For each permanent destroyed this way, create a 3/3 Elemental creature token.",

        "[CARD_NAME] randomly destroys three creatures. For each creature destroyed this way, create a 3/3 Elemental creature token.",

        "Destroy three creature permanents chosen at random. For each one destroyed, create a 3/3 Elemental creature token.",

        "[CARD_NAME] destroys three random creature permanents and creates a 3/3 Elemental creature token for each one destroyed.",

        "Randomly destroy three creature permanents. For each permanent destroyed this way, create a 3/3 Elemental token.",

        "[CARD_NAME] randomly destroys three creature permanents. For each permanent destroyed this way, you create a 3/3 Elemental creature token."
    ]
