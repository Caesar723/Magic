from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Apocalypse_Riders.model import Apocalypse_Riders

@bind_card(Apocalypse_Riders)
class Apocalypse_Riders_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Summon four 2/2 Knight creature tokens, each with a different ability (Trample, Haste, Lifelink, Flying).",

        "[CARD_NAME] creates four 2/2 Knight creature tokens, each with a different keyword ability: Haste, Lifelink, Flying, and Trample.",

        "Create four 2/2 Knight tokens. One has flying, one has haste, one has lifelink, and one has trample.",

        "[CARD_NAME] summons four 2/2 Knight creature tokens with distinct abilities: Lifelink, Flying, Trample, and Haste.",

        "Put four 2/2 Knight creature tokens onto the battlefield, each granted a different ability among Flying, Trample, Haste, and Lifelink.",

        "[CARD_NAME] generates four 2/2 Knight creature tokens, each with one of Haste, Trample, Lifelink, or Flying.",

        "Summon four Knight creature tokens that are 2/2, each with a unique ability: Lifelink, Haste, Trample, or Flying.",

        "[CARD_NAME] places four 2/2 Knight tokens into play, each bearing a different ability from Flying, Lifelink, Haste, and Trample.",

        "Create four 2/2 Knight creature tokens. Each token has a different ability: Haste, Flying, Lifelink, or Trample.",

        "[CARD_NAME] brings four 2/2 Knight creature tokens onto the battlefield, each with a separate ability among Lifelink, Trample, Flying, and Haste."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.room.env_no_creature(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"W": (2, 7)},
            least_mana={"colorless": 5, "W": 2},
        )

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
