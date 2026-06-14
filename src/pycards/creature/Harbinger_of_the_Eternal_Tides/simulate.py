from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Harbinger_of_the_Eternal_Tides.model import Harbinger_of_the_Eternal_Tides

@bind_card(Harbinger_of_the_Eternal_Tides)
class Harbinger_of_the_Eternal_Tides_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Flash. When [CARD_NAME] enters the battlefield, tap target creature an opponent controls. It doesn't untap during its controller's next untap step.",

        "Flash. When [CARD_NAME] enters play, tap target creature an opponent controls. It doesn't untap during its controller's next untap step.",

        "Flash. As [CARD_NAME] enters the battlefield, tap target creature an opponent controls. It won't untap during its controller's next untap step.",

        "Flash. Upon entering the battlefield, [CARD_NAME] taps target creature an opponent controls. It doesn't untap during its controller's next untap step.",

        "Flash. When [CARD_NAME] arrives, tap target creature an opponent controls. It doesn't untap during its controller's next untap step.",

        "Flash. When [CARD_NAME] enters the battlefield, tap an opposing creature. It doesn't untap during its controller's next untap step.",

        "Flash. When [CARD_NAME] enters the battlefield, tap target creature an opponent controls. That creature skips untapping during its controller's next untap step.",

        "Flash. When [CARD_NAME] enters the battlefield, tap a target creature an opponent controls. It doesn't untap during its controller's next untap step.",

        "Flash. When [CARD_NAME] enters the battlefield, tap target opposing creature. It doesn't untap during its controller's next untap step.",

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
            least_mana={"colorless":2,"U":2}
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

