from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Awaken_the_Elemental.model import Awaken_the_Elemental

@bind_card(Awaken_the_Elemental)
class Awaken_the_Elemental_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Return a creature card from your graveyard to the battlefield, then put five +1/+1 counters on it until end of turn.",

        "[CARD_NAME] returns a creature card from your graveyard to the battlefield, then puts five +1/+1 counters on it until end of turn.",

        "Return one creature card from your graveyard to the battlefield. Put five +1/+1 counters on it until end of turn.",

        "[CARD_NAME] brings a creature card from your graveyard to the battlefield and gives it five +1/+1 counters until end of turn.",

        "Put a creature card from your graveyard onto the battlefield, then put five +1/+1 counters on it until end of turn.",

        "[CARD_NAME] returns a creature from your graveyard to the battlefield with five +1/+1 counters until end of turn.",

        "Return a creature card from your graveyard to play, then put five +1/+1 counters on it until end of turn.",

        "[CARD_NAME] puts a creature card from your graveyard onto the battlefield and adds five +1/+1 counters until end of turn.",

        "Return one creature card from your graveyard to the battlefield. It gets five +1/+1 counters until end of turn.",

        "[CARD_NAME] returns a creature card from your graveyard to the battlefield, then grants it five +1/+1 counters until end of turn."
    ]
