from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Grove_Guardian.model import Grove_Guardian

@bind_card(Grove_Guardian)
class Grove_Guardian_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Reach, Hexproof (This creature can't be the target of spells or abilities your opponents control).",

        "Hexproof, Reach.",

        "Hexproof, Reach (can't be targeted by opponents' spells or abilities).",

        "Hexproof. Reach (opponents can't target this with spells or abilities).",

        "Reach, Hexproof (this can't be the target of opposing spells or abilities).",

        "Hexproof, Reach (immune to opposing targeting).",

        "Reach, Hexproof (opponents cannot target this creature).",

        "Hexproof, Reach (not targetable by opponent spells or abilities).",

        "Reach, Hexproof (your opponents can't target this).",

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

