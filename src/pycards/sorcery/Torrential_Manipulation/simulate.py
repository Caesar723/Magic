from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Torrential_Manipulation.model import Torrential_Manipulation

@bind_card(Torrential_Manipulation)
class Torrential_Manipulation_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Return target creature to its owner's hand. You randomly cast an instant or sorcery spell without paying its mana cost.",

        "[CARD_NAME] returns target creature to its owner's hand, then you randomly cast an instant or sorcery spell without paying its mana cost.",

        "Bounce target creature to its owner's hand. Then randomly cast an instant or sorcery spell without paying its mana cost.",

        "[CARD_NAME] sends target creature back to its owner's hand and lets you randomly cast an instant or sorcery spell for free.",

        "Return target creature to its owner's hand. Then you cast a random instant or sorcery spell without paying its mana cost.",

        "[CARD_NAME] bounces target creature to its owner's hand, then you randomly cast an instant or sorcery spell without paying mana.",

        "Target creature returns to its owner's hand. You randomly cast an instant or sorcery spell without paying its mana cost.",

        "[CARD_NAME] returns target creature to hand and randomly casts an instant or sorcery spell without paying its mana cost.",

        "Return a target creature to its owner's hand, then randomly cast an instant or sorcery spell without paying its mana cost.",

        "[CARD_NAME] puts target creature into its owner's hand, then you randomly cast an instant or sorcery spell without paying its mana cost."
    ]
