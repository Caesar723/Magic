from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Shadowtide_Leviathan.model import Shadowtide_Leviathan

@bind_card(Shadowtide_Leviathan)
class Shadowtide_Leviathan_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Islandwalk. When [CARD_NAME] enters the battlefield, you may return target nonland permanent an opponent controls to its owner's hand.",

        "Islandwalk. When [CARD_NAME] enters play, you may return target nonland permanent an opponent controls to its owner's hand.",

        "Islandwalk. As [CARD_NAME] enters the battlefield, you may return target nonland permanent an opponent controls to its owner's hand.",

        "Islandwalk. Upon entering the battlefield, [CARD_NAME] lets you return target nonland permanent an opponent controls to its owner's hand.",

        "Islandwalk. When [CARD_NAME] arrives, you may return target nonland permanent an opponent controls to its owner's hand.",

        "Islandwalk. When [CARD_NAME] enters the battlefield, you may bounce target nonland permanent an opponent controls.",

        "Islandwalk. When [CARD_NAME] enters the battlefield, you may return target nonland permanent an opponent controls to hand.",

        "Islandwalk. When [CARD_NAME] enters the battlefield, you may return a target nonland permanent an opponent controls to its owner's hand.",

        "Islandwalk. When [CARD_NAME] enters the battlefield, you may return target opposing nonland permanent to its owner's hand.",

    ]
