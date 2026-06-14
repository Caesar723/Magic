from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Guardian_of_the_Grove__.model import Guardian_of_the_Grove__

@bind_card(Guardian_of_the_Grove__)
class Guardian_of_the_Grove___Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Whenever [CARD_NAME] enters the battlefield, you may search your library for a basic Forest card and put it onto the battlefield tapped.",

        "When [CARD_NAME] enters the battlefield, you may search your library for a basic Forest and put it onto the battlefield tapped.",

        "As [CARD_NAME] enters the battlefield, you may search your library for a basic Forest card and put it onto the battlefield tapped.",

        "Upon entering the battlefield, [CARD_NAME] lets you search for a basic Forest and put it onto the battlefield tapped.",

        "When [CARD_NAME] arrives, you may search your library for a basic Forest card and put it onto the battlefield tapped.",

        "When [CARD_NAME] enters the battlefield, you may find a basic Forest in your library and put it onto the battlefield tapped.",

        "When [CARD_NAME] enters the battlefield, you may search your library for a basic Forest and place it onto the battlefield tapped.",

        "When [CARD_NAME] enters the battlefield, you may search for a basic Forest card and put it onto the battlefield tapped.",

        "When [CARD_NAME] enters the battlefield, you may search your library for a basic Forest and put it on the battlefield tapped.",

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
            least_mana={"colorless":1,"W":2}
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

