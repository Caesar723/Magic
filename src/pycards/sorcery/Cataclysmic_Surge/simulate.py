from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Cataclysmic_Surge.model import Cataclysmic_Surge

@bind_card(Cataclysmic_Surge)
class Cataclysmic_Surge_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] deals 5 damage to each creature and each player.",

        "Deal 5 damage to every creature and every player.",

        "[CARD_NAME] inflicts 5 damage on each creature and each player.",

        "Each creature and each player takes 5 damage.",

        "[CARD_NAME] deals five damage to all creatures and all players.",

        "Deal 5 damage to each creature on the battlefield and each player.",

        "[CARD_NAME] hits every creature and every player for 5 damage.",

        "All creatures and all players take 5 damage.",

        "[CARD_NAME] deals 5 damage to each creature and each player in the game.",

        "Deal five damage to each creature and each player."
    ]
