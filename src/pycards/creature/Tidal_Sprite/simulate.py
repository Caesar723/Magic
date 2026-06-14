from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Tidal_Sprite.model import Tidal_Sprite

@bind_card(Tidal_Sprite)
class Tidal_Sprite_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Flying (This creature can't be blocked except by creatures with flying or reach).",

        "Flying.",

        "Flying (can only be blocked by creatures with flying or reach).",

        "Flying (blocked only by flying or reach creatures).",

        "Flying (this can't be blocked except by creatures with flying or reach).",

        "Flying (only blockable by flying or reach).",

        "Flying (requires flying or reach to block).",

        "Flying (can't be blocked except by flying or reach creatures).",

        "Flying (blockable only by creatures with flying or reach).",

    ]
