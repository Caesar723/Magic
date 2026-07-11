from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Mystic_Reversal.model import Mystic_Reversal

@bind_card(Mystic_Reversal)
class Mystic_Reversal_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Each player draws a card, then discards a card.",

        "[CARD_NAME] causes each player to draw a card, then discard a card.",

        "Every player draws a card, then discards a card.",

        "[CARD_NAME] makes each player draw a card and then discard a card.",

        "Each player draws one card, then discards one card.",

        "[CARD_NAME] lets each player draw a card, then discard a card.",

        "All players draw a card, then discard a card.",

        "[CARD_NAME] has each player draw a card, then discard a card.",

        "Each player draws a card. Then each player discards a card.",

        "[CARD_NAME] causes every player to draw a card, then discard a card."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.room.env_initinal_library(self.player.opponent, {"creature_number": (1, 3), "land_number": (1, 3)})
        self.room.env_initinal_hand(self.player.opponent, {"creature_number": (1, 2), "instant_number": (1, 2)})
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U": (1, 7)},
            least_mana={"colorless": 1, "U": 1},
        )

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
