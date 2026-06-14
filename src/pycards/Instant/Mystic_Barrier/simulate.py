from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Mystic_Barrier.model import Mystic_Barrier

@bind_card(Mystic_Barrier)
class Mystic_Barrier_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Target player can't cast noncreature spells until end of turn.",
        "[CARD_NAME] prevents target player from casting noncreature spells until end of turn.",
        "Choose a player. They can't cast noncreature spells this turn.",
        "Target player is locked out of noncreature spells until end of turn.",
        "[CARD_NAME]: target player can't cast noncreature spells this turn.",
        "Until end of turn, target player can't cast noncreature spells.",
        "Silence noncreature spells for target player until end of turn.",
        "With [CARD_NAME], stop a player from casting noncreature spells this turn.",
        "Target player cannot cast instants, sorceries, etc. until end of turn.",
        "[CARD_NAME] bars target player from noncreature spells until end of turn.",
    ]
