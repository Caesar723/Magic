from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Spectral_Harbinger.model import Spectral_Harbinger

@bind_card(Spectral_Harbinger)
class Spectral_Harbinger_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Flying, Lifelink. When [CARD_NAME] enters the battlefield, you may exile a random creature card from a graveyard. If you do, you gain 2 life.",

        "Lifelink, Flying. When [CARD_NAME] enters play, you may exile a random creature card from a graveyard. If you do, you gain 2 life.",

        "Flying, Lifelink. As [CARD_NAME] enters the battlefield, you may exile a random creature card from a graveyard. If you do, you gain 2 life.",

        "Lifelink, Flying. Upon entering the battlefield, [CARD_NAME] lets you exile a random creature card from a graveyard. If you do, you gain 2 life.",

        "Flying, Lifelink. When [CARD_NAME] arrives, you may exile a random creature card from a graveyard. If you do, you gain 2 life.",

        "Lifelink, Flying. When [CARD_NAME] enters the battlefield, you may exile a random creature card from any graveyard. If you do, you gain 2 life.",

        "Flying, Lifelink. When [CARD_NAME] enters the battlefield, you may exile a random creature from a graveyard. If you do, you gain 2 life.",

        "Lifelink, Flying. When [CARD_NAME] enters the battlefield, you may exile a random creature card from a graveyard. If you do, gain 2 life.",

        "Flying, Lifelink. When [CARD_NAME] enters the battlefield, you may exile a random creature card from a graveyard. If you do, you gain two life.",

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
            least_mana={"colorless":2,"W":2}
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

