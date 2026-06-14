from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Witch_s_Curse_Counter.model import Witch_s_Curse_Counter

@bind_card(Witch_s_Curse_Counter)
class Witch_s_Curse_Counter_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Counter target spell. Then, its controller's creatures gains a curse for three turns, reducing their strength and stamina by half.",
        "[CARD_NAME] counters target spell and curses controller's creatures for three turns, halving strength and stamina.",
        "Counter a spell. Controller's creatures get a three-turn curse halving strength and stamina.",
        "With [CARD_NAME], counter target spell and apply a halving curse to controller's creatures.",
        "Counter target spell. Controller's creatures cursed for three turns (half strength/stamina).",
        "[CARD_NAME]: counter spell; three-turn halving curse on controller's creatures.",
        "Counter a spell. Then curse controller's creatures, halving stats for three turns.",
        "Counter target spell. Curse reduces controller's creatures' strength and stamina by half for three turns.",
        "[CARD_NAME] counters and curses opponent creatures with halved stats for three turns.",
        "Counter spell; controller's creatures suffer halved strength and stamina for three turns.",
    ]
