from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Chaos_Unleashed.model import Chaos_Unleashed

@bind_card(Chaos_Unleashed)
class Chaos_Unleashed_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] deals 3 damage to each creature and each player.",

        "Deal 3 damage to every creature and every player.",

        "[CARD_NAME] inflicts 3 damage on each creature and each player.",

        "Each creature and each player takes 3 damage.",

        "[CARD_NAME] deals three damage to all creatures and all players.",

        "Deal 3 damage to each creature on the battlefield and each player.",

        "[CARD_NAME] hits every creature and every player for 3 damage.",

        "All creatures and all players take 3 damage.",

        "[CARD_NAME] deals 3 damage to each creature and each player in the game.",

        "Deal three damage to each creature and each player."
    ]
