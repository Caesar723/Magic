from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.land.Verdant_Sanctuary.model import Verdant_Sanctuary

@bind_card(Verdant_Sanctuary)
class Verdant_Sanctuary_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] enters the battlefield tapped and adds one green mana to your mana pool. You may also tap [CARD_NAME] and deal 3 damage to yourself to search your library for a basic Forest card and put it onto the battlefield tapped.",

        "[CARD_NAME] enters the battlefield tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] and deal 3 damage to yourself to search your library for a basic Forest card and put it onto the battlefield tapped.",

        "When [CARD_NAME] enters the battlefield, it enters tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] and deal 3 damage to yourself to search your library for a basic Forest card and put it onto the battlefield tapped.",

        "[CARD_NAME] enters tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] and deal 3 damage to yourself to search your library for a basic Forest card and put it onto the battlefield tapped.",

        "[CARD_NAME] enters the battlefield tapped and produces one green mana. You may tap [CARD_NAME] and deal 3 damage to yourself to search your library for a basic Forest card and put it onto the battlefield tapped.",

        "[CARD_NAME] enters the battlefield tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] and take 3 damage to search your library for a basic Forest card and put it onto the battlefield tapped.",

        "[CARD_NAME] enters tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] and deal 3 damage to yourself to search your library for a basic Forest and put it onto the battlefield tapped.",

        "[CARD_NAME] enters the battlefield tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] and deal 3 damage to yourself to find a basic Forest in your library and put it onto the battlefield tapped.",

        "When [CARD_NAME] enters the battlefield tapped, add one green mana to your mana pool. You may tap [CARD_NAME] and deal 3 damage to yourself to search your library for a basic Forest card and put it onto the battlefield tapped.",

        "[CARD_NAME] enters the battlefield tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] and deal 3 damage to yourself to search your library for a basic Forest card and put that land onto the battlefield tapped.",
    ]

    @simulate
    def simulate_with_forest_and_life_to_pay(self):
        # The seeded basic lands provide a Forest, while high life makes the
        # self-damage mode usable without immediately putting the player at risk.
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.room.env_life_high(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U": (0, 3), "B": (0, 3), "G": (0, 3), "R": (0, 3), "W": (0, 3)},
        )

        return self.room.simulate_play(self.card)

    @simulate
    def simulate_activate_ability(self):
        # The library contains a basic Forest, and high life enables self-damage safely.
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.room.env_life_high(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U": (0, 3), "B": (0, 3), "G": (0, 3), "R": (0, 3), "W": (0, 3)},
        )

        return self.room.simulate_activate_ability(self.card)
