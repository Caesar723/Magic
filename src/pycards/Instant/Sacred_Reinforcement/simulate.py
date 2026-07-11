from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Sacred_Reinforcement.model import Sacred_Reinforcement

@bind_card(Sacred_Reinforcement)
class Sacred_Reinforcement_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Tap up to two target creatures. They gain +1/+1 until end of turn.",
        "[CARD_NAME] taps up to two creatures and gives them +1/+1 until end of turn.",
        "Tap up to two creatures. They get +1/+1 this turn.",
        "Choose up to two creatures. Tap them. +1/+1 until end of turn.",
        "[CARD_NAME]: tap up to two creatures, +1/+1 until end of turn.",
        "Tap as many as two target creatures. Buff them +1/+1 this turn.",
        "Up to two creatures are tapped and get +1/+1 until end of turn.",
        "With [CARD_NAME], tap up to two creatures and grant +1/+1.",
        "Tap up to two creatures; they gain +1/+1 until end of turn.",
        "[CARD_NAME] taps up to two targets and buffs them +1/+1.",
    ]

    @simulate
    def simulate_card(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.room.env_creature(self.player.opponent)
        if len(self.player.opponent.battlefield)==1:
            creature=self.player.opponent.battlefield[0]
            self.player.opponent.battlefield.append(type(creature)(self.player.opponent))
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"W":(1,7)},
            least_mana={"colorless":1,"W":1}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
