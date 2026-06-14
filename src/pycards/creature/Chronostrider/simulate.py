from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Chronostrider.model import Chronostrider

@bind_card(Chronostrider)
class Chronostrider_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Flash, Haste. When [CARD_NAME] enters the battlefield, you may take an extra turn after this one.",

        "Haste, Flash. When [CARD_NAME] enters play, you may take an extra turn after this one.",

        "Flash, Haste. As [CARD_NAME] enters the battlefield, you may take an extra turn after this one.",

        "Haste, Flash. Upon entering the battlefield, [CARD_NAME] lets you take an extra turn after this one.",

        "Flash, Haste. When [CARD_NAME] arrives, you may take an extra turn after this one.",

        "Haste, Flash. When [CARD_NAME] enters the battlefield, you may gain an extra turn after this one.",

        "Flash, Haste. When [CARD_NAME] enters the battlefield, you may take another turn after this one ends.",

        "Haste, Flash. When [CARD_NAME] enters the battlefield, you may take an additional turn after this one.",

        "Flash, Haste. When [CARD_NAME] enters the battlefield, you may take an extra turn following this one.",

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
            least_mana={"colorless":3,"G":1}
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

