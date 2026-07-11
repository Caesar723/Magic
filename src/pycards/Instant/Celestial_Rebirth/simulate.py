from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Celestial_Rebirth.model import Celestial_Rebirth

@bind_card(Celestial_Rebirth)
class Celestial_Rebirth_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Return a creature card from your graveyard to the battlefield. It gains indestructible until end of turn. Exile [CARD_NAME].",
        "[CARD_NAME] returns a creature from your graveyard to the battlefield with indestructible until end of turn, then exiles itself.",
        "Put a creature card from your graveyard onto the battlefield. It has indestructible this turn. Exile [CARD_NAME].",
        "Reanimate a creature from your graveyard with indestructible until end of turn. Exile [CARD_NAME] as it resolves.",
        "Return one creature from graveyard to battlefield; it gains indestructible until end of turn. Exile [CARD_NAME].",
        "[CARD_NAME] brings back a creature with indestructible this turn, then exiles itself.",
        "Return a creature card from graveyard to battlefield with indestructible until end of turn. Exile this spell.",
        "Bring a creature from your graveyard back with indestructible until end of turn. Exile [CARD_NAME].",
        "Return a creature from graveyard to play; indestructible until end of turn. Exile [CARD_NAME].",
        "[CARD_NAME]: reanimate a creature with indestructible this turn, then exile itself.",
    ]

    @simulate
    def simulate_card(self):
        self.basic_initinal()
        self.room.env_initinal_graveyard(
            self.player,
            {"creature_number":(1,10)},
        )
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"W":(3,7)},
            least_mana={"colorless":1,"W":3}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
