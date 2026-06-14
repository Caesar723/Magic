from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Soul_Devourer.model import Soul_Devourer

@bind_card(Soul_Devourer)
class Soul_Devourer_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Whenever a creature dies, [CARD_NAME] gets +1/+1 counters equal to the power of that creature.",

        "Whenever a creature dies, [CARD_NAME] gains +1/+1 counters equal to that creature's power.",

        "Each time a creature dies, [CARD_NAME] gets +1/+1 counters equal to the power of that creature.",

        "When a creature dies, [CARD_NAME] receives +1/+1 counters equal to the power of that creature.",

        "Whenever any creature dies, [CARD_NAME] gets +1/+1 counters equal to the power of that creature.",

        "Whenever a creature dies, [CARD_NAME] grows by +1/+1 counters equal to the power of that creature.",

        "Whenever a creature dies, [CARD_NAME] gets +1/+1 counters matching the power of that creature.",

        "Whenever a creature dies, [CARD_NAME] gains counters equal to that creature's power.",

        "On a creature's death, [CARD_NAME] gets +1/+1 counters equal to the power of that creature.",

    ]
