from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Eternal_Phoenix.model import Eternal_Phoenix

@bind_card(Eternal_Phoenix)
class Eternal_Phoenix_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Flying. When [CARD_NAME] dies, if it didn't have a feather counter on it, return it to the battlefield with a feather counter on it instead of putting it into your graveyard.",

        "Flying. When [CARD_NAME] dies without a feather counter, return it to the battlefield with a feather counter instead of going to your graveyard.",

        "Flying. If [CARD_NAME] dies without a feather counter, return it to the battlefield with a feather counter rather than putting it in your graveyard.",

        "Flying. When [CARD_NAME] is put into a graveyard from the battlefield, if it had no feather counter, return it with a feather counter instead.",

        "Flying. When [CARD_NAME] dies, if it lacks a feather counter, return it to the battlefield with one instead of going to the graveyard.",

        "Flying. When [CARD_NAME] dies without a feather counter, it returns to the battlefield with a feather counter instead of entering your graveyard.",

        "Flying. When [CARD_NAME] dies, if no feather counter is on it, return it to the battlefield with a feather counter instead of your graveyard.",

        "Flying. When [CARD_NAME] dies, if it didn't have a feather counter, return it to play with a feather counter instead of the graveyard.",

        "Flying. When [CARD_NAME] dies without a feather counter, put it back on the battlefield with a feather counter instead of your graveyard.",

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
            least_mana={"colorless":2,"R":2}
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

