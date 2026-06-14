from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Celestial_Herald.model import Celestial_Herald

@bind_card(Celestial_Herald)
class Celestial_Herald_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Flying, Lifelink. At the beginning of your upkeep, exile a random nonland permanent an opponent controls. Return that permanent to the battlefield under its owner's control at the beginning of the next end step.",

        "Lifelink, Flying. At the start of your upkeep, exile a random nonland permanent an opponent controls, then return it at the beginning of the next end step.",

        "Flying, Lifelink. During your upkeep, exile a random nonland permanent an opponent controls. It returns under its owner's control at the next end step.",

        "Lifelink, Flying. At the beginning of your upkeep, temporarily exile a random nonland permanent an opponent controls until the next end step.",

        "Flying, Lifelink. At the beginning of your upkeep, exile a random nonland permanent controlled by an opponent. Return it at the beginning of the next end step.",

        "Lifelink, Flying. At your upkeep, exile a random nonland opposing permanent and return it at the beginning of the next end step.",

        "Flying, Lifelink. At the beginning of your upkeep, banish a random nonland permanent an opponent controls until the next end step.",

        "Lifelink, Flying. At the beginning of your upkeep, exile a random nonland permanent an opponent owns. Return it at the next end step.",

        "Flying, Lifelink. At the beginning of your upkeep, exile a random nonland permanent an opponent controls, returning it at the beginning of the next end step.",

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
            {"W":(2,7)},
            least_mana={"colorless":3,"W":2}
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
