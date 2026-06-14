from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Titan_Giant.model import Titan_Giant

@bind_card(Titan_Giant)
class Titan_Giant_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "When [CARD_NAME] enters the battlefield, destroy all other creatures with power less than 5.",

        "When [CARD_NAME] enters play, destroy all other creatures with power less than 5.",

        "As [CARD_NAME] enters the battlefield, destroy all other creatures with power less than 5.",

        "Upon entering the battlefield, [CARD_NAME] destroys all other creatures with power less than 5.",

        "When [CARD_NAME] arrives, destroy all other creatures with power less than 5.",

        "When [CARD_NAME] enters the battlefield, destroy every other creature with power less than 5.",

        "When [CARD_NAME] enters the battlefield, destroy all other creatures with power 4 or less.",

        "When [CARD_NAME] enters the battlefield, destroy all other creatures with power below 5.",

        "When [CARD_NAME] enters the battlefield, destroy all other creatures that have power less than 5.",

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
            least_mana={"colorless":5,"G":2}
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

