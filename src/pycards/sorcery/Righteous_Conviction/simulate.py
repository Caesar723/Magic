from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Righteous_Conviction.model import Righteous_Conviction

@bind_card(Righteous_Conviction)
class Righteous_Conviction_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Choose a creature you control. Until end of turn, that creature gets +2/+2 and gains lifelink.",

        "[CARD_NAME] lets you choose a creature you control. Until end of turn, it gets +2/+2 and gains lifelink.",

        "Choose a creature you control. It gets +2/+2 and gains lifelink until end of turn.",

        "[CARD_NAME] causes a creature you control to get +2/+2 and gain lifelink until end of turn.",

        "Select a creature you control. Until end of turn, that creature gets +2/+2 and has lifelink.",

        "[CARD_NAME] grants a creature you control +2/+2 and lifelink until end of turn.",

        "Pick a creature you control. Until end of turn, it gets +2/+2 and gains lifelink.",

        "[CARD_NAME] buffs a creature you control with +2/+2 and lifelink until end of turn.",

        "Choose one of your creatures. Until end of turn, it gets +2/+2 and gains lifelink.",

        "[CARD_NAME] gives a creature you control +2/+2 and lifelink until end of turn."
    ]
