from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Mage_s_Veto.model import Mage_s_Veto

@bind_card(Mage_s_Veto)
class Mage_s_Veto_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Counter target spell. If that spell's mana cost is less than 3, search your library for a Sorcery card and put it into your hand.",
        "[CARD_NAME] counters target spell; if mana cost under 3, tutor a Sorcery to hand.",
        "Counter a spell. If its mana cost is less than 3, search for a Sorcery and put it in your hand.",
        "With [CARD_NAME], counter target spell and tutor a Sorcery if the spell cost less than 3.",
        "Counter target spell. Cheap spells (cost <3) let you search for a Sorcery.",
        "[CARD_NAME]: counter spell; fetch Sorcery if countered spell cost less than 3.",
        "Counter target spell. When mana cost is under 3, find a Sorcery in your library.",
        "Counter a spell. If cost less than 3, search library for Sorcery to hand.",
        "[CARD_NAME] counters and may tutor a Sorcery when the spell's mana cost is less than 3.",
        "Counter target spell. Mana cost below 3 triggers a Sorcery search.",
    ]

    @simulate
    def simulate_card_stack(self):
        self.basic_initinal()
        self.room.env_initinal_library(self.player,{"sorcery_number":(1,10)})
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U":(1,7)},
            least_mana={"colorless":1,"U":1}
        )

        self.room.env_stack_cards(self.player,self.card,max_mana_value=2)
        simulate_info=self.room.simulate_play_in_stack(self.card)
        return simulate_info
