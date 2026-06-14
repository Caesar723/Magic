from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Merfolk_Wayfinder.model import Merfolk_Wayfinder

@bind_card(Merfolk_Wayfinder)
class Merfolk_Wayfinder_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "When [CARD_NAME] enters the battlefield, you may scry 1.",

        "When [CARD_NAME] enters play, you may scry 1.",

        "As [CARD_NAME] enters the battlefield, you may scry 1.",

        "Upon entering the battlefield, [CARD_NAME] lets you scry 1.",

        "When [CARD_NAME] arrives, you may scry 1.",

        "When [CARD_NAME] enters the battlefield, you may scry one.",

        "When [CARD_NAME] enters the battlefield, you may look at the top card of your library and put it on the bottom.",

        "When [CARD_NAME] enters the battlefield, you may scry 1. (Look at the top card of your library. You may put it on the bottom.)",

        "When [CARD_NAME] enters the battlefield, you may scry 1 (look at the top of your library, optionally put it on the bottom).",

    ]
    @simulate
    def simulate_when_enter_battlefield(self):
        self.basic_initinal()
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

    @simulate
    def simulate_when_attack_opponent(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U":(0,7),"B":(0,7),"G":(0,7),"R":(0,7),"W":(0,7)},
        )

        simulate_info=self.room.simulate_creature_attack(self.card)
        return simulate_info

    @simulate
    def simulate_when_defend_opponent(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.room.env_creature(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U":(0,7),"B":(0,7),"G":(0,7),"R":(0,7),"W":(0,7)},
        )

        simulate_info=self.room.simulate_creature_defend(self.card)
        return simulate_info

