from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Mystic_Tidecaller.model import Mystic_Tidecaller

@bind_card(Mystic_Tidecaller)
class Mystic_Tidecaller_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Flash. When [CARD_NAME] enters the battlefield, you may return target nonland permanent to its owner's hand.",

        "Flash. When [CARD_NAME] enters play, you may return target nonland permanent to its owner's hand.",

        "Flash. As [CARD_NAME] enters the battlefield, you may return target nonland permanent to its owner's hand.",

        "Flash. Upon entering the battlefield, [CARD_NAME] lets you return target nonland permanent to its owner's hand.",

        "Flash. When [CARD_NAME] arrives, you may return target nonland permanent to its owner's hand.",

        "Flash. When [CARD_NAME] enters the battlefield, you may bounce target nonland permanent.",

        "Flash. When [CARD_NAME] enters the battlefield, you may return target nonland permanent to hand.",

        "Flash. When [CARD_NAME] enters the battlefield, you may return a target nonland permanent to its owner's hand.",

        "Flash. When [CARD_NAME] enters the battlefield, you may return target nonland permanent to its owner's hand.",

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
            least_mana={"colorless":3,"U":1}
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

