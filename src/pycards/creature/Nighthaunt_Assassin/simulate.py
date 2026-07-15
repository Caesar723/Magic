from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Nighthaunt_Assassin.model import Nighthaunt_Assassin

@bind_card(Nighthaunt_Assassin)
class Nighthaunt_Assassin_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "When [CARD_NAME] enters the battlefield, you may destroy a random creature an opponent controls with converted mana cost 2 or less.",

        "When [CARD_NAME] enters play, you may destroy a random opposing creature with mana value 2 or less.",

        "As [CARD_NAME] enters the battlefield, you may destroy a random creature an opponent controls with CMC 2 or less.",

        "Upon entering the battlefield, [CARD_NAME] lets you destroy a random opposing creature with converted mana cost 2 or less.",

        "When [CARD_NAME] arrives, you may destroy a random creature an opponent controls with mana value 2 or less.",

        "When [CARD_NAME] enters the battlefield, you may destroy a random opponent's creature with converted mana cost 2 or less.",

        "When [CARD_NAME] enters the battlefield, you may destroy a random creature an opponent controls costing 2 or less.",

        "When [CARD_NAME] enters the battlefield, you may destroy a random opposing creature with CMC 2 or less.",

        "When [CARD_NAME] enters the battlefield, you may destroy a random creature an opponent controls with mana cost 2 or less.",

    ]
    @simulate
    def simulate_when_enter_battlefield(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        # Testing creatures cost one mana, so the Assassin always has an
        # eligible opposing creature for its enter-the-battlefield effect.
        self.room.env_creature(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"B":(1,7)},
            least_mana={"colorless":2,"B":1}
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
