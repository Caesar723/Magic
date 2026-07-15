from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.land.Nexus_of_the_Eternal_Seas.model import Nexus_of_the_Eternal_Seas

@bind_card(Nexus_of_the_Eternal_Seas)
class Nexus_of_the_Eternal_Seas_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] enters the battlefield tapped and adds one blue mana to your mana pool. You may tap [CARD_NAME] to return random opponent's creature to its owner's hand.",

        "[CARD_NAME] enters the battlefield tapped and adds one blue mana to your mana pool. You may tap [CARD_NAME] to return a random creature controlled by an opponent to its owner's hand.",

        "When [CARD_NAME] enters the battlefield, it enters tapped and adds one blue mana to your mana pool. You may tap [CARD_NAME] to return a random opponent's creature to its owner's hand.",

        "[CARD_NAME] enters tapped and adds one blue mana to your mana pool. You may tap [CARD_NAME] to return a random creature an opponent controls to its owner's hand.",

        "[CARD_NAME] enters the battlefield tapped and produces one blue mana. You may tap [CARD_NAME] to return a random opponent's creature to its owner's hand.",

        "[CARD_NAME] enters the battlefield tapped and adds one blue mana to your mana pool. You may tap [CARD_NAME] to bounce a random opponent's creature to its owner's hand.",

        "[CARD_NAME] enters tapped and adds one blue mana to your mana pool. You may tap [CARD_NAME] to return a random opponent creature to its owner's hand.",

        "[CARD_NAME] enters the battlefield tapped and adds one blue mana to your mana pool. You may tap [CARD_NAME] to return a random creature controlled by your opponent to its owner's hand.",

        "When [CARD_NAME] enters the battlefield tapped, add one blue mana to your mana pool. You may tap [CARD_NAME] to return a random opponent's creature to its owner's hand.",

        "[CARD_NAME] enters the battlefield tapped and adds one blue mana to your mana pool. You may tap [CARD_NAME] to return a random opponent's creature back to its owner's hand.",
    ]

    @simulate
    def simulate_with_opponent_creature(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        # Guarantee a legal object for the random bounce mode.
        self.room.env_creature(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U": (0, 3), "B": (0, 3), "G": (0, 3), "R": (0, 3), "W": (0, 3)},
        )

        return self.room.simulate_play(self.card)

    @simulate
    def simulate_activate_ability(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        # Guarantee a bounce target for the manual branch.
        self.room.env_creature(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U": (0, 3), "B": (0, 3), "G": (0, 3), "R": (0, 3), "W": (0, 3)},
        )

        return self.room.simulate_activate_ability(self.card)
