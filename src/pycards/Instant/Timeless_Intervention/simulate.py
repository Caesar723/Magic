from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Timeless_Intervention.model import Timeless_Intervention

@bind_card(Timeless_Intervention)
class Timeless_Intervention_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Exile all creatures and planeswalkers. Return all exiled creatures and planeswalkers to the battlefield under their owners' control at the beginning of the next end step.",
        "[CARD_NAME] exiles all creatures and planeswalkers, then returns them at the next end step.",
        "Exile all creatures and planeswalkers. They return at beginning of next end step.",
        "Blink all creatures and planeswalkers—they return next end step.",
        "[CARD_NAME]: mass exile creatures and planeswalkers; return next end step.",
        "Exile every creature and planeswalker. They come back at next end step.",
        "All creatures and planeswalkers exiled temporarily; return next end step.",
        "With [CARD_NAME], exile all creatures and planeswalkers and return them next end step.",
        "Mass exile creatures and planeswalkers; they re-enter at next end step.",
        "[CARD_NAME] blinks all creatures and planeswalkers until next end step.",
    ]

    @simulate
    def simulate_card(self):
        self.basic_initinal()
        self.room.env_creature(self.player)
        self.random_life()(self.player)
        self.room.env_creature(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"G":(1,7),"W":(1,7)},
            least_mana={"colorless":2,"G":1,"W":1}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
