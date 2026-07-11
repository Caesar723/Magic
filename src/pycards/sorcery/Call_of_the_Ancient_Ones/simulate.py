from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Call_of_the_Ancient_Ones.model import Call_of_the_Ancient_Ones

@bind_card(Call_of_the_Ancient_Ones)
class Call_of_the_Ancient_Ones_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] allows you to return a random creature card from a graveyard to the battlefield under your control. That creature gains haste until end of turn and must be sacrificed at the beginning of the next end step.",

        "Return a random creature card from a graveyard to the battlefield under your control. It gains haste until end of turn and is sacrificed at the beginning of the next end step.",

        "[CARD_NAME] returns a random creature card from a graveyard to the battlefield under your control with haste until end of turn. Sacrifice it at the beginning of the next end step.",

        "Put a random creature card from a graveyard onto the battlefield under your control. It gains haste until end of turn and must be sacrificed at the next end step.",

        "[CARD_NAME] brings a random creature card from a graveyard to the battlefield under your control. That creature has haste until end of turn and is sacrificed at the beginning of the next end step.",

        "Return one random creature card from a graveyard to the battlefield under your control. It gains haste until end of turn. Sacrifice it at the beginning of the next end step.",

        "[CARD_NAME] returns a random creature from a graveyard to the battlefield under your control with haste until end of turn, then sacrifices it at the beginning of the next end step.",

        "A random creature card from a graveyard returns to the battlefield under your control. It gains haste until end of turn and must be sacrificed at the beginning of the next end step.",

        "[CARD_NAME] puts a random creature card from a graveyard onto the battlefield under your control. It gains haste until end of turn and is sacrificed at the beginning of the next end step.",

        "Return a random creature card from a graveyard to the battlefield under your control. That creature gains haste until end of turn. Sacrifice it at the beginning of the next end step."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.room.env_initinal_graveyard(self.player, {"creature_number": (2, 5)})
        self.room.env_initinal_graveyard(self.player.opponent, {"creature_number": (1, 3)})
        self.room.env_no_creature(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"B": (2, 7)},
            least_mana={"colorless": 2, "B": 2},
        )

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
