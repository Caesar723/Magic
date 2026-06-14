from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Emberheart_Salamander.model import Emberheart_Salamander

@bind_card(Emberheart_Salamander)
class Emberheart_Salamander_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Trample. When [CARD_NAME] enters the battlefield, it deals 2 damage to any target.",

        "Trample. When [CARD_NAME] enters play, it deals 2 damage to any target.",

        "Trample. As [CARD_NAME] enters the battlefield, it deals 2 damage to any target.",

        "Trample. Upon entering the battlefield, [CARD_NAME] deals 2 damage to any target.",

        "Trample. When [CARD_NAME] arrives, it deals 2 damage to any target.",

        "Trample. When [CARD_NAME] enters the battlefield, deal 2 damage to any target.",

        "Trample. When [CARD_NAME] enters the battlefield, it deals two damage to any target.",

        "Trample. When [CARD_NAME] enters the battlefield, it inflicts 2 damage on any target.",

        "Trample. When [CARD_NAME] enters the battlefield, it deals 2 damage to a target of your choice.",

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
            least_mana={"colorless":2,"R":2}
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

