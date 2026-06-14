from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Demonic_Ascendance.model import Demonic_Ascendance

@bind_card(Demonic_Ascendance)
class Demonic_Ascendance_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Target opponent reveals their hand. You may choose a creature card from it and put it onto the battlefield under your control. That creature gains haste. Sacrifice it at the beginning of the next end step.",

        "[CARD_NAME] makes target opponent reveal their hand. You may put a creature card from it onto the battlefield under your control with haste. Sacrifice it at the beginning of the next end step.",

        "Target opponent reveals their hand. You may choose a creature card and put it onto the battlefield under your control with haste. Sacrifice it at the next end step.",

        "[CARD_NAME] causes target opponent to reveal their hand. You may steal a creature card from it, which gains haste. Sacrifice it at the beginning of the next end step.",

        "Target opponent reveals their hand. You may put a creature card from their hand onto the battlefield under your control. It gains haste. Sacrifice it at the beginning of the next end step.",

        "[CARD_NAME] lets target opponent reveal their hand. You may choose a creature card and put it onto the battlefield under your control with haste, then sacrifice it at the next end step.",

        "Make target opponent reveal their hand. You may put a creature card from it onto the battlefield under your control with haste. Sacrifice it at the beginning of the next end step.",

        "[CARD_NAME] has target opponent reveal their hand. You may put a creature card onto the battlefield under your control with haste. Sacrifice it at the beginning of the next end step.",

        "Target opponent reveals their hand. You may choose a creature card and put it into play under your control with haste. Sacrifice it at the beginning of the next end step.",

        "[CARD_NAME] makes an opponent reveal their hand. You may put a creature card from it onto the battlefield under your control with haste, sacrificing it at the beginning of the next end step."
    ]
