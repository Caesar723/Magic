from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Thundering_Behemoth.model import Thundering_Behemoth

@bind_card(Thundering_Behemoth)
class Thundering_Behemoth_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Trample. When [CARD_NAME] enters the battlefield, creatures you control gain trample until end of turn.",

        "Trample. When [CARD_NAME] enters play, creatures you control gain trample until end of turn.",

        "Trample. As [CARD_NAME] enters the battlefield, creatures you control gain trample until end of turn.",

        "Trample. Upon entering the battlefield, [CARD_NAME] grants trample to creatures you control until end of turn.",

        "Trample. When [CARD_NAME] arrives, creatures you control gain trample until end of turn.",

        "Trample. When [CARD_NAME] enters the battlefield, your creatures gain trample until end of turn.",

        "Trample. When [CARD_NAME] enters the battlefield, all creatures you control gain trample until end of turn.",

        "Trample. When [CARD_NAME] enters the battlefield, creatures under your control gain trample until end of turn.",

        "Trample. When [CARD_NAME] enters the battlefield, creatures you control have trample until end of turn.",

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
            {"G":(3,7)},
            least_mana={"colorless":4,"G":3}
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

