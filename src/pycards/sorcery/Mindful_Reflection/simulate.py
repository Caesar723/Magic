from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Mindful_Reflection.model import Mindful_Reflection

@bind_card(Mindful_Reflection)
class Mindful_Reflection_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Draw two cards, then discard a card.",

        "[CARD_NAME] lets you draw two cards, then discard a card.",

        "Draw two cards. Then discard a card.",

        "[CARD_NAME] draws you two cards, then you discard a card.",

        "Draw two cards, then discard one card from your hand.",

        "[CARD_NAME] causes you to draw two cards, then discard a card.",

        "You draw two cards, then discard a card.",

        "[CARD_NAME] allows you to draw two cards and then discard a card.",

        "Draw a pair of cards, then discard one card.",

        "[CARD_NAME] draws two cards, then you discard a card."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.room.env_initinal_hand(self.player, {"creature_number": (1, 2), "sorcery_number": (1, 2)})
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
