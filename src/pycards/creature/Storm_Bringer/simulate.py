from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Storm_Bringer.model import Storm_Bringer

@bind_card(Storm_Bringer)
class Storm_Bringer_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Flying. When [CARD_NAME] enters the battlefield, it deals 3 damage to each opponent and you gain 3 life.",

        "Flying. When [CARD_NAME] enters play, it deals 3 damage to each opponent and you gain 3 life.",

        "Flying. As [CARD_NAME] enters the battlefield, it deals 3 damage to each opponent and you gain 3 life.",

        "Flying. Upon entering the battlefield, [CARD_NAME] deals 3 damage to each opponent and you gain 3 life.",

        "Flying. When [CARD_NAME] arrives, it deals 3 damage to each opponent and you gain 3 life.",

        "Flying. When [CARD_NAME] enters the battlefield, deal 3 damage to each opponent and gain 3 life.",

        "Flying. When [CARD_NAME] enters the battlefield, it deals three damage to each opponent and you gain three life.",

        "Flying. When [CARD_NAME] enters the battlefield, it damages each opponent for 3 and you gain 3 life.",

        "Flying. When [CARD_NAME] enters the battlefield, it deals 3 damage to every opponent and you gain 3 life.",

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
            {"U":(2,7)},
            least_mana={"colorless":4,"U":2}
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

