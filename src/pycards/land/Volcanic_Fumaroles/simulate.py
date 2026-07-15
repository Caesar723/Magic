from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.land.Volcanic_Fumaroles.model import Volcanic_Fumaroles

@test
@bind_card(Volcanic_Fumaroles)
class Volcanic_Fumaroles_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] enters the battlefield tapped and adds one red mana to your mana pool. You mayp pay 1 mana to tap [CARD_NAME] and deal 1 damage to random opponent's creature or player.",

        "[CARD_NAME] enters the battlefield tapped and adds one red mana to your mana pool. You may pay 1 mana to tap [CARD_NAME] and deal 1 damage to a random opponent's creature or player.",

        "When [CARD_NAME] enters the battlefield, it enters tapped and adds one red mana to your mana pool. You may pay 1 mana to tap [CARD_NAME] and deal 1 damage to a random opponent's creature or player.",

        "[CARD_NAME] enters tapped and adds one red mana to your mana pool. You may pay 1 mana to tap [CARD_NAME] and deal 1 damage to a random creature or player controlled by an opponent.",

        "[CARD_NAME] enters the battlefield tapped and produces one red mana. You may pay 1 mana to tap [CARD_NAME] and deal 1 damage to a random opponent's creature or player.",

        "[CARD_NAME] enters the battlefield tapped and adds one red mana to your mana pool. You may pay 1 mana to tap [CARD_NAME] and deal 1 damage to a random opponent creature or the opponent.",

        "[CARD_NAME] enters tapped and adds one red mana to your mana pool. You may pay 1 mana to tap [CARD_NAME] and deal 1 damage to a random target among an opponent's creatures and that opponent.",

        "[CARD_NAME] enters the battlefield tapped and adds one red mana to your mana pool. You may pay 1 mana to tap [CARD_NAME] and deal 1 damage to a random creature or player an opponent controls.",

        "When [CARD_NAME] enters the battlefield tapped, add one red mana to your mana pool. You may pay 1 mana to tap [CARD_NAME] and deal 1 damage to a random opponent's creature or player.",

        "[CARD_NAME] enters the battlefield tapped and adds one red mana to your mana pool. You may pay 1 mana to tap [CARD_NAME] and deal 1 damage to a random opponent's creature or to the opponent.",
    ]

    @simulate
    def simulate_with_damage_cost_and_target(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.room.env_creature(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U": (0, 3), "B": (0, 3), "G": (0, 3), "R": (0, 3), "W": (0, 3)},
            least_mana={"colorless": 1},
        )

        return self.room.simulate_play(self.card)

    @simulate
    def simulate_activate_ability(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        # Guarantee a creature target in addition to the opposing player.
        self.room.env_creature(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"colorless": (1, 1), "U": (0, 3), "B": (0, 3), "G": (0, 3), "R": (0, 3), "W": (0, 3)},
        )

        return self.room.simulate_activate_ability(self.card)
