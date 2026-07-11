from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.land.Elysian_Grove.model import Elysian_Grove

@bind_card(Elysian_Grove)
class Elysian_Grove_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] enters the battlefield tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] to tap random opponent's land.",

        "[CARD_NAME] enters the battlefield tapped and produces one green mana. You may tap [CARD_NAME] to tap a random land controlled by an opponent.",

        "When [CARD_NAME] enters the battlefield, it enters tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] to tap a random opponent's land.",

        "[CARD_NAME] enters tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] to tap a random land an opponent controls.",

        "[CARD_NAME] enters the battlefield tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] to tap a random land belonging to an opponent.",

        "[CARD_NAME] enters the battlefield tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] to tap a random land on the opponent's side.",

        "[CARD_NAME] enters tapped and produces one green mana. You may tap [CARD_NAME] to tap a random opponent's land.",

        "[CARD_NAME] enters the battlefield tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] to tap a random land controlled by your opponent.",

        "When [CARD_NAME] enters the battlefield tapped, add one green mana to your mana pool. You may tap [CARD_NAME] to tap a random opponent's land.",

        "[CARD_NAME] enters the battlefield tapped and adds one green mana to your mana pool. You may tap [CARD_NAME] to tap a random land an opponent controls.",
    ]

    @simulate
    def simulate_with_opponent_land(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U": (0, 3), "B": (0, 3), "G": (0, 3), "R": (0, 3), "W": (0, 3)},
        )
        # The alternate tap mode needs at least one opposing land to select at random.
        self.room.env_mana(
            self.player.opponent,
            {"U": (0, 2), "B": (0, 2), "G": (1, 3), "R": (0, 2), "W": (0, 2)},
        )

        return self.room.simulate_play(self.card)
