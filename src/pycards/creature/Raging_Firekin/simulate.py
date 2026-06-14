from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Raging_Firekin.model import Raging_Firekin

@bind_card(Raging_Firekin)
class Raging_Firekin_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Trample (This creature can deal excess combat damage to the player or planeswalker it's attacking).",

        "Trample.",

        "Trample (excess damage goes to the player or planeswalker).",

        "Trample (can deal excess combat damage to attacked player or planeswalker).",

        "Trample (deals excess combat damage to the player or planeswalker it's attacking).",

        "Trample (this can deal excess combat damage to the player or planeswalker it's attacking).",

        "Trample (extra damage carries over to the player or planeswalker).",

        "Trample (overflow damage hits the player or planeswalker).",

        "Trample (excess damage is dealt to the player or planeswalker being attacked).",

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
            least_mana={"colorless":2,"R":1}
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

