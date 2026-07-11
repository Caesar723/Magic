from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Celestial_Renewal.model import Celestial_Renewal

@bind_card(Celestial_Renewal)
class Celestial_Renewal_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] allows you to return 3 random creature cards from your graveyard to the battlefield. Those creatures' stats become 1/1.",

        "Return 3 random creature cards from your graveyard to the battlefield. Those creatures become 1/1.",

        "[CARD_NAME] returns three random creature cards from your graveyard to the battlefield. Their power and toughness become 1/1.",

        "Put 3 random creature cards from your graveyard onto the battlefield. Those creatures' stats are set to 1/1.",

        "[CARD_NAME] brings back 3 random creature cards from your graveyard. Those creatures' stats become 1/1.",

        "Return three random creature cards from your graveyard to the battlefield. Each returned creature becomes 1/1.",

        "[CARD_NAME] returns 3 random creatures from your graveyard to the battlefield with power and toughness 1/1.",

        "Three random creature cards from your graveyard return to the battlefield. Those creatures' stats become 1/1.",

        "[CARD_NAME] puts 3 random creature cards from your graveyard onto the battlefield. Those creatures become 1/1.",

        "Return 3 random creature cards from your graveyard to the battlefield. Those creatures' power and toughness become 1/1."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.room.env_initinal_graveyard(self.player, {"creature_number": (3, 6)})
        self.room.env_no_creature(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"G": (1, 7), "W": (1, 7)},
            least_mana={"colorless": 2, "G": 1, "W": 1},
        )

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
