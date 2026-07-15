from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Temporal_Traveler.model import Temporal_Traveler
from pycards.sorcery.Mystic_Insight.model import Mystic_Insight

@bind_card(Temporal_Traveler)
class Temporal_Traveler_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Whenever [CARD_NAME] attacks, you may cast an instant or sorcery card from your graveyard without paying its mana cost.",

        "Each time [CARD_NAME] attacks, you may cast an instant or sorcery from your graveyard without paying its mana cost.",

        "When [CARD_NAME] attacks, you may cast an instant or sorcery card from your graveyard for free.",

        "Whenever [CARD_NAME] attacks, you may cast an instant or sorcery from your graveyard without paying mana.",

        "On attack, [CARD_NAME] lets you cast an instant or sorcery from your graveyard without paying its mana cost.",

        "Whenever [CARD_NAME] attacks, you may play an instant or sorcery from your graveyard without paying its mana cost.",

        "Whenever [CARD_NAME] attacks, you may cast an instant or sorcery spell from your graveyard without paying its mana cost.",

        "Whenever [CARD_NAME] attacks, you may cast an instant or sorcery card from your graveyard without paying mana.",

        "Whenever [CARD_NAME] attacks, you may cast an instant or sorcery from your graveyard without paying its mana cost.",

    ]
    @simulate
    def simulate_when_enter_battlefield(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U":(2,7)},
            least_mana={"colorless":3,"U":2}
        )

        simulate_info=self.room.simulate_play(self.card)
        return simulate_info

    @simulate
    def simulate_when_attack_opponent(self):
        self.basic_initinal()
        self.room.env_initinal_graveyard(self.player,{})
        self.player.graveyard.append(Mystic_Insight(self.player))
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.random_env_creature()(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U":(0,7),"B":(0,7),"G":(0,7),"R":(0,7),"W":(0,7)},
        )

        simulate_info=self.room.simulate_creature_attack(self.card)
        return simulate_info

    @simulate
    def simulate_when_defend_opponent(self):
        self.basic_initinal()
        self.random_env_creature()(self.player)
        self.random_life()(self.player)
        self.room.env_creature(self.player.opponent)
        self.random_life()(self.player.opponent)

        self.room.env_mana(
            self.player,
            {"U":(0,7),"B":(0,7),"G":(0,7),"R":(0,7),"W":(0,7)},
        )

        simulate_info=self.room.simulate_creature_defend(self.card)
        return simulate_info
