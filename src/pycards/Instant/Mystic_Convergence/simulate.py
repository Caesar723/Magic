from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.Instant.Mystic_Convergence.model import Mystic_Convergence

@bind_card(Mystic_Convergence)
class Mystic_Convergence_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Prevent all combat damage that would be dealt this turn. At the beginning of your next main phase, add X mana in any combination of colors to your mana pool, where X is the amount of combat damage prevented this way.",
        "[CARD_NAME] prevents all combat damage this turn; next main phase add X mana of any colors, X = damage prevented.",
        "Prevent all combat damage this turn. Next main phase, add mana equal to damage prevented in any colors.",
        "With [CARD_NAME], stop all combat damage; gain mana next main phase equal to damage prevented.",
        "No combat damage this turn. Next main phase, add X mana (any colors), X = prevented combat damage.",
        "[CARD_NAME]: fog all combat damage; mana reward next main phase based on prevented damage.",
        "Prevent all combat damage. At your next main phase, add X mana in any combination, X = prevented damage.",
        "Combat damage is prevented this turn. Next main phase, gain mana equal to prevented damage.",
        "[CARD_NAME] fogs combat and converts prevented damage into mana next main phase.",
        "Prevent combat damage this turn; add X colored mana next main phase where X is damage prevented.",
    ]

    @simulate
    def simulate_card(self):
        self.basic_initinal()
        self.room.env_creature(self.player)
        self.random_life()(self.player)
        self.room.env_creature(self.player.opponent)
        self.room.attacker=self.player.opponent.battlefield[0]
        self.room.flag_dict["attacker_defenders"]=True
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"G":(1,7),"W":(1,7)},
            least_mana={"colorless":2,"G":1,"W":1}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info
