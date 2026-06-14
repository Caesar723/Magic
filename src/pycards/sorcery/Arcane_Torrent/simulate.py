from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.sorcery.Arcane_Torrent.model import Arcane_Torrent

@bind_card(Arcane_Torrent)
class Arcane_Torrent_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "[CARD_NAME] allows you to search your library for a random sorcery card, reveal it, and put it into your hand. Then shuffle your library.",

        "Search your library for a random sorcery card, reveal it, and put it into your hand. Then shuffle your library.",

        "[CARD_NAME] searches your library for a random sorcery card, reveals it, puts it into your hand, then shuffles.",

        "Find a random sorcery card in your library, reveal it, put it into your hand, then shuffle your library.",

        "[CARD_NAME] lets you search your library for a random sorcery, reveal it, add it to your hand, and shuffle.",

        "Search your library for a random sorcery card. Reveal it and put it into your hand. Shuffle your library.",

        "[CARD_NAME] finds a random sorcery in your library, reveals it, puts it into your hand, then shuffles your library.",

        "Search for a random sorcery card in your library, reveal it, put it into your hand, then shuffle.",

        "[CARD_NAME] allows you to search your library for a random sorcery card, reveal it, put it in your hand, and shuffle.",

        "Search your library for a random sorcery card, reveal it, put it into your hand, and shuffle your library."
    ]
