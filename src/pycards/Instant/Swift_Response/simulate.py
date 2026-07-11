from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Swift_Response.model import Swift_Response

@bind_card(Swift_Response)
class Swift_Response_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Instantly destroy target attacking or blocking creature with power 2 or less.",
        "[CARD_NAME] destroys target attacking or blocking creature with power 2 or less.",
        "Destroy an attacking or blocking creature with power 2 or less.",
        "Choose attacking or blocking creature with power ≤2. Destroy it.",
        "[CARD_NAME]: destroy small attacking/blocking creature (power 2 or less).",
        "Eliminate target attacking or blocking creature with power 2 or less.",
        "Destroy weak attacking or blocking creatures (power 2 or less).",
        "With [CARD_NAME], kill attacking or blocking creature with power 2 or less.",
        "Target attacking or blocking creature with power 2 or less is destroyed.",
        "[CARD_NAME] removes attacking or blocking creatures with power 2 or less.",
    ]

    @simulate
    def simulate_card(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.room.env_creature(self.player.opponent)
        for creature in self.player.opponent.battlefield:
            creature.power=min(2,creature.power)
            creature.actual_power=min(2,creature.actual_power)
        self.room.attacker=self.player.opponent.battlefield[0]
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"W":(2,7)},
            least_mana={"colorless":1,"W":2}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
