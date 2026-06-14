from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Flamespark.model import Flamespark

@bind_card(Flamespark)
class Flamespark_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] deals 3 damage to any target. If you control a Mountain, it deals 5 damage instead.",
        "Deal 3 damage to any target. If you control a Mountain, deal 5 instead.",
        "[CARD_NAME] hits for 3, or 5 if you control a Mountain.",
        "Choose any target. Deal 3, or 5 with a Mountain.",
        "Fire 3 damage at any target; 5 if you control a Mountain.",
        "[CARD_NAME]: 3 damage, boosted to 5 when you control a Mountain.",
        "Any target takes 3 damage, or 5 if you have a Mountain.",
        "Deal 3 to any target. Mountain control upgrades [CARD_NAME] to 5 damage.",
        "[CARD_NAME] deals 3 or 5 damage depending on whether you control a Mountain.",
        "Three damage to any target, five if you control a Mountain.",
    ]
