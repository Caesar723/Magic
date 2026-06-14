from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Celestial_Seraph.model import Celestial_Seraph

@bind_card(Celestial_Seraph)
class Celestial_Seraph_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Flying, Lifelink. Whenever [CARD_NAME] attacks, you may exile a random nonland permanent an opponent controls until [CARD_NAME] leaves the battlefield.",

        "Lifelink, Flying. When [CARD_NAME] attacks, you may exile a random nonland permanent an opponent controls until [CARD_NAME] leaves play.",

        "Flying, Lifelink. Each time [CARD_NAME] attacks, you may exile a random nonland permanent an opponent controls until [CARD_NAME] departs the battlefield.",

        "Lifelink, Flying. Whenever [CARD_NAME] attacks, you may exile a random nonland permanent controlled by an opponent until [CARD_NAME] leaves the battlefield.",

        "Flying, Lifelink. On attack, [CARD_NAME] may exile a random nonland permanent an opponent controls until it leaves the battlefield.",

        "Lifelink, Flying. Whenever [CARD_NAME] attacks, you may exile a random nonland opposing permanent until [CARD_NAME] leaves the battlefield.",

        "Flying, Lifelink. When [CARD_NAME] attacks, you may exile a random nonland permanent an opponent controls for as long as [CARD_NAME] remains on the battlefield.",

        "Lifelink, Flying. Whenever [CARD_NAME] attacks, you may exile a random nonland permanent an opponent controls until [CARD_NAME] is gone.",

        "Flying, Lifelink. Whenever [CARD_NAME] attacks, you may exile a random nonland permanent an opponent controls until [CARD_NAME] leaves the battlefield.",

    ]
