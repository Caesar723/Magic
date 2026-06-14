from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Thunderstrike.model import Thunderstrike

@bind_card(Thunderstrike)
class Thunderstrike_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Choose one creature. [CARD_NAME] deals 8 damage to that creature. If that creature dies, [CARD_NAME] deals the same amount of damage to each opponent.",

        "Choose a creature. Deal 8 damage to it. If it dies, deal 8 damage to each opponent.",

        "[CARD_NAME] deals 8 damage to a chosen creature. If that creature dies, each opponent takes 8 damage.",

        "Select one creature. [CARD_NAME] deals 8 damage to it. If that creature is destroyed, each opponent takes the same amount of damage.",

        "Choose one creature and deal 8 damage to it. If that creature dies, deal the same amount of damage to every opponent.",

        "[CARD_NAME] targets one creature and deals 8 damage to it. If that creature dies, each opponent takes 8 damage.",

        "Pick one creature. [CARD_NAME] deals 8 damage to that creature. If it dies, each opponent takes equal damage.",

        "Choose a creature. [CARD_NAME] deals 8 damage to it. If that creature dies, deal 8 damage to each opponent.",

        "Target one creature with [CARD_NAME], dealing 8 damage to it. If that creature dies, each opponent takes the same amount of damage.",

        "Choose one creature. Deal 8 damage to that creature. If it dies, [CARD_NAME] deals 8 damage to each opponent."
    ]
