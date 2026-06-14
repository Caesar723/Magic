from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Blightsteel_Colossus.model import Blightsteel_Colossus

@bind_card(Blightsteel_Colossus)
class Blightsteel_Colossus_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Trample, Infect, Indestructible.",

        "Infect, Indestructible, Trample (damage to creatures is -1/-1 counters; damage to players is poison counters).",

        "Indestructible, Trample, Infect (can't be destroyed by damage or effects that say destroy).",

        "Infect. Trample. Indestructible.",

        "Indestructible, Infect, and Trample.",

        "Infect, Trample (this deals damage as -1/-1 counters to creatures and poison counters to players), Indestructible.",

        "Trample, Indestructible, Infect — this creature can't be destroyed by damage or destroy effects.",

        "Indestructible, Infect, Trample (immune to damage-based destruction and destroy effects).",

        "Infect, Indestructible, Trample (this creature can't be destroyed by damage or destroy effects).",

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
            {},
            least_mana={"colorless":12}
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
