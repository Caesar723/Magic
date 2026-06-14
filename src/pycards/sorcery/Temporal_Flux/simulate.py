from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Temporal_Flux.model import Temporal_Flux

@bind_card(Temporal_Flux)
class Temporal_Flux_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Tap all creatures your opponents control. They don't untap during their next untap step.",

        "[CARD_NAME] taps all creatures your opponents control. They don't untap during their next untap step.",

        "Tap every creature controlled by your opponents. They don't untap during their next untap step.",

        "[CARD_NAME] causes all creatures your opponents control to become tapped. They don't untap during their next untap step.",

        "All creatures your opponents control are tapped. They don't untap during their next untap step.",

        "[CARD_NAME] taps all opponent-controlled creatures. They don't untap during their next untap step.",

        "Tap all creatures your opponents control. Those creatures don't untap during their controllers' next untap step.",

        "[CARD_NAME] taps every creature your opponents control. They don't untap during their next untap step.",

        "All creatures controlled by your opponents are tapped and don't untap during their next untap step.",

        "[CARD_NAME] taps all creatures your opponents control and prevents them from untapping during their next untap step."
    ]
