from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Luminous_Angel.model import Luminous_Angel

@bind_card(Luminous_Angel)
class Luminous_Angel_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Flying, Lifelink. At the beginning of your upkeep, if you have at least 20 life, [CARD_NAME] gets +1/+1.",

        "Lifelink, Flying. At the start of your upkeep, if you have 20 or more life, [CARD_NAME] gets +1/+1.",

        "Flying, Lifelink. During your upkeep, if your life total is 20 or higher, [CARD_NAME] gets +1/+1.",

        "Lifelink, Flying. At the beginning of your upkeep, if you have 20+ life, [CARD_NAME] gets +1/+1.",

        "Flying, Lifelink. At your upkeep, if you have at least 20 life, [CARD_NAME] grows by +1/+1.",

        "Lifelink, Flying. At the beginning of your upkeep, if your life total is at least 20, [CARD_NAME] gets +1/+1.",

        "Flying, Lifelink. At the beginning of your upkeep, if you have twenty or more life, [CARD_NAME] gets +1/+1.",

        "Lifelink, Flying. At the beginning of your upkeep, if you have at least 20 life, [CARD_NAME] gains +1/+1.",

        "Flying, Lifelink. At the beginning of your upkeep, if you have 20 or more life, [CARD_NAME] receives +1/+1.",

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

