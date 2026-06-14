from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Ephemeral_Bolt.model import Ephemeral_Bolt

@bind_card(Ephemeral_Bolt)
class Ephemeral_Bolt_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] deals 1 damage to target creature or player. If a creature dealt damage this way dies this turn, you may draw a card.",
        "Deal 1 damage to target creature or player. If a creature damaged this way dies this turn, draw a card.",
        "[CARD_NAME] hits a creature or player for 1. Draw a card if that creature dies this turn.",
        "Choose target creature or player. Deal 1 damage. You may draw if the creature dies this turn.",
        "Deal 1 damage to a creature or player. Draw a card if a creature damaged this way dies this turn.",
        "[CARD_NAME]: 1 damage to creature or player; draw if the creature dies this turn.",
        "Strike target creature or player for 1 damage. If it dies this turn, you may draw a card.",
        "Inflict 1 damage on a creature or player. Draw a card if that creature dies this turn.",
        "[CARD_NAME] deals 1 to a creature or player; optional draw if the creature dies this turn.",
        "One damage to target creature or player. You may draw a card if that creature dies this turn.",
    ]
