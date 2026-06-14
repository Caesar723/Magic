from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Avacyn__Guardian_of_Hope.model import Avacyn__Guardian_of_Hope

@bind_card(Avacyn__Guardian_of_Hope)
class Avacyn__Guardian_of_Hope_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Flying, Vigilance, Lifelink. When [CARD_NAME] enters the battlefield, creatures you control gain indestructible until end of turn.",

        "Vigilance, Lifelink, Flying. When [CARD_NAME] enters play, your creatures become indestructible until end of turn.",

        "Lifelink, Flying, Vigilance. As [CARD_NAME] enters the battlefield, all creatures you control gain indestructible until end of turn.",

        "Flying, Lifelink, Vigilance. Upon entering the battlefield, [CARD_NAME] grants indestructible to creatures you control until end of turn.",

        "Vigilance, Flying, Lifelink. When [CARD_NAME] arrives, each creature you control gains indestructible until end of turn.",

        "Lifelink, Vigilance, Flying. When [CARD_NAME] enters the battlefield, your creatures can't be destroyed until end of turn.",

        "Flying, Vigilance, Lifelink. When [CARD_NAME] enters the battlefield, creatures under your control gain indestructible for the rest of the turn.",

        "Vigilance, Lifelink, Flying. When [CARD_NAME] enters the battlefield, all your creatures become indestructible until the turn ends.",

        "Lifelink, Flying, Vigilance. When [CARD_NAME] enters the battlefield, creatures you control are indestructible until end of turn.",

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
            {"W":(1,7)},
            least_mana={"colorless":5,"W":1}
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
