from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Divine_Sanctuary.model import Divine_Sanctuary

@bind_card(Divine_Sanctuary)
class Divine_Sanctuary_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Until the end of your turn, you and all creatures you control gain immunity to all effects.",
        "[CARD_NAME] grants you and your creatures immunity to all effects until end of your turn.",
        "You and creatures you control have immunity to all effects until end of your turn.",
        "Until end of your turn, you and your creatures can't be affected by any effects.",
        "[CARD_NAME]: full immunity for you and your creatures until end of your turn.",
        "Grant immunity to all effects to you and your creatures until end of your turn.",
        "You and all creatures you control are immune to all effects until end of your turn.",
        "With [CARD_NAME], you and your creatures gain total immunity until end of your turn.",
        "Immunity to all effects for you and your creatures until end of your turn.",
        "[CARD_NAME] makes you and your creatures immune to all effects this turn.",
    ]

    @simulate
    def simulate_card(self):
        self.basic_initinal()
        self.room.env_creature(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"W":(2,7)},
            least_mana={"colorless":4,"W":2}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
