from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Falling_Stars.model import Falling_Stars

@bind_card(Falling_Stars)
class Falling_Stars_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Deal 7 damage to all creatures, then summon a 7/7 Star Beast creature token onto the battlefield.",

        "[CARD_NAME] deals 7 damage to each creature, then creates a 7/7 Star Beast creature token.",

        "All creatures take 7 damage. Then put a 7/7 Star Beast creature token onto the battlefield.",

        "[CARD_NAME] inflicts 7 damage on every creature, then summons a 7/7 Star Beast token.",

        "Deal seven damage to all creatures. Afterward, create a 7/7 Star Beast creature token.",

        "[CARD_NAME] deals 7 damage to all creatures on the battlefield, then places a 7/7 Star Beast creature token into play.",

        "Each creature takes 7 damage. Then you create a 7/7 Star Beast creature token.",

        "[CARD_NAME] hits all creatures for 7 damage, then puts a 7/7 Star Beast creature token onto the battlefield.",

        "Deal 7 damage to every creature, then generate a 7/7 Star Beast creature token.",

        "[CARD_NAME] deals 7 damage to all creatures and then summons a 7/7 Star Beast creature token onto the battlefield."
    ]
