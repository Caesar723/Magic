from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Divine_Blessing.model import Divine_Blessing

@bind_card(Divine_Blessing)
class Divine_Blessing_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Target creature gets +2/+2 and lifelink until end of turn.",

        "[CARD_NAME] gives target creature +2/+2 and lifelink until end of turn.",

        "Target creature gets +2/+2 and gains lifelink until end of turn.",

        "[CARD_NAME] grants target creature +2/+2 and lifelink until end of turn.",

        "Choose target creature. It gets +2/+2 and gains lifelink until end of turn.",

        "[CARD_NAME] causes target creature to get +2/+2 and gain lifelink until end of turn.",

        "Until end of turn, target creature gets +2/+2 and has lifelink.",

        "[CARD_NAME] buffs target creature with +2/+2 and lifelink until end of turn.",

        "Target creature receives +2/+2 and gains lifelink until end of turn.",

        "[CARD_NAME] gives a target creature +2/+2 and lifelink until end of turn."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"W": (2, 7)},
            least_mana={"colorless": 1, "W": 2},
        )

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
