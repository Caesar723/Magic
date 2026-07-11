from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Wild_Growth_Rush.model import Wild_Growth_Rush

@bind_card(Wild_Growth_Rush)
class Wild_Growth_Rush_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Target creature gains +2/+2 and trample until end of turn. Then, if you control a Forest, you may search your library for a basic land card and put it onto the battlefield tapped.",
        "[CARD_NAME] gives +2/+2 and trample; with a Forest, you may fetch a tapped basic land.",
        "Buff +2/+2 and trample. Forest lets you tutor tapped basic land.",
        "Target creature gets +2/+2 and trample. Forest: optional tapped land tutor.",
        "[CARD_NAME]: +2/+2 trample; Forest enables land tutor.",
        "+2/+2 and trample this turn. If you control Forest, fetch tapped basic land.",
        "Give +2/+2 and trample. With Forest, search for tapped basic land.",
        "With [CARD_NAME], +2/+2 trample buff and optional land ramp with Forest.",
        "Target creature +2/+2 trample. Forest control: tutor tapped basic land.",
        "[CARD_NAME] rushes a creature +2/+2 trample and may ramp with Forest.",
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
            {"G":(2,7)},
            least_mana={"colorless":1,"G":2}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
