from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Shadow_Snare.model import Shadow_Snare

@bind_card(Shadow_Snare)
class Shadow_Snare_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Target creature gets -3/-3 until end of turn.",
        "[CARD_NAME] gives target creature -3/-3 until end of turn.",
        "Choose a creature. It gets -3/-3 this turn.",
        "-3/-3 until end of turn on target creature.",
        "[CARD_NAME]: -3/-3 debuff until end of turn.",
        "Weaken target creature by -3/-3 until end of turn.",
        "Target creature suffers -3/-3 this turn.",
        "With [CARD_NAME], apply -3/-3 to a creature until end of turn.",
        "Give -3/-3 to target creature until end of turn.",
        "[CARD_NAME] snares a creature with -3/-3 until end of turn.",
    ]

    @simulate
    def simulate_card(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.room.env_creature(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"B":(1,7)},
            least_mana={"colorless":2,"B":1}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
