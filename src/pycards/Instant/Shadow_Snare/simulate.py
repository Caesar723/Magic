from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Shadow_Snare.model import Shadow_Snare

@bind_card(Shadow_Snare)
class Shadow_Snare_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Target creature gets -3/-3 until end of turn.",
        "[CARD_NAME] gives target creature -3/-3 until end of turn.",
        "Choose a creature. It gets -3/-3 this turn.",
        "-3/-3 until end of turn on target creature.",
        "[CARD_NAME]: -3/-3 debuff until end of turn.",
        "Weaken target creature by -3/-3 until end of turn.",
        "Target creature suffers -3/-3 this turn.",
        "With [CARD_NAME], apply -3/-3 to a creature until end of turn.",
        "Give -3/-3 to target creature until end of turn.",
        "[CARD_NAME] snares a creature with -3/-3 until end of turn.",
    ]
