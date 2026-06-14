from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Flameblade_Pyromancer.model import Flameblade_Pyromancer

@bind_card(Flameblade_Pyromancer)
class Flameblade_Pyromancer_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "When [CARD_NAME] enters the battlefield, you may discard a card. If you do, it deals 2 damage to target creature or player.",

        "When [CARD_NAME] enters play, you may discard a card. If you do, it deals 2 damage to target creature or player.",

        "As [CARD_NAME] enters the battlefield, you may discard a card. If you do, it deals 2 damage to target creature or player.",

        "Upon entering the battlefield, [CARD_NAME] lets you discard a card to deal 2 damage to target creature or player.",

        "When [CARD_NAME] arrives, you may discard a card. If you do, it deals 2 damage to target creature or player.",

        "When [CARD_NAME] enters the battlefield, you may discard a card. If you do, deal 2 damage to target creature or player.",

        "When [CARD_NAME] enters the battlefield, you may discard a card. If you do, it deals two damage to target creature or player.",

        "When [CARD_NAME] enters the battlefield, you may discard a card. If you do, it inflicts 2 damage on target creature or player.",

        "When [CARD_NAME] enters the battlefield, you may discard a card. If you do, it deals 2 damage to a target creature or player.",

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
            {"R":(1,7)},
            least_mana={"colorless":1,"R":1}
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

