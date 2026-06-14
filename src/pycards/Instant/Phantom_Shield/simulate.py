from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Phantom_Shield.model import Phantom_Shield

@bind_card(Phantom_Shield)
class Phantom_Shield_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Until end of turn, your creatures gain 'Prevent all damage that would be dealt to this creature this turn.'",
        "[CARD_NAME] gives all your creatures damage prevention until end of turn.",
        "Your creatures can't be dealt damage this turn.",
        "All creatures you control prevent damage dealt to them this turn.",
        "[CARD_NAME]: your creatures prevent all damage this turn.",
        "Grant damage prevention to all your creatures until end of turn.",
        "Your creatures ignore damage this turn with [CARD_NAME].",
        "Until end of turn, damage is prevented to all creatures you control.",
        "All your creatures gain damage prevention this turn.",
        "[CARD_NAME] shields all your creatures from damage until end of turn.",
    ]
