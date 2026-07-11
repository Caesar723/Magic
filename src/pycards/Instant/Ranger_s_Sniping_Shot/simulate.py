from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Ranger_s_Sniping_Shot.model import Ranger_s_Sniping_Shot

@bind_card(Ranger_s_Sniping_Shot)
class Ranger_s_Sniping_Shot_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Counter target spell. If that spell is a creature spell, deal damage to its controller equal to that creature's power.",
        "[CARD_NAME] counters target spell; if it's a creature spell, deal damage equal to power to controller.",
        "Counter a spell. Creature spells deal damage equal to power to controller.",
        "With [CARD_NAME], counter target spell and snipe controller for creature power if creature spell.",
        "Counter target spell. On creature spell, damage controller equal to creature power.",
        "[CARD_NAME]: counter spell; damage controller equal to creature power if creature spell.",
        "Counter a spell. If creature spell, controller takes damage equal to creature's power.",
        "Counter target spell. Creature spell controllers take damage equal to power.",
        "[CARD_NAME] counters and punishes creature spell controllers with damage equal to power.",
        "Counter spell; if creature, deal damage to controller equal to its power.",
    ]

    @simulate
    def simulate_card_stack(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"G":(1,7)},
            least_mana={"colorless":1,"G":1}
        )

        self.room.env_stack_cards(
            self.player,self.card,preferred_types=("creature",)
        )
        simulate_info=self.room.simulate_play_in_stack(self.card)
        return simulate_info
