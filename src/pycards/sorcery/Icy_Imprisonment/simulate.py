from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Icy_Imprisonment.model import Icy_Imprisonment

@bind_card(Icy_Imprisonment)
class Icy_Imprisonment_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Freeze all creatures your opponents control until the start of your next turn.",

        "[CARD_NAME] freezes all creatures your opponents control until the start of your next turn.",

        "All creatures your opponents control are frozen until the start of your next turn.",

        "[CARD_NAME] causes all creatures your opponents control to be frozen until the start of your next turn.",

        "Freeze every creature controlled by your opponents until the start of your next turn.",

        "[CARD_NAME] freezes all opponent-controlled creatures until the start of your next turn.",

        "All creatures your opponents control cannot act until the start of your next turn.",

        "[CARD_NAME] freezes all creatures controlled by your opponents until the start of your next turn.",

        "Freeze each creature your opponents control until the start of your next turn.",

        "[CARD_NAME] keeps all creatures your opponents control frozen until the start of your next turn."
    ]
