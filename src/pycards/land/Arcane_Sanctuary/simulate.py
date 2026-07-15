from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.land.Arcane_Sanctuary.model import Arcane_Sanctuary

@bind_card(Arcane_Sanctuary)
class Arcane_Sanctuary_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] enters the battlefield tapped and adds one colorless mana to your mana pool. You may also tap [CARD_NAME] and pay 2 mana to scry 2 and draw a card.",

        "[CARD_NAME] enters the battlefield tapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] and pay 2 mana to scry 2, then draw a card.",

        "When [CARD_NAME] enters the battlefield, it enters tapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] and pay 2 mana to scry 2 and draw a card.",

        "[CARD_NAME] enters tapped and produces one colorless mana. You may tap [CARD_NAME] and pay 2 mana to scry 2 and draw a card.",

        "[CARD_NAME] enters the battlefield tapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] and pay 2 mana to look at the top two cards of your library, then draw a card.",

        "[CARD_NAME] enters the battlefield tapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] and pay 2 mana to scry 2, then draw one card.",

        "[CARD_NAME] enters tapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] and pay 2 mana to scry 2 and draw a card.",

        "[CARD_NAME] enters the battlefield tapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] and pay 2 mana to scry two, then draw a card.",

        "When [CARD_NAME] enters the battlefield tapped, add one colorless mana to your mana pool. You may tap [CARD_NAME] and pay 2 mana to scry 2 and draw a card.",

        "[CARD_NAME] enters the battlefield tapped and adds one colorless mana to your mana pool. You may tap [CARD_NAME] and pay 2 mana to scry 2 and draw one card.",
    ]

    @simulate
    def simulate_with_scry_cost(self):
        self.basic_initinal(
            {
                "graveyard": {"creature_number": (0, 4), "instant_number": (0, 4), "sorcery_number": (0, 4), "land_number": (0, 4)},
                "hand": {"creature_number": (0, 2), "instant_number": (0, 2), "sorcery_number": (0, 2), "land_number": (0, 2)},
                "library": {"creature_number": (2, 8), "instant_number": (2, 8), "sorcery_number": (2, 8), "land_number": (2, 8)},
            }
        )
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        # Leave at least two mana sources besides this land for its activated ability.
        self.room.env_mana(
            self.player,
            {"U": (0, 3), "B": (0, 3), "G": (0, 3), "R": (0, 3), "W": (0, 3)},
            least_mana={"colorless": 2},
        )

        return self.room.simulate_play(self.card)

    @simulate
    def simulate_activate_ability(self):
        self.basic_initinal(
            {
                "graveyard": {"creature_number": (0, 4), "instant_number": (0, 4), "sorcery_number": (0, 4), "land_number": (0, 4)},
                "hand": {"creature_number": (0, 2), "instant_number": (0, 2), "sorcery_number": (0, 2), "land_number": (0, 2)},
                "library": {"creature_number": (2, 8), "instant_number": (2, 8), "sorcery_number": (2, 8), "land_number": (2, 8)},
            }
        )
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        # Keep the two-mana manual branch payable after the land is staged for activation.
        self.room.env_mana(
            self.player,
            {"colorless": (2, 2), "U": (0, 3), "B": (0, 3), "G": (0, 3), "R": (0, 3), "W": (0, 3)},
        )

        return self.room.simulate_activate_ability(self.card)
