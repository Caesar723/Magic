from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Mystic_Confluence.model import Mystic_Confluence

@bind_card(Mystic_Confluence)
class Mystic_Confluence_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Counter target spell. Return target creature to its owner's hand. Draw a card.",
        "[CARD_NAME] counters a spell, bounces a creature, and draws a card.",
        "Counter target spell, bounce a creature to hand, draw a card.",
        "With [CARD_NAME], counter, bounce creature, and draw.",
        "Counter a spell. Return a creature to hand. Draw a card.",
        "[CARD_NAME]: counter + creature bounce + draw a card.",
        "Counter target spell, return target creature to hand, then draw.",
        "Three effects: counter spell, bounce creature, draw a card.",
        "[CARD_NAME] counters, bounces a creature, and lets you draw.",
        "Counter, bounce creature to hand, draw a card.",
    ]
