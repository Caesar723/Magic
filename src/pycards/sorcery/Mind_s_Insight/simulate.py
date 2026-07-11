from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Mind_s_Insight.model import Mind_s_Insight

@bind_card(Mind_s_Insight)
class Mind_s_Insight_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Draw three cards, then randomly discard one card unless you discard an Island.",

        "[CARD_NAME] lets you draw three cards, then randomly discard one card unless you discard an Island.",

        "Draw three cards. Then randomly discard one card unless you discard an Island.",

        "[CARD_NAME] draws you three cards, then you randomly discard one card unless you discard an Island.",

        "Draw three cards, then discard a random card unless you choose to discard an Island instead.",

        "[CARD_NAME] causes you to draw three cards, then randomly discard one card unless you discard an Island.",

        "Draw three cards. Then randomly discard one card. You may discard an Island to avoid the random discard.",

        "[CARD_NAME] draws three cards, then you randomly discard one card unless you discard an Island.",

        "Draw three cards, then randomly discard a card from your hand unless you discard an Island.",

        "[CARD_NAME] allows you to draw three cards, then randomly discard one card unless you discard an Island."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.room.env_initinal_hand(self.player, {"land_number": (2, 3), "instant_number": (1, 2)})
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U": (1, 7)},
            least_mana={"colorless": 4, "U": 1},
        )

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
