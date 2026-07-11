from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Unyielding_Resolve.model import Unyielding_Resolve

@bind_card(Unyielding_Resolve)
class Unyielding_Resolve_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] gives all creatures you control indestructible until end of turn. Creatures you control gain lifelink until end of turn.",

        "Creatures you control gain indestructible and lifelink until end of turn.",

        "[CARD_NAME] grants all creatures you control indestructible and lifelink until end of turn.",

        "Until end of turn, creatures you control have indestructible and lifelink.",

        "[CARD_NAME] makes all creatures you control indestructible until end of turn and gives them lifelink until end of turn.",

        "All creatures you control gain indestructible until end of turn and lifelink until end of turn.",

        "[CARD_NAME] causes creatures you control to gain indestructible and lifelink until end of turn.",

        "Until end of turn, all creatures you control are indestructible and have lifelink.",

        "[CARD_NAME] gives your creatures indestructible until end of turn and lifelink until end of turn.",

        "Creatures you control have indestructible and lifelink until end of turn."
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
            least_mana={"colorless": 2, "W": 2},
        )

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
