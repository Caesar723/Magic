from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Vengeful_Retribution.model import Vengeful_Retribution

@bind_card(Vengeful_Retribution)
class Vengeful_Retribution_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Opponent sacrifices two random creatures. If a creature was sacrificed this way, [CARD_NAME] deals damage to random target equal to the total power of the sacrificed creatures.",
        "[CARD_NAME] makes opponent sacrifice two random creatures; deals damage equal to total power to random target if any sacrificed.",
        "Opponent sacrifices two random creatures. Damage random target for total sacrificed power if any died.",
        "Force opponent to sacrifice two random creatures. Damage equal to total power to random target.",
        "[CARD_NAME]: opponent sacrifices two random creatures; damage based on total power.",
        "Opponent sacrifices two creatures at random. [CARD_NAME] damages random target for their total power.",
        "Two random opponent creatures sacrificed. Damage random target equal to combined power.",
        "With [CARD_NAME], opponent sacrifices two random creatures; retribution damage equals total power.",
        "Opponent sacrifices two random creatures. If so, damage random target for total power.",
        "[CARD_NAME] forces sacrifices and deals damage equal to total sacrificed power.",
    ]

    @simulate
    def simulate_card(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.room.env_creature(self.player.opponent)
        while len(self.player.opponent.battlefield)<3:
            creature=self.player.opponent.battlefield[0]
            self.player.opponent.battlefield.append(type(creature)(self.player.opponent))
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"B":(1,7)},
            least_mana={"colorless":4,"B":1}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
