from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Luminous_Guardian.model import Luminous_Guardian

@bind_card(Luminous_Guardian)
class Luminous_Guardian_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Flying, Lifelink. When [CARD_NAME] enters the battlefield, you may exile target creature with power 3 or greater an opponent controls until [CARD_NAME] leaves the battlefield.",

        "Flying, Lifelink. When [CARD_NAME] enters play, you may exile target creature with power 3 or greater an opponent controls until [CARD_NAME] leaves the battlefield.",

        "Flying, Lifelink. As [CARD_NAME] enters the battlefield, you may exile target creature with power 3 or greater an opponent controls until [CARD_NAME] leaves the battlefield.",

        "Flying, Lifelink. Upon entering the battlefield, [CARD_NAME] lets you exile target creature with power 3 or greater an opponent controls until [CARD_NAME] leaves the battlefield.",

        "Flying, Lifelink. When [CARD_NAME] arrives, you may exile target creature with power 3 or greater an opponent controls until [CARD_NAME] leaves the battlefield.",

        "Flying, Lifelink. When [CARD_NAME] enters the battlefield, you may exile a target creature with power 3 or greater an opponent controls until [CARD_NAME] leaves the battlefield.",

        "Flying, Lifelink. When [CARD_NAME] enters the battlefield, you may exile target creature an opponent controls with power 3 or greater until [CARD_NAME] leaves the battlefield.",

        "Flying, Lifelink. When [CARD_NAME] enters the battlefield, you may exile target creature with power 3+ an opponent controls until [CARD_NAME] leaves the battlefield.",

        "Flying, Lifelink. When [CARD_NAME] enters the battlefield, you may exile target opposing creature with power 3 or greater until [CARD_NAME] leaves the battlefield.",

    ]
