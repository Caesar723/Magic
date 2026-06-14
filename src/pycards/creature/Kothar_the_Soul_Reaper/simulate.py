from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Kothar_the_Soul_Reaper.model import Kothar_the_Soul_Reaper

@bind_card(Kothar_the_Soul_Reaper)
class Kothar_the_Soul_Reaper_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "When [CARD_NAME] enters the battlefield, each opponent sacrifices a creature at random. Whenever a creature dies, [CARD_NAME] gets a +1/+1 counter.",

        "When [CARD_NAME] enters play, each opponent sacrifices a random creature. Whenever a creature dies, [CARD_NAME] gets a +1/+1 counter.",

        "As [CARD_NAME] enters the battlefield, each opponent sacrifices a creature randomly. Whenever a creature dies, [CARD_NAME] gets a +1/+1 counter.",

        "Upon entering the battlefield, [CARD_NAME] forces each opponent to sacrifice a random creature. Whenever a creature dies, [CARD_NAME] gets a +1/+1 counter.",

        "When [CARD_NAME] arrives, each opponent sacrifices a random creature. Whenever a creature dies, [CARD_NAME] gets a +1/+1 counter.",

        "When [CARD_NAME] enters the battlefield, each opponent sacrifices a creature at random. When a creature dies, [CARD_NAME] gets a +1/+1 counter.",

        "When [CARD_NAME] enters the battlefield, each opponent sacrifices a random creature. Each time a creature dies, [CARD_NAME] gets a +1/+1 counter.",

        "When [CARD_NAME] enters the battlefield, each opponent sacrifices a creature at random. Whenever any creature dies, [CARD_NAME] gets a +1/+1 counter.",

        "When [CARD_NAME] enters the battlefield, each opponent sacrifices a random creature. Whenever a creature dies, [CARD_NAME] receives a +1/+1 counter.",

    ]
