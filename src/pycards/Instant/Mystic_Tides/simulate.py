from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Mystic_Tides.model import Mystic_Tides

@bind_card(Mystic_Tides)
class Mystic_Tides_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Counter target spell unless its controller's mana pool is less than 2. If it is countered this way, tap random opponent's creature.",
        "[CARD_NAME] counters unless controller has less than 2 mana; tap random opponent creature if countered.",
        "Counter unless mana pool <2. If countered, tap random opponent creature.",
        "With [CARD_NAME], counter unless 2 mana available; tap random enemy creature on counter.",
        "Counter target spell unless controller's mana is below 2. Tap random opponent creature if countered.",
        "[CARD_NAME]: counter unless mana <2; tap random opponent creature when countered.",
        "Unless controller has 2+ mana, counter target spell. On counter, tap random opponent creature.",
        "Counter unless mana pool less than 2. Successful counter taps random opponent creature.",
        "[CARD_NAME] counters unless 2 mana; taps random opponent creature if countered this way.",
        "Counter unless controller's mana pool is under 2. Tap random opponent creature if countered.",
    ]

    @simulate
    def simulate_card_stack(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.room.env_creature(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U":(1,7)},
            least_mana={"colorless":1,"U":1}
        )

        self.room.env_stack_cards(self.player,self.card)
        simulate_info=self.room.simulate_play_in_stack(self.card)
        return simulate_info
