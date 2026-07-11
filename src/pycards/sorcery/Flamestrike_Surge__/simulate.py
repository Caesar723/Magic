from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Flamestrike_Surge__.model import Flamestrike_Surge__

@bind_card(Flamestrike_Surge__)
class Flamestrike_Surge___Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] deals 3 damage to any target and randomly discards a card and draws a card.",

        "Deal 3 damage to any target. Then randomly discard a card and draw a card.",

        "[CARD_NAME] deals 3 damage to any target, then you randomly discard a card and draw a card.",

        "Deal 3 damage to any target, then randomly discard a card and draw a card.",

        "[CARD_NAME] hits any target for 3 damage, then you randomly discard a card and draw a card.",

        "Deal three damage to any target. Then randomly discard a card and draw a card.",

        "[CARD_NAME] deals 3 damage to a target of your choice, then randomly discards a card and draws a card.",

        "Any target takes 3 damage. Then randomly discard a card and draw a card.",

        "[CARD_NAME] inflicts 3 damage on any target, then you randomly discard a card and draw a card.",

        "Deal 3 damage to any target. Randomly discard a card, then draw a card."
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
            {"R": (2, 7)},
            least_mana={"colorless": 1, "R": 2},
        )

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
