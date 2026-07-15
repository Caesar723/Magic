from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.rlearning.trainingRoom.training_parallel_specific_room import Multi_Agent_Parallel_Specific_Room
    from game.player import Player

from game.card_simulation import bind_card,simulate,Card_Simulation,test
from pycards.creature.Igni_the_Pyromancer.model import Igni_the_Pyromancer
from pycards.sorcery.Mystic_Insight.model import Mystic_Insight

@bind_card(Igni_the_Pyromancer)
class Igni_the_Pyromancer_Simulation(Card_Simulation):

    similar_descriptions:list[str]=[
        "Whenever [CARD_NAME] deals damage to a player, you randomly cast an instant or sorcery spell from your graveyard without paying its mana cost.",

        "Each time [CARD_NAME] deals damage to a player, you randomly cast an instant or sorcery from your graveyard without paying its mana cost.",

        "When [CARD_NAME] deals damage to a player, you randomly cast an instant or sorcery spell from your graveyard for free.",

        "Whenever [CARD_NAME] damages a player, you randomly cast an instant or sorcery from your graveyard without paying mana.",

        "On dealing damage to a player, [CARD_NAME] lets you randomly cast an instant or sorcery from your graveyard without paying its mana cost.",

        "Whenever [CARD_NAME] deals damage to a player, randomly cast an instant or sorcery spell from your graveyard without paying its mana cost.",

        "Whenever [CARD_NAME] deals damage to a player, you cast a random instant or sorcery from your graveyard without paying its mana cost.",

        "Whenever [CARD_NAME] deals damage to a player, you randomly play an instant or sorcery from your graveyard without paying its mana cost.",

        "Whenever [CARD_NAME] deals damage to a player, you randomly cast an instant or sorcery card from your graveyard without paying its mana cost.",

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
            {"R":(1,7)},
            least_mana={"colorless":2,"R":1}
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
        # With no blocker, combat damage reaches the player and exercises the
        # graveyard-cast branch in when_harm_is_done.
        self.room.env_no_creature(self.player.opponent)
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
