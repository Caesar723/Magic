from game.type_cards.land import Land
from pycards.land.Plains.model import Plains
from pycards.land.Forest.model import Forest
from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Thornroot_Druid.model import Thornroot_Druid


@bind_card(Thornroot_Druid)
class Thornroot_Druid_Simulation(Card_Simulation):
    scenario_locks={
        '_enter_library':('self.land_area', 'self.library'),
    }

    text_parts = {
        "enter.trigger": [
            "When {card_name} enters the battlefield,",
            "Whenever {card_name} enters the battlefield,",
            "When this creature enters the battlefield,",
            "Whenever this creature enters the battlefield,",
            "When {card_name} enters play,",
            "Whenever {card_name} enters play,",
            "When this creature enters play,",
            "Whenever this creature enters play,",
            "When {card_name} comes into play,",
            "Whenever {card_name} comes into play,",
        ],
        "enter.effect": [
            "Put a random basic land from your library into your hand, if one is available.",
            "If your library has a basic land, randomly choose one and put it into your hand.",
            "Choose a basic land from your library at random and put it into your hand, if possible.",
            "If available, move one random basic land from your library into your hand.",
            "Randomly select a basic land in your library and put it into your hand, when available.",
            "When your library contains a basic land, put one selected at random into your hand.",
            "Move a randomly chosen basic land from your library into your hand if any exist.",
            "Put one basic land chosen randomly from your library into your hand, if you have one.",
            "From your library, take a random basic land if present and put it into your hand.",
            "If any basic lands remain in your library, randomly choose one to enter your hand.",
        ],
        "library.shuffle": [
            "If a land was moved this way, then shuffle your library.",
            "If a land was moved this way, shuffle the remaining library afterward.",
            "If a land was moved this way, next, shuffle your remaining library.",
            "If a land was moved this way, afterward, shuffle the library.",
            "If a land was moved this way, finish by shuffling your library.",
            "If a land was moved this way, finally, randomize your library's order.",
            "If a land was moved this way, shuffle your library after this.",
            "If a land was moved this way, after moving the land, shuffle your library.",
            "If a land was moved this way, then randomize the order of your remaining library.",
            "If a land was moved this way, the remaining library is shuffled afterward.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_cast_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self.scenario_combat(False, True, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(False, True, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive(self):
        return self.scenario_combat(False, False, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive_beyond_boundary(self):
        return self.scenario_combat(False, False, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies(self):
        return self.scenario_combat(False, False, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(False, False, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die(self):
        return self.scenario_combat(False, True, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die_beyond_boundary(self):
        return self.scenario_combat(False, True, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_dies_self_survives(self):
        return self.scenario_combat(True, True, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(True, True, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_survive(self):
        return self.scenario_combat(True, False, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_survive_beyond_boundary(self):
        return self.scenario_combat(True, False, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_survives_self_dies(self):
        return self.scenario_combat(True, False, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(True, False, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_die(self):
        return self.scenario_combat(True, True, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_die_beyond_boundary(self):
        return self.scenario_combat(True, True, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'special_type')})
    def simulate_attack_empty_board(self):
        return self.scenario_unblocked(False)

    @simulate(evidence={'fields': ('attack', 'special_type')})
    def simulate_attack_opponent_passes(self):
        return self.scenario_unblocked(True)

    def _enter_library(self, basics, forests=0, nonbasic=False, only_lands=False):
        self.scenario_prepare()
        if only_lands:
            self.player.library.clear()
        else:
            self.player.library = [card for card in self.player.library if card.type != "Land"][:3]
        for _ in range(basics):
            self.player.library.append(Plains(self.player))
        for _ in range(forests):
            self.player.library.append(Forest(self.player))
        if nonbasic:
            land = self.scenario_cards(self.player,land=1,basic=False)[0]
            self.player.library.insert(0, land)
        self.player.mana.update(self.card.calculate_cost())
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_enter_library_none(self):
        return self._enter_library(0, 0, nonbasic=False)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_enter_library_plains_only(self):
        return self._enter_library(1, 0, nonbasic=False)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_enter_library_forest_only(self):
        return self._enter_library(0, 1, nonbasic=False)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_enter_library_many(self):
        return self._enter_library(3, 2, nonbasic=False)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_enter_library_nonbasic_only(self):
        return self._enter_library(0, 0, nonbasic=True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_enter_library_mixed_nonbasic(self):
        return self._enter_library(1, 2, nonbasic=True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_enter_empty_library(self):
        return self._enter_library(0, only_lands=True)

