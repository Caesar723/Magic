from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Shadowform_Surge.model import Shadowform_Surge

@bind_card(Shadowform_Surge)
class Shadowform_Surge_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Target creature gets -3/-3 until end of turn. If that creature dies this turn, create a 2/2 black Shade creature token with lifelink.",
        "[CARD_NAME] gives -3/-3; if the creature dies this turn, create a 2/2 Shade token with lifelink.",
        "-3/-3 until end of turn. Death this turn creates 2/2 black Shade with lifelink.",
        "Debuff -3/-3. If creature dies this turn, spawn 2/2 Shade lifelink token.",
        "[CARD_NAME]: -3/-3; Shade token on death this turn.",
        "Target creature gets -3/-3. Dies this turn? Create 2/2 black Shade with lifelink.",
        "Weaken -3/-3. Creature death this turn makes a 2/2 Shade token.",
        "With [CARD_NAME], -3/-3 debuff and Shade token if the creature dies this turn.",
        "-3/-3 until end of turn. Death creates 2/2 black Shade with lifelink.",
        "[CARD_NAME] debuffs -3/-3 and summons Shade token on death this turn.",
    ]
