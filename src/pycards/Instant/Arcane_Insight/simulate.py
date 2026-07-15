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

    @simulate
    def simulate_card(self):
        self.basic_initinal()
        self.room.env_initinal_hand(
            self.player,
            {"instant_number":(1,2),"sorcery_number":(1,2)},
        )
        # Keep every post-draw choice an Instant so the implemented discard branch
        # is deterministic instead of depending on the seeded basic lands.
        self.player.hand=[type(self.card)(self.player) for _ in range(4)]
        self.player.library=[type(self.card)(self.player) for _ in range(5)]
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U":(1,7)},
            least_mana={"colorless":2,"U":1}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
