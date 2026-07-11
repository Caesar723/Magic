from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Time_Warp.model import Time_Warp

@bind_card(Time_Warp)
class Time_Warp_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Draw two cards, then randomly discard a card. You may put a card from your graveyard on top of your library.",

        "[CARD_NAME] lets you draw two cards, randomly discard a card, and optionally put a card from your graveyard on top of your library.",

        "Draw two cards, then discard a card at random. You may put a card from your graveyard on top of your library.",

        "[CARD_NAME] draws you two cards, then you randomly discard a card. You may put a card from your graveyard on top of your library.",

        "Draw two cards. Then randomly discard one card. You may put a card from your graveyard on top of your library.",

        "[CARD_NAME] causes you to draw two cards, randomly discard a card, and optionally place a card from your graveyard on top of your library.",

        "Draw a pair of cards, then randomly discard one. You may put a card from your graveyard on top of your library.",

        "[CARD_NAME] draws two cards, then you discard a random card. You may put a card from your graveyard on top of your library.",

        "Draw two cards, randomly discard a card from your hand, then you may put a card from your graveyard on top of your library.",

        "[CARD_NAME] allows you to draw two cards, randomly discard a card, and put a card from your graveyard on top of your library if you choose."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.room.env_initinal_graveyard(self.player, {"creature_number": (1, 3), "instant_number": (1, 3), "sorcery_number": (1, 3)})
        self.room.env_initinal_hand(self.player, {"creature_number": (1, 2), "instant_number": (1, 2)})
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U": (2, 7)},
            least_mana={"colorless": 3, "U": 2},
        )

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
