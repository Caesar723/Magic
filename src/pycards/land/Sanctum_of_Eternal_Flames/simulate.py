from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.land.Sanctum_of_Eternal_Flames.model import Sanctum_of_Eternal_Flames

@bind_card(Sanctum_of_Eternal_Flames)
class Sanctum_of_Eternal_Flames_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] enters the battlefield tapped and adds one red mana to your mana pool. You may also tap [CARD_NAME] and pay 2 mana to deal 2 damage to random opponent's creature or player.",

        "[CARD_NAME] enters the battlefield tapped and adds one red mana to your mana pool. You may tap [CARD_NAME] and pay 2 mana to deal 2 damage to a random creature or player controlled by an opponent.",

        "When [CARD_NAME] enters the battlefield, it enters tapped and adds one red mana to your mana pool. You may tap [CARD_NAME] and pay 2 mana to deal 2 damage to a random opponent's creature or player.",

        "[CARD_NAME] enters tapped and adds one red mana to your mana pool. You may tap [CARD_NAME] and pay 2 mana to deal 2 damage to a random creature or player an opponent controls.",

        "[CARD_NAME] enters the battlefield tapped and produces one red mana. You may tap [CARD_NAME] and pay 2 mana to deal 2 damage to a random opponent's creature or player.",

        "[CARD_NAME] enters the battlefield tapped and adds one red mana to your mana pool. You may tap [CARD_NAME] and pay 2 mana to deal 2 damage to a random target among an opponent's creatures and that opponent.",

        "[CARD_NAME] enters tapped and adds one red mana to your mana pool. You may tap [CARD_NAME] and pay 2 mana to deal 2 damage to a random opponent creature or the opponent.",

        "[CARD_NAME] enters the battlefield tapped and adds one red mana to your mana pool. You may tap [CARD_NAME] and pay 2 mana to deal 2 damage to a random opponent's creature or to the opponent.",

        "When [CARD_NAME] enters the battlefield tapped, add one red mana to your mana pool. You may tap [CARD_NAME] and pay 2 mana to deal 2 damage to a random opponent's creature or player.",

        "[CARD_NAME] enters the battlefield tapped and adds one red mana to your mana pool. You may tap [CARD_NAME] and pay 2 mana to deal 2 damage to a random creature or player controlled by your opponent.",
    ]

    @simulate
    def simulate_with_damage_cost_and_target(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        # A creature makes the random target choice strategically distinct from face damage.
        self.room.env_creature(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U": (0, 3), "B": (0, 3), "G": (0, 3), "R": (0, 3), "W": (0, 3)},
            least_mana={"colorless": 2},
        )

        return self.room.simulate_play(self.card)
