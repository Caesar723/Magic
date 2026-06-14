from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Vengeful_Retribution.model import Vengeful_Retribution

@bind_card(Vengeful_Retribution)
class Vengeful_Retribution_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Opponent sacrifices two random creatures. If a creature was sacrificed this way, [CARD_NAME] deals damage to random target equal to the total power of the sacrificed creatures.",
        "[CARD_NAME] makes opponent sacrifice two random creatures; deals damage equal to total power to random target if any sacrificed.",
        "Opponent sacrifices two random creatures. Damage random target for total sacrificed power if any died.",
        "Force opponent to sacrifice two random creatures. Damage equal to total power to random target.",
        "[CARD_NAME]: opponent sacrifices two random creatures; damage based on total power.",
        "Opponent sacrifices two creatures at random. [CARD_NAME] damages random target for their total power.",
        "Two random opponent creatures sacrificed. Damage random target equal to combined power.",
        "With [CARD_NAME], opponent sacrifices two random creatures; retribution damage equals total power.",
        "Opponent sacrifices two random creatures. If so, damage random target for total power.",
        "[CARD_NAME] forces sacrifices and deals damage equal to total sacrificed power.",
    ]
