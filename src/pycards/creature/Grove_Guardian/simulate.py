from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Grove_Guardian.model import Grove_Guardian

@bind_card(Grove_Guardian)
class Grove_Guardian_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Reach, Hexproof (This creature can't be the target of spells or abilities your opponents control).",

        "Hexproof, Reach.",

        "Hexproof, Reach (can't be targeted by opponents' spells or abilities).",

        "Hexproof. Reach (opponents can't target this with spells or abilities).",

        "Reach, Hexproof (this can't be the target of opposing spells or abilities).",

        "Hexproof, Reach (immune to opposing targeting).",

        "Reach, Hexproof (opponents cannot target this creature).",

        "Hexproof, Reach (not targetable by opponent spells or abilities).",

        "Reach, Hexproof (your opponents can't target this).",

    ]
