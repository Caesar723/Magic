from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Celestial_Intervention.model import Celestial_Intervention

@bind_card(Celestial_Intervention)
class Celestial_Intervention_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Until end of turn, creatures you control gain indestructible. You draw a card.",
        "[CARD_NAME] gives your creatures indestructible until end of turn and lets you draw a card.",
        "Your creatures gain indestructible until end of turn. Draw a card.",
        "Creatures you control can't be destroyed until end of turn. Draw a card.",
        "[CARD_NAME]: indestructible for your creatures this turn, plus draw a card.",
        "Grant indestructible to creatures you control until end of turn. Draw a card.",
        "Until end of turn, your creatures have indestructible. Draw a card.",
        "With [CARD_NAME], your creatures gain indestructible this turn and you draw a card.",
        "All creatures you control gain indestructible until end of turn. You draw a card.",
        "Indestructible on your creatures until end of turn. Draw a card.",
    ]
