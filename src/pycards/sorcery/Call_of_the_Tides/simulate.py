from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Call_of_the_Tides.model import Call_of_the_Tides

@bind_card(Call_of_the_Tides)
class Call_of_the_Tides_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Draw two cards, then discard a card randomly. Scry 2.",

        "[CARD_NAME] lets you draw two cards, randomly discard a card, then scry 2.",

        "Draw two cards. Then randomly discard a card. Scry 2.",

        "[CARD_NAME] draws you two cards, then you randomly discard a card and scry 2.",

        "Draw two cards, then discard a random card from your hand. Scry 2.",

        "[CARD_NAME] causes you to draw two cards, randomly discard a card, then scry 2.",

        "Draw a pair of cards, randomly discard one, then scry 2.",

        "[CARD_NAME] draws two cards, randomly discards a card, then you scry 2.",

        "Draw two cards, randomly discard a card, then scry 2.",

        "[CARD_NAME] allows you to draw two cards, randomly discard a card, and scry 2."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.room.env_initinal_hand(self.player, {"creature_number": (1, 2), "instant_number": (1, 2)})
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U": (2, 7)},
            least_mana={"colorless": 2, "U": 2},
        )

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
