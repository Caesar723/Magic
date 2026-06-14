from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Emberheart_Berserker__.model import Emberheart_Berserker__

@bind_card(Emberheart_Berserker__)
class Emberheart_Berserker___Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Whenever [CARD_NAME] defends, it gets +0/+1 until end of turn for each Mountain you control.",

        "Each time [CARD_NAME] blocks, it gets +0/+1 until end of turn for every Mountain you control.",

        "When [CARD_NAME] defends, it gains +0/+1 until end of turn for each Mountain you control.",

        "Whenever [CARD_NAME] blocks, it gets +0/+1 until end of turn per Mountain you control.",

        "On defense, [CARD_NAME] gets +0/+1 until end of turn for each Mountain you control.",

        "Whenever [CARD_NAME] defends, add +0/+1 until end of turn for each Mountain you control.",

        "When [CARD_NAME] defends, its toughness increases by 1 until end of turn for each Mountain you control.",

        "Whenever [CARD_NAME] defends, it grows by +0/+1 until end of turn for each Mountain you control.",

        "Each block by [CARD_NAME] grants it +0/+1 until end of turn for every Mountain you control.",

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
            {"R":(2,7)},
            least_mana={"colorless":1,"R":2}
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

