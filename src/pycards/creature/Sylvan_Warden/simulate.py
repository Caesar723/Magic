from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Sylvan_Warden.model import Sylvan_Warden

@bind_card(Sylvan_Warden)
class Sylvan_Warden_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "When [CARD_NAME] enters the battlefield, you may search your library for a basic land card and put it onto the battlefield tapped. If you do, shuffle your library. Whenever [CARD_NAME] attacks, you may put a +1/+1 counter on target creature you control.",

        "When [CARD_NAME] enters play, you may search for a basic land, put it onto the battlefield tapped, and shuffle. Whenever [CARD_NAME] attacks, you may put a +1/+1 counter on target creature you control.",

        "As [CARD_NAME] enters the battlefield, you may search your library for a basic land, put it onto the battlefield tapped, shuffle if you do. Whenever [CARD_NAME] attacks, you may put a +1/+1 counter on target creature you control.",

        "Upon entering the battlefield, [CARD_NAME] lets you search for a basic land and put it onto the battlefield tapped, then shuffle. Whenever [CARD_NAME] attacks, you may put a +1/+1 counter on target creature you control.",

        "When [CARD_NAME] arrives, you may search for a basic land, put it onto the battlefield tapped, shuffle. Whenever [CARD_NAME] attacks, you may put a +1/+1 counter on target creature you control.",

        "When [CARD_NAME] enters the battlefield, you may find a basic land, put it onto the battlefield tapped, shuffle if you do. Whenever [CARD_NAME] attacks, you may put a +1/+1 counter on target creature you control.",

        "When [CARD_NAME] enters the battlefield, you may search your library for a basic land card, put it onto the battlefield tapped, shuffle if you do. On attack, you may put a +1/+1 counter on target creature you control.",

        "When [CARD_NAME] enters the battlefield, you may search for a basic land and put it onto the battlefield tapped, then shuffle. Each time [CARD_NAME] attacks, you may put a +1/+1 counter on target creature you control.",

        "When [CARD_NAME] enters the battlefield, you may search your library for a basic land, put it onto the battlefield tapped, shuffle if you do. Whenever [CARD_NAME] attacks, you may place a +1/+1 counter on target creature you control.",

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
            {"G":(1,7)},
            least_mana={"colorless":4,"G":1}
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

