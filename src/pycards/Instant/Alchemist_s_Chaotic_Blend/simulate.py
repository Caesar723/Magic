from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Alchemist_s_Chaotic_Blend.model import Alchemist_s_Chaotic_Blend

@bind_card(Alchemist_s_Chaotic_Blend)
class Alchemist_s_Chaotic_Blend_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Counter target spell. Then reveal a random card from your library and cast it without paying its mana cost.",
        "[CARD_NAME] counters target spell, then reveals a random card from your library and lets you cast it for free.",
        "Counter a spell on the stack. Afterward, reveal a random library card and cast it without paying mana.",
        "With [CARD_NAME], counter target spell, then flip over a random card from your library and cast it at no cost.",
        "Counter target spell. Then show a random card from your library and cast it without paying its mana cost.",
        "[CARD_NAME] lets you counter target spell, then reveal and freely cast a random card from your library.",
        "Counter target spell. Next, reveal a random card from among your library and cast it without paying mana.",
        "Use [CARD_NAME] to counter a spell, then reveal a random library card and cast it without its mana cost.",
        "Counter target spell. Then you reveal a random card from your library and may cast it without paying mana.",
        "Counter target spell, then reveal a random card from your deck and cast it without paying its mana cost.",
    ]
