from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Time_Rift_Convergence.model import Time_Rift_Convergence

@bind_card(Time_Rift_Convergence)
class Time_Rift_Convergence_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Return up to two target cards from your graveyard to your hand.",

        "[CARD_NAME] lets you return up to two target cards from your graveyard to your hand.",

        "Return up to two cards from your graveyard to your hand.",

        "[CARD_NAME] returns up to two target cards from your graveyard to your hand.",

        "Choose up to two target cards in your graveyard. Return them to your hand.",

        "[CARD_NAME] allows you to return up to two cards from your graveyard to your hand.",

        "Return up to two cards from your graveyard to hand.",

        "[CARD_NAME] brings up to two target cards from your graveyard back to your hand.",

        "Put up to two target cards from your graveyard into your hand.",

        "[CARD_NAME] returns up to two target cards from your graveyard to your hand."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.room.env_initinal_graveyard(self.player, {"creature_number": (2, 4), "instant_number": (2, 4), "sorcery_number": (2, 4)})
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
