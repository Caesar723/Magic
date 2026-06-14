from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Angelic_Protector.model import Angelic_Protector

@bind_card(Angelic_Protector)
class Angelic_Protector_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "When [CARD_NAME] enters the battlefield, you may tap target creature. It doesn't untap during its controller's next untap step.",

        "When [CARD_NAME] enters play, you may tap a target creature. That creature remains tapped through its controller's next untap step.",

        "As [CARD_NAME] enters the battlefield, you may tap target creature. It won't untap during its controller's next untap step.",

        "When [CARD_NAME] arrives on the battlefield, you may tap any target creature. It doesn't untap on its controller's next untap.",

        "Upon entering the battlefield, [CARD_NAME] lets you tap target creature, which stays tapped through the next untap step of its controller.",

        "When [CARD_NAME] enters the battlefield, you may choose a target creature and tap it. It doesn't untap during its controller's next untap step.",

        "When [CARD_NAME] enters the battlefield, you may tap one target creature. That creature skips untapping during its controller's next untap step.",

        "When [CARD_NAME] enters the battlefield, you may tap a creature of your choice. It remains tapped until after its controller's next untap step.",

        "When [CARD_NAME] enters the battlefield, you may tap target creature. It cannot untap during its controller's next untap step.",

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
            least_mana={"colorless":1,"W":1}
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
