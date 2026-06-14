from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Arcane_Insight.model import Arcane_Insight

@bind_card(Arcane_Insight)
class Arcane_Insight_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Draw two cards, then randomly discard a card unless you discard an instant or sorcery card.",
        "[CARD_NAME] lets you draw two cards, then discard a random card unless you choose an instant or sorcery.",
        "Draw two cards. Then discard a card at random unless you discard an instant or sorcery instead.",
        "With [CARD_NAME], draw two cards, then randomly discard unless you discard an instant or sorcery card.",
        "Draw two cards, then discard a random card from your hand unless you discard an instant or sorcery.",
        "[CARD_NAME]: draw two, then random discard unless you discard an instant or sorcery card.",
        "Draw two cards. Unless you discard an instant or sorcery card, discard a card at random.",
        "Use [CARD_NAME] to draw two cards, then discard randomly unless you discard an instant or sorcery.",
        "Draw two cards, then you must randomly discard a card unless you discard an instant or sorcery instead.",
        "Draw two cards, then discard a card at random unless you discard an instant or sorcery card from your hand.",
    ]
