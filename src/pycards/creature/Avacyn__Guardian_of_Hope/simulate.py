from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Avacyn__Guardian_of_Hope.model import Avacyn__Guardian_of_Hope

@bind_card(Avacyn__Guardian_of_Hope)
class Avacyn__Guardian_of_Hope_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Flying, Vigilance, Lifelink. When [CARD_NAME] enters the battlefield, creatures you control gain indestructible until end of turn.",

        "Flying, Vigilance, Lifelink. When [CARD_NAME] enters play, your creatures become indestructible until end of turn.",

        "Flying, Vigilance, Lifelink. As [CARD_NAME] enters the battlefield, all creatures you control gain indestructible until end of turn.",

        "Flying, Vigilance, Lifelink. Upon entering the battlefield, [CARD_NAME] grants indestructible to creatures you control until end of turn.",

        "Flying, Vigilance, Lifelink. When [CARD_NAME] arrives, each creature you control gains indestructible until end of turn.",

        "Flying, Vigilance, Lifelink. When [CARD_NAME] enters the battlefield, your creatures can't be destroyed until end of turn.",

        "Flying, Vigilance, Lifelink. When [CARD_NAME] enters the battlefield, creatures under your control gain indestructible for the rest of the turn.",

        "Flying, Vigilance, Lifelink. When [CARD_NAME] enters the battlefield, all your creatures become indestructible until the turn ends.",

        "Flying, Vigilance, Lifelink. When [CARD_NAME] enters the battlefield, creatures you control are indestructible until end of turn.",

    ]
