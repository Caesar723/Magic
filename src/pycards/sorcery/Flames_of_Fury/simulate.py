from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Flames_of_Fury.model import Flames_of_Fury

@bind_card(Flames_of_Fury)
class Flames_of_Fury_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] deals 3 damage to target creature or player. If you control a Mountain, [CARD_NAME] deals 1 additional damage.",

        "Deal 3 damage to target creature or player. If you control a Mountain, deal 1 additional damage.",

        "[CARD_NAME] deals 3 damage to any creature or player. If you control a Mountain, it deals 1 more damage.",

        "Deal three damage to target creature or player. If you control a Mountain, deal one additional damage.",

        "[CARD_NAME] inflicts 3 damage on target creature or player. If you control a Mountain, it deals 1 extra damage.",

        "Deal 3 damage to a target creature or player. If you control a Mountain, [CARD_NAME] deals 1 additional damage.",

        "[CARD_NAME] deals 3 damage to target creature or player, plus 1 additional damage if you control a Mountain.",

        "Target creature or player takes 3 damage. If you control a Mountain, [CARD_NAME] deals 1 additional damage.",

        "Deal 3 damage to target creature or player. When you control a Mountain, [CARD_NAME] deals 1 additional damage.",

        "[CARD_NAME] hits target creature or player for 3 damage, dealing 1 additional damage if you control a Mountain."
    ]
