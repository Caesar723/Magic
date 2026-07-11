from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Mechanist_s_Disruption_Device.model import Mechanist_s_Disruption_Device

@bind_card(Mechanist_s_Disruption_Device)
class Mechanist_s_Disruption_Device_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Counter target spell. Then draw a card and you may put a land card from your hand onto the battlefield.",
        "[CARD_NAME] counters target spell, draws a card, and may put a land from hand onto the battlefield.",
        "Counter a spell, draw a card, and optionally play a land from your hand.",
        "With [CARD_NAME], counter target spell, then draw and optionally drop a land from hand.",
        "Counter target spell. Draw a card. You may put a land from hand onto the battlefield.",
        "[CARD_NAME]: counter, draw, optional land from hand to battlefield.",
        "Counter target spell, then draw and you may play a land from your hand.",
        "Counter a spell. Draw one. Optionally put a land from hand onto the battlefield.",
        "[CARD_NAME] counters, draws, and lets you put a land from hand into play.",
        "Counter target spell, draw, and may put a land card from hand onto the battlefield.",
    ]

    @simulate
    def simulate_card_stack(self):
        self.basic_initinal()
        self.room.env_initinal_hand(self.player,{"land_number":(1,2)})
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
