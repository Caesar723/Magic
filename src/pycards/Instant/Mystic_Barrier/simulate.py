from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Mystic_Barrier.model import Mystic_Barrier

@bind_card(Mystic_Barrier)
class Mystic_Barrier_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Target player can't cast noncreature spells until end of turn.",
        "[CARD_NAME] prevents target player from casting noncreature spells until end of turn.",
        "Choose a player. They can't cast noncreature spells this turn.",
        "Target player is locked out of noncreature spells until end of turn.",
        "[CARD_NAME]: target player can't cast noncreature spells this turn.",
        "Until end of turn, target player can't cast noncreature spells.",
        "Silence noncreature spells for target player until end of turn.",
        "With [CARD_NAME], stop a player from casting noncreature spells this turn.",
        "Target player cannot cast instants, sorceries, etc. until end of turn.",
        "[CARD_NAME] bars target player from noncreature spells until end of turn.",
    ]

    @simulate
    def simulate_card(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)
        # The implemented effect decorates cards already in the opponent's hand.
        self.room.env_initinal_hand(
            self.player.opponent,
            {"creature_number":(1,2),"instant_number":(1,3),"sorcery_number":(1,3),"land_number":(1,2)},
        )

        self.room.env_mana(
            self.player,
            {"W":(2,7)},
            least_mana={"colorless":1,"W":2}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
