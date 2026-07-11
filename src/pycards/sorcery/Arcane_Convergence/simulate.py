from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Arcane_Convergence.model import Arcane_Convergence

@bind_card(Arcane_Convergence)
class Arcane_Convergence_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] allows you to untap all lands you control and add X mana in any combination of colors to your mana pool, where X is the number of sorcery cards in your graveyard.",

        "Untap all lands you control. Add X mana in any combination of colors to your mana pool, where X is the number of sorcery cards in your graveyard.",

        "[CARD_NAME] untaps all your lands and adds X mana of any combination of colors, where X equals the number of sorcery cards in your graveyard.",

        "Untap all lands you control, then add X mana in any combination of colors, where X is the number of sorcery cards in your graveyard.",

        "[CARD_NAME] lets you untap all lands you control and add X mana in any colors, where X is the number of sorcery cards in your graveyard.",

        "Untap all lands you control. Add mana equal to the number of sorcery cards in your graveyard in any combination of colors.",

        "[CARD_NAME] untaps your lands and adds X mana in any combination of colors, where X is the count of sorcery cards in your graveyard.",

        "Untap all lands you control and add X mana in any combination of colors, where X is how many sorcery cards are in your graveyard.",

        "[CARD_NAME] allows you to untap all lands you control and add X mana of any colors, where X is the number of sorcery cards in your graveyard.",

        "Untap all lands you control. Add X mana in any combination of colors, where X is the number of sorcery cards in your graveyard."
    ]

    @simulate
    def simulate_when_cast(self):
        self.basic_initinal()
        self.room.env_initinal_graveyard(self.player, {"sorcery_number": (3, 6)})
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U": (6, 7)},
            least_mana={"colorless": 3, "U": 2},
        )

        if self.player.land_area:
            self.player.land_area[0].tap()

        simulate_info = self.room.simulate_play(self.card)
        return simulate_info
