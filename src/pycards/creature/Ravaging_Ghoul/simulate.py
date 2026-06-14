from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Ravaging_Ghoul.model import Ravaging_Ghoul

@bind_card(Ravaging_Ghoul)
class Ravaging_Ghoul_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "When [CARD_NAME] enters the battlefield, target opponent loses 2 life.",

        "When [CARD_NAME] enters play, target opponent loses 2 life.",

        "As [CARD_NAME] enters the battlefield, target opponent loses 2 life.",

        "Upon entering the battlefield, [CARD_NAME] causes target opponent to lose 2 life.",

        "When [CARD_NAME] arrives, target opponent loses 2 life.",

        "When [CARD_NAME] enters the battlefield, a target opponent loses 2 life.",

        "When [CARD_NAME] enters the battlefield, target opponent loses two life.",

        "When [CARD_NAME] enters the battlefield, target opponent's life total decreases by 2.",

        "When [CARD_NAME] enters the battlefield, target opponent loses 2 life points.",

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
            {"B":(1,7)},
            least_mana={"colorless":1,"B":1}
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

