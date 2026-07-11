from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Avenging_Light.model import Avenging_Light

@bind_card(Avenging_Light)
class Avenging_Light_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Exile target nonland permanent. If it was a creature, you gain life equal to its power.",
        "[CARD_NAME] exiles target nonland permanent. If it was a creature, gain life equal to its power.",
        "Exile a nonland permanent. If it's a creature, you gain life equal to its power.",
        "Remove target nonland permanent from the game. If it was a creature, gain life equal to its power.",
        "[CARD_NAME]: exile target nonland permanent; if it was a creature, gain life equal to its power.",
        "Exile target nonland permanent. You gain life equal to its power if it was a creature.",
        "Target nonland permanent is exiled. If it was a creature, you gain life equal to its power.",
        "With [CARD_NAME], exile a nonland permanent and gain life equal to its power if it was a creature.",
        "Exile target nonland permanent. When it's a creature, you gain life equal to its power.",
        "Banish target nonland permanent. If it was a creature, gain life equal to its power.",
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
            {"W":(1,7)},
            least_mana={"colorless":3,"W":1}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
