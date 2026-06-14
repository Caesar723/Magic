from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Seraph_of_the_Eternal_Flame.model import Seraph_of_the_Eternal_Flame

@bind_card(Seraph_of_the_Eternal_Flame)
class Seraph_of_the_Eternal_Flame_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Radiant Aura — Whenever [CARD_NAME] attacks, creatures you control gain indestructible until end of turn.",

        "Radiant Aura — Each time [CARD_NAME] attacks, creatures you control gain indestructible until end of turn.",

        "Radiant Aura — When [CARD_NAME] attacks, your creatures gain indestructible until end of turn.",

        "Radiant Aura — On attack, [CARD_NAME] grants indestructible to creatures you control until end of turn.",

        "Radiant Aura — Whenever [CARD_NAME] attacks, all creatures you control gain indestructible until end of turn.",

        "Radiant Aura — Whenever [CARD_NAME] attacks, creatures you control become indestructible until end of turn.",

        "Radiant Aura — Whenever [CARD_NAME] attacks, creatures you control can't be destroyed until end of turn.",

        "Radiant Aura — Whenever [CARD_NAME] attacks, your creatures are indestructible until end of turn.",

        "Radiant Aura — Whenever [CARD_NAME] attacks, creatures under your control gain indestructible until end of turn.",

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

