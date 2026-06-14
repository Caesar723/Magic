from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Titan_Giant.model import Titan_Giant

@bind_card(Titan_Giant)
class Titan_Giant_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "When [CARD_NAME] enters the battlefield, destroy all other creatures with power less than 5.",

        "When [CARD_NAME] enters play, destroy all other creatures with power less than 5.",

        "As [CARD_NAME] enters the battlefield, destroy all other creatures with power less than 5.",

        "Upon entering the battlefield, [CARD_NAME] destroys all other creatures with power less than 5.",

        "When [CARD_NAME] arrives, destroy all other creatures with power less than 5.",

        "When [CARD_NAME] enters the battlefield, destroy every other creature with power less than 5.",

        "When [CARD_NAME] enters the battlefield, destroy all other creatures with power 4 or less.",

        "When [CARD_NAME] enters the battlefield, destroy all other creatures with power below 5.",

        "When [CARD_NAME] enters the battlefield, destroy all other creatures that have power less than 5.",

    ]
