from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Paladin_s_Judging_Light.model import Paladin_s_Judging_Light

@bind_card(Paladin_s_Judging_Light)
class Paladin_s_Judging_Light_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Counter target spell. Its controller takes light damage equal to its mana cost.",
        "[CARD_NAME] counters target spell; its controller takes light damage equal to mana cost.",
        "Counter a spell. Controller takes light damage equal to its mana cost.",
        "With [CARD_NAME], counter target spell and deal light damage equal to mana cost to controller.",
        "Counter target spell. Spell controller takes light damage equal to mana cost.",
        "[CARD_NAME]: counter spell; light damage to controller equal to mana cost.",
        "Counter a spell. Its controller suffers light damage equal to the spell's mana cost.",
        "Counter target spell. Controller takes damage equal to mana cost (light damage).",
        "[CARD_NAME] counters and punishes controller with light damage equal to mana cost.",
        "Counter spell; controller takes light damage matching the spell's mana cost.",
    ]
