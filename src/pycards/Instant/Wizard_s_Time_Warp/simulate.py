from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Wizard_s_Time_Warp.model import Wizard_s_Time_Warp

@bind_card(Wizard_s_Time_Warp)
class Wizard_s_Time_Warp_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Counter target spell. Its controller discards a card.",
        "[CARD_NAME] counters target spell and makes its controller discard a card.",
        "Counter a spell. Controller discards a card.",
        "With [CARD_NAME], counter target spell; controller discards.",
        "Counter target spell. Its controller discards one card.",
        "[CARD_NAME]: counter spell; controller discards.",
        "Counter a spell. Force controller to discard.",
        "Counter target spell. Spell controller discards a card.",
        "[CARD_NAME] counters and forces a discard from the spell's controller.",
        "Counter spell; controller discards a card.",
    ]

    @simulate
    def simulate_card_stack(self):
        self.basic_initinal()
        self.room.env_initinal_hand(
            self.player.opponent,
            {"creature_number":(1,2),"land_number":(1,2)},
        )
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U":(1,7)},
            least_mana={"colorless":3,"U":1}
        )

        self.room.env_stack_cards(self.player,self.card)
        simulate_info=self.room.simulate_play_in_stack(self.card)
        return simulate_info
