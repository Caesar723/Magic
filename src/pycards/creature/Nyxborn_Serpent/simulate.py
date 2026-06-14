from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Nyxborn_Serpent.model import Nyxborn_Serpent

@bind_card(Nyxborn_Serpent)
class Nyxborn_Serpent_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Constellation — Whenever [CARD_NAME] enters the battlefield under your control, you may tap target creature an opponent controls.",

        "Constellation — When [CARD_NAME] enters the battlefield under your control, you may tap target creature an opponent controls.",

        "Constellation — As [CARD_NAME] enters the battlefield under your control, you may tap target creature an opponent controls.",

        "Constellation — Upon entering under your control, [CARD_NAME] lets you tap target creature an opponent controls.",

        "Constellation — When [CARD_NAME] enters under your control, you may tap target creature an opponent controls.",

        "Constellation — Whenever [CARD_NAME] enters the battlefield under your control, you may tap an opposing creature.",

        "Constellation — Whenever [CARD_NAME] enters under your control, you may tap target creature an opponent controls.",

        "Constellation — Whenever [CARD_NAME] enters the battlefield under your control, you may tap a target creature an opponent controls.",

        "Constellation — Whenever [CARD_NAME] enters the battlefield under your control, you may tap target opposing creature.",

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
            {"U":(1,7)},
            least_mana={"colorless":3,"U":1}
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

