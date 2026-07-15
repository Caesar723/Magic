from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.land.Mystic_Reflection_Pool.model import Mystic_Reflection_Pool

@bind_card(Mystic_Reflection_Pool)
class Mystic_Reflection_Pool_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] enters the battlefield untapped and adds one blue mana to your mana pool. Additionally, you may tap [CARD_NAME] and pay 1 mana to scry 2, then draw a card.",

        "[CARD_NAME] enters the battlefield untapped and adds one blue mana to your mana pool. You may tap [CARD_NAME] and pay 1 mana to scry 2, then draw a card.",

        "When [CARD_NAME] enters the battlefield, it enters untapped and adds one blue mana to your mana pool. You may tap [CARD_NAME] and pay 1 mana to scry 2, then draw a card.",

        "[CARD_NAME] enters untapped and adds one blue mana to your mana pool. You may tap [CARD_NAME] and pay 1 mana to scry 2, then draw a card.",

        "[CARD_NAME] enters the battlefield untapped and produces one blue mana. You may tap [CARD_NAME] and pay 1 mana to scry 2, then draw a card.",

        "[CARD_NAME] enters the battlefield untapped and adds one blue mana to your mana pool. You may tap [CARD_NAME] and pay 1 mana to scry 2 and draw a card.",

        "[CARD_NAME] enters untapped and adds one blue mana to your mana pool. You may tap [CARD_NAME] and pay 1 mana to scry two, then draw a card.",

        "[CARD_NAME] enters the battlefield untapped and adds one blue mana to your mana pool. You may tap [CARD_NAME] and pay 1 mana to look at the top two cards of your library, then draw a card.",

        "When [CARD_NAME] enters the battlefield untapped, add one blue mana to your mana pool. You may tap [CARD_NAME] and pay 1 mana to scry 2, then draw a card.",

        "[CARD_NAME] enters the battlefield untapped and adds one blue mana to your mana pool. You may tap [CARD_NAME] and pay 1 mana to scry 2, then draw one card.",
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

        # Keep the advertised one-mana activated mode payable.
        self.room.env_mana(
            self.player,
            {"U": (0, 3), "B": (0, 3), "G": (0, 3), "R": (0, 3), "W": (0, 3)},
            least_mana={"colorless": 1},
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

        # The manual scry-and-draw branch costs one generic mana.
        self.room.env_mana(
            self.player,
            {"colorless": (1, 1), "U": (0, 3), "B": (0, 3), "G": (0, 3), "R": (0, 3), "W": (0, 3)},
        )

        return self.room.simulate_activate_ability(self.card)
