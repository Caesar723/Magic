from game.type_cards.land import Land
from pycards.land.Plains.model import Plains
from pycards.land.Forest.model import Forest
from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Verdant_Titan.model import Verdant_Titan


@bind_card(Verdant_Titan)
class Verdant_Titan_Simulation(Card_Simulation):
    scenario_locks={
        '_enter_library':('self.land_area', 'self.library'),
    }

    text_parts = {
        "keyword.trample": [
            "Trample.",
            "This creature has trample.",
            "{card_name} has trample.",
            "This creature has the trample ability.",
            "{card_name} has the trample ability.",
            "Trample (This creature can deal excess combat damage to the defending player).",
            "This creature has trample and can deal excess combat damage to the defending player.",
            "{card_name} has trample and can deal excess combat damage to the defending player.",
            "This creature can deal excess combat damage to the defending player through trample.",
            "{card_name} can deal excess combat damage to the defending player through trample.",
        ],
        "keyword.vigilance": [
            "Vigilance.",
            "This creature has vigilance.",
            "{card_name} has vigilance.",
            "This creature has the vigilance ability.",
            "{card_name} has the vigilance ability.",
            "Attacking does not cause this creature to tap.",
            "This creature does not tap when it attacks.",
            "{card_name} does not tap when it attacks.",
            "Vigilance (Attacking does not cause this creature to tap).",
            "This creature has vigilance and does not tap when it attacks.",
        ],
        "land.trigger": [
            "Whenever this creature enters the battlefield or attacks,",
            "When this creature enters play or begins attacking,",
            "Each time this creature enters the battlefield or attacks,",
            "When this creature enters the battlefield, and whenever it attacks,",
            "On entering play or beginning an attack, this creature triggers the following ability.",
            "Whenever this creature enters play or starts an attack,",
            "This ability triggers when this creature enters the battlefield or attacks.",
            "Each entry to the battlefield and each attack by this creature triggers this.",
            "When this creature comes into play or attacks,",
            "Whenever this creature enters the battlefield or begins its attack,",
        ],
        "land.effect": [
            "Put a random basic land from your library onto your battlefield tapped, if one is available.",
            "If your library has a basic land, randomly choose one and put it onto your battlefield tapped.",
            "Choose a basic land from your library at random and put it into play tapped, if possible.",
            "If available, move one random basic land from your library onto your battlefield tapped.",
            "Randomly select a basic land in your library and put it onto your battlefield tapped, when available.",
            "When your library contains a basic land, put one selected at random into play tapped.",
            "Move a randomly chosen basic land from your library onto your battlefield tapped if any exist.",
            "Put one basic land chosen randomly from your library into play tapped, if you have one.",
            "From your library, take a random basic land if present and put it onto your battlefield tapped.",
            "If any basic lands remain in your library, randomly choose one to enter your battlefield tapped.",
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

    @simulate(evidence={'fields': ('mana_cost',), 'text': ('land.trigger', 'land.effect', 'library.shuffle')})
    def simulate_when_cast(self):
        self.scenario_prepare()
        return self.scenario_cast()

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_cast_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('keyword.trample', 'keyword.vigilance', 'land.trigger', 'land.effect', 'library.shuffle'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self.scenario_combat(False, True, False, margin=0)

    @simulate(evidence={'text': ('keyword.trample', 'keyword.vigilance', 'land.trigger', 'land.effect', 'library.shuffle'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(False, True, False, margin=1)

    @simulate(evidence={'text': ('keyword.trample', 'keyword.vigilance', 'land.trigger', 'land.effect', 'library.shuffle'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive(self):
        return self.scenario_combat(False, False, False, margin=0)

    @simulate(evidence={'text': ('keyword.trample', 'keyword.vigilance', 'land.trigger', 'land.effect', 'library.shuffle'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive_beyond_boundary(self):
        return self.scenario_combat(False, False, False, margin=1)

    @simulate(evidence={'text': ('keyword.trample', 'keyword.vigilance', 'land.trigger', 'land.effect', 'library.shuffle'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies(self):
        return self.scenario_combat(False, False, True, margin=0)

    @simulate(evidence={'text': ('keyword.trample', 'keyword.vigilance', 'land.trigger', 'land.effect', 'library.shuffle'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(False, False, True, margin=1)

    @simulate(evidence={'text': ('keyword.trample', 'keyword.vigilance', 'land.trigger', 'land.effect', 'library.shuffle'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die(self):
        return self.scenario_combat(False, True, True, margin=0)

    @simulate(evidence={'text': ('keyword.trample', 'keyword.vigilance', 'land.trigger', 'land.effect', 'library.shuffle'), 'fields': ('attack', 'defend', 'special_type')})
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

    @simulate(evidence={'text': ('keyword.vigilance', 'land.trigger', 'land.effect', 'library.shuffle'), 'fields': ('attack', 'special_type')})
    def simulate_attack_empty_board(self):
        return self.scenario_unblocked(False)

    @simulate(evidence={'text': ('keyword.vigilance', 'land.trigger', 'land.effect', 'library.shuffle'), 'fields': ('attack', 'special_type')})
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


    @simulate(evidence={'text': ('land.trigger', 'land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_enter_library_none(self):
        return self._enter_library(0, 0, nonbasic=False)


    @simulate(evidence={'text': ('land.trigger', 'land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_enter_library_plains_only(self):
        return self._enter_library(1, 0, nonbasic=False)


    @simulate(evidence={'text': ('land.trigger', 'land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_enter_library_forest_only(self):
        return self._enter_library(0, 1, nonbasic=False)


    @simulate(evidence={'text': ('land.trigger', 'land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_enter_library_many(self):
        return self._enter_library(3, 2, nonbasic=False)


    @simulate(evidence={'text': ('land.trigger', 'land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_enter_library_nonbasic_only(self):
        return self._enter_library(0, 0, nonbasic=True)


    @simulate(evidence={'text': ('land.trigger', 'land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_enter_library_mixed_nonbasic(self):
        return self._enter_library(1, 2, nonbasic=True)


    @simulate(evidence={'text': ('land.trigger', 'land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_enter_empty_library(self):
        return self._enter_library(0, only_lands=True)


