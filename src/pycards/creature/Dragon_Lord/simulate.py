from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Dragon_Lord.model import Dragon_Lord

@bind_card(Dragon_Lord)
class Dragon_Lord_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Flying. Whenever [CARD_NAME] deals damage to an opponent, create two 4/4 red Dragon creature tokens.",

        "Flying. Each time [CARD_NAME] deals damage to an opponent, create two 4/4 red Dragon creature tokens.",

        "Flying. When [CARD_NAME] deals damage to an opponent, create two 4/4 red Dragon creature tokens.",

        "Flying. Whenever [CARD_NAME] damages an opponent, create two 4/4 red Dragon creature tokens.",

        "Flying. On dealing damage to an opponent, [CARD_NAME] creates two 4/4 red Dragon creature tokens.",

        "Flying. Whenever [CARD_NAME] deals combat damage to an opponent, create two 4/4 red Dragon creature tokens.",

        "Flying. Whenever [CARD_NAME] deals damage to an opponent, spawn two 4/4 red Dragon creature tokens.",

        "Flying. Whenever [CARD_NAME] deals damage to an opponent, put two 4/4 red Dragon creature tokens onto the battlefield.",

        "Flying. Whenever [CARD_NAME] deals damage to an opponent, you create two 4/4 red Dragon creature tokens.",

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
            {"R":(2,7)},
            least_mana={"colorless":6,"R":2}
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

