from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Radiant_Angel.model import Radiant_Angel

@bind_card(Radiant_Angel)
class Radiant_Angel_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Flying, Lifelink. Whenever [CARD_NAME] deals damage, it illuminates all creatures with dark attributes, making them unable to attack or block this turn.",

        "Flying, Lifelink. Whenever [CARD_NAME] deals damage, all dark-attribute creatures can't attack or block this turn.",

        "Flying, Lifelink. When [CARD_NAME] deals damage, creatures with dark attributes can't attack or block this turn.",

        "Flying, Lifelink. Each time [CARD_NAME] deals damage, dark-attribute creatures are unable to attack or block this turn.",

        "Flying, Lifelink. Whenever [CARD_NAME] deals damage, it blinds dark creatures, preventing them from attacking or blocking this turn.",

        "Flying, Lifelink. Whenever [CARD_NAME] deals damage, all creatures with dark attributes cannot attack or block this turn.",

        "Flying, Lifelink. On dealing damage, [CARD_NAME] renders dark-attribute creatures unable to attack or block this turn.",

        "Flying, Lifelink. Whenever [CARD_NAME] deals damage, dark creatures can't attack or block for the rest of the turn.",

        "Flying, Lifelink. Whenever [CARD_NAME] deals damage, it illuminates dark creatures, preventing them from attacking or blocking this turn.",

    ]
