from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Thornwood_Guardian.model import Thornwood_Guardian

@bind_card(Thornwood_Guardian)
class Thornwood_Guardian_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Reach, Trample (This creature can block creatures with flying, and it can deal excess combat damage to the player or planeswalker it's attacking).",

        "Trample, Reach.",

        "Trample, Reach (can block flyers and deal excess combat damage).",

        "Reach. Trample (blocks flying creatures and deals excess damage).",

        "Trample, Reach (can block creatures with flying and deal excess combat damage).",

        "Reach, Trample (blocks flying and deals excess damage to attacked player or planeswalker).",

        "Trample, Reach (can block flying creatures; excess damage goes to the player or planeswalker).",

        "Reach, Trample (can block flyers; deals excess combat damage to the player or planeswalker it's attacking).",

        "Trample, Reach (can block creatures with flying and deal excess combat damage to the attacked player or planeswalker).",

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
            {"G":(2,7)},
            least_mana={"colorless":3,"G":2}
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

