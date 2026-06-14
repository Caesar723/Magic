from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Mistweaver_Adept.model import Mistweaver_Adept

@bind_card(Mistweaver_Adept)
class Mistweaver_Adept_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "When [CARD_NAME] enters the battlefield, you may return target creature to its owner's hand. If you do, scry 2.",

        "When [CARD_NAME] enters play, you may return target creature to its owner's hand. If you do, scry 2.",

        "As [CARD_NAME] enters the battlefield, you may return target creature to its owner's hand. If you do, scry 2.",

        "Upon entering the battlefield, [CARD_NAME] lets you return target creature to its owner's hand. If you do, scry 2.",

        "When [CARD_NAME] arrives, you may return target creature to its owner's hand. If you do, scry 2.",

        "When [CARD_NAME] enters the battlefield, you may bounce target creature. If you do, scry 2.",

        "When [CARD_NAME] enters the battlefield, you may return target creature to hand. If you do, scry 2.",

        "When [CARD_NAME] enters the battlefield, you may return target creature to its owner's hand, then scry 2 if you do.",

        "When [CARD_NAME] enters the battlefield, you may return target creature to its owner's hand. If you do, scry two.",

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
            least_mana={"colorless":1,"U":1}
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

