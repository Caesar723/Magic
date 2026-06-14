from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Thornwood_Ranger.model import Thornwood_Ranger

@bind_card(Thornwood_Ranger)
class Thornwood_Ranger_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Reach. When [CARD_NAME] enters the battlefield, another target creature you control gets +1/+0 until end of turn.",

        "Reach. When [CARD_NAME] enters play, another target creature you control gets +1/+0 until end of turn.",

        "Reach. As [CARD_NAME] enters the battlefield, another target creature you control gets +1/+0 until end of turn.",

        "Reach. Upon entering the battlefield, [CARD_NAME] gives another target creature you control +1/+0 until end of turn.",

        "Reach. When [CARD_NAME] arrives, another target creature you control gets +1/+0 until end of turn.",

        "Reach. When [CARD_NAME] enters the battlefield, target another creature you control gets +1/+0 until end of turn.",

        "Reach. When [CARD_NAME] enters the battlefield, another creature you control gets +1/+0 until end of turn.",

        "Reach. When [CARD_NAME] enters the battlefield, another target creature you control gains +1/+0 until end of turn.",

        "Reach. When [CARD_NAME] enters the battlefield, another target creature you control receives +1/+0 until end of turn.",

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
            {"G":(1,7)},
            least_mana={"colorless":1,"G":1}
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

