from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Divine_Rebirth.model import Divine_Rebirth

@bind_card(Divine_Rebirth)
class Divine_Rebirth_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Return target creature card from your graveyard to the battlefield. If it's an Angel, create two 4/4 white Angel creature tokens with flying tapped and attacking.",

        "[CARD_NAME] returns target creature card from your graveyard to the battlefield. If it's an Angel, create two 4/4 white Angel creature tokens with flying tapped and attacking.",

        "Return a target creature card from your graveyard to the battlefield. If that creature is an Angel, create two 4/4 white Angel tokens with flying that are tapped and attacking.",

        "[CARD_NAME] brings target creature card from your graveyard to the battlefield. If it's an Angel, create two 4/4 white flying Angel tokens tapped and attacking.",

        "Put target creature card from your graveyard onto the battlefield. If it's an Angel, create two 4/4 white Angel creature tokens with flying, tapped and attacking.",

        "[CARD_NAME] returns target creature from your graveyard to the battlefield. If it's an Angel, create two 4/4 white Angel tokens with flying that are tapped and attacking.",

        "Return target creature card from your graveyard to play. If it's an Angel, create two 4/4 white Angel creature tokens with flying, tapped and attacking.",

        "[CARD_NAME] puts target creature card from your graveyard onto the battlefield. If it's an Angel, create two 4/4 white flying Angel tokens tapped and attacking.",

        "Return a creature card from your graveyard to the battlefield. If it's an Angel, create two 4/4 white Angel creature tokens with flying that are tapped and attacking.",

        "[CARD_NAME] returns target creature card from your graveyard to the battlefield. If the returned card is an Angel, create two 4/4 white Angel tokens with flying, tapped and attacking."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.room.env_initinal_graveyard(self.player, {"creature_number": (2, 5)})
        self.room.env_no_creature(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"W": (1, 7)},
            least_mana={"colorless": 3, "W": 1},
        )

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
