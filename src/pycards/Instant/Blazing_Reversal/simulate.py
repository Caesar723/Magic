from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Blazing_Reversal.model import Blazing_Reversal

@bind_card(Blazing_Reversal)
class Blazing_Reversal_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Change the target of target spell or ability with a single target. You may choose new targets for the redirection. If [CARD_NAME] is in your graveyard, you may cast it by sacrificing a Mountain and paying its flashback cost. If you do, exile it as it resolves.",
        "[CARD_NAME] redirects a single-target spell or ability. You may choose new targets. Flashback by sacrificing a Mountain.",
        "Redirect target spell or ability with a single target. Choose new targets if you want. Cast from graveyard by sacrificing a Mountain.",
        "Change one target of a single-target spell or ability. Optionally pick new targets. [CARD_NAME] has flashback: sacrifice a Mountain.",
        "[CARD_NAME] lets you retarget a single-target spell or ability and may be cast from graveyard by sacrificing a Mountain.",
        "Retarget a spell or ability that has a single target. You may choose new targets. Flashback—sacrifice a Mountain.",
        "Change the target of a single-target spell or ability. New targets optional. [CARD_NAME] can be flashed back by sacrificing a Mountain.",
        "Redirect a single-target spell or ability and optionally choose new targets. From graveyard, cast by sacrificing a Mountain.",
        "[CARD_NAME]: redirect single-target spell or ability; flashback by sacrificing a Mountain, then exile on resolve.",
        "Alter the target of a single-target spell or ability. You may pick new targets. Sacrifice a Mountain to cast [CARD_NAME] from your graveyard.",
    ]

    @simulate
    def simulate_card(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U":(1,7),"R":(1,7)},
            least_mana={"colorless":1,"U":1,"R":1}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
