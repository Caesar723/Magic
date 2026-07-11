from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Summoner_s_Respite.model import Summoner_s_Respite

@bind_card(Summoner_s_Respite)
class Summoner_s_Respite_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Prevent all combat damage that would be dealt this turn. You gain 4 life. Put a +1/+1 counter on each creature you control.",
        "[CARD_NAME] prevents all combat damage, you gain 4 life, and each your creature gets +1/+1.",
        "Fog all combat damage. Gain 4 life. +1/+1 counter on each creature you control.",
        "No combat damage this turn. Gain 4 life. Buff all your creatures +1/+1.",
        "[CARD_NAME]: combat fog, gain 4 life, +1/+1 on all your creatures.",
        "Prevent combat damage. Gain 4 life. Put +1/+1 on each creature you control.",
        "All combat damage prevented. You gain 4 life. Your creatures get +1/+1 counters.",
        "With [CARD_NAME], fog combat, heal 4, and +1/+1 all your creatures.",
        "Prevent all combat damage. Gain 4 life. +1/+1 counter on your creatures.",
        "[CARD_NAME] fogs combat, grants 4 life, and puts +1/+1 on your creatures.",
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
