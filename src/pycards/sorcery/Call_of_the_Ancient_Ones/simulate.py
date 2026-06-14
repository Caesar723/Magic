from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Call_of_the_Ancient_Ones.model import Call_of_the_Ancient_Ones

@bind_card(Call_of_the_Ancient_Ones)
class Call_of_the_Ancient_Ones_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] allows you to return a random creature card from a graveyard to the battlefield under your control. That creature gains haste until end of turn and must be sacrificed at the beginning of the next end step.",

        "Return a random creature card from a graveyard to the battlefield under your control. It gains haste until end of turn and is sacrificed at the beginning of the next end step.",

        "[CARD_NAME] returns a random creature card from a graveyard to the battlefield under your control with haste until end of turn. Sacrifice it at the beginning of the next end step.",

        "Put a random creature card from a graveyard onto the battlefield under your control. It gains haste until end of turn and must be sacrificed at the next end step.",

        "[CARD_NAME] brings a random creature card from a graveyard to the battlefield under your control. That creature has haste until end of turn and is sacrificed at the beginning of the next end step.",

        "Return one random creature card from a graveyard to the battlefield under your control. It gains haste until end of turn. Sacrifice it at the beginning of the next end step.",

        "[CARD_NAME] returns a random creature from a graveyard to the battlefield under your control with haste until end of turn, then sacrifices it at the beginning of the next end step.",

        "A random creature card from a graveyard returns to the battlefield under your control. It gains haste until end of turn and must be sacrificed at the beginning of the next end step.",

        "[CARD_NAME] puts a random creature card from a graveyard onto the battlefield under your control. It gains haste until end of turn and is sacrificed at the beginning of the next end step.",

        "Return a random creature card from a graveyard to the battlefield under your control. That creature gains haste until end of turn. Sacrifice it at the beginning of the next end step."
    ]
