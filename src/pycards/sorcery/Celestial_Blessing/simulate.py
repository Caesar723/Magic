from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Celestial_Blessing.model import Celestial_Blessing

@bind_card(Celestial_Blessing)
class Celestial_Blessing_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Choose one target creature you control and another target creature nearby. They gain lifelink until end of turn.",

        "[CARD_NAME] lets you choose one creature you control and another nearby creature. They gain lifelink until end of turn.",

        "Choose a creature you control and another nearby creature. Both gain lifelink until end of turn.",

        "[CARD_NAME] causes one creature you control and another nearby creature to gain lifelink until end of turn.",

        "Select one creature you control and another nearby creature. They gain lifelink until end of turn.",

        "[CARD_NAME] grants lifelink until end of turn to one creature you control and another nearby creature.",

        "Choose one of your creatures and another nearby creature. Both gain lifelink until end of turn.",

        "[CARD_NAME] gives lifelink until end of turn to a creature you control and another nearby creature.",

        "Pick one creature you control and another nearby creature. They gain lifelink until end of turn.",

        "[CARD_NAME] allows you to choose one creature you control and another nearby creature, giving them lifelink until end of turn."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.room.env_creature(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"W": (2, 7)},
            least_mana={"colorless": 1, "W": 2},
        )

        if len(self.player.battlefield) < 2:
            creature_type = type(self.player.battlefield[0])
            self.player.battlefield.append(creature_type(self.player))

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
