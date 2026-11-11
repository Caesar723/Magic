from pycards.sorcery.Pocket_Discovery.model import Pocket_Discovery
from pycards.Instant.Arcane_Reflection.model import Arcane_Reflection
from pycards.Instant.Time_Reversal.model import Time_Reversal
from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Temporal_Traveler.model import Temporal_Traveler


@bind_card(Temporal_Traveler)
class Temporal_Traveler_Simulation(Card_Simulation):
    scenario_locks={
        '_set_grave':('self.graveyard', 'self.library'),
        '_spell_combat':(),
        '_spell_unblocked':(),
        '_grave_attack':(),
    }

    text_parts = {
        "attack.trigger": [
            "Whenever this creature attacks,",
            "When this creature attacks,",
            "Each time this creature attacks,",
            "Whenever this creature starts attacking,",
            "When this creature begins an attack,",
            "As this creature attacks,",
            "When an attack by this creature begins,",
            "On each attack by this creature,",
            "Whenever this creature begins attacking,",
            "At the start of this creature's attack,",
        ],
        "spell.effect": [
            "randomly cast an available non-counter instant or sorcery from your graveyard without paying its cost.",
            "choose a non-counter instant or sorcery in your graveyard at random and cast it for free, if available.",
            "freely cast a random instant or sorcery from your graveyard, excluding counterspells, when possible.",
            "randomly select an available graveyard instant or sorcery other than a counterspell and cast it without mana.",
            "cast one random non-counter instant or sorcery from your graveyard for no mana cost, if one exists.",
            "take a random eligible instant or sorcery in your graveyard and cast it without paying, excluding counters.",
            "if available, freely cast one randomly chosen non-counter instant or sorcery in your graveyard.",
            "randomly cast one of your graveyard instants or sorceries that is not a counterspell, paying nothing.",
            "cast for free a randomly selected non-counter instant or sorcery from your graveyard, if possible.",
            "choose and cast one random available non-counter instant or sorcery from your graveyard without mana.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_when_cast(self):
        self.scenario_prepare()
        return self.scenario_cast()

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_cast_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'spell.effect')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self._spell_combat(False, True, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'spell.effect')})
    def simulate_attack_opponent_dies_self_survives_beyond_boundary(self):
        return self._spell_combat(False, True, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'spell.effect')})
    def simulate_attack_both_survive(self):
        return self._spell_combat(False, False, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'spell.effect')})
    def simulate_attack_both_survive_beyond_boundary(self):
        return self._spell_combat(False, False, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'spell.effect')})
    def simulate_attack_opponent_survives_self_dies(self):
        return self._spell_combat(False, False, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'spell.effect')})
    def simulate_attack_opponent_survives_self_dies_beyond_boundary(self):
        return self._spell_combat(False, False, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'spell.effect')})
    def simulate_attack_both_die(self):
        return self._spell_combat(False, True, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'spell.effect')})
    def simulate_attack_both_die_beyond_boundary(self):
        return self._spell_combat(False, True, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_dies_self_survives(self):
        return self._spell_combat(True, True, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_dies_self_survives_beyond_boundary(self):
        return self._spell_combat(True, True, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_survive(self):
        return self._spell_combat(True, False, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_survive_beyond_boundary(self):
        return self._spell_combat(True, False, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_survives_self_dies(self):
        return self._spell_combat(True, False, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_survives_self_dies_beyond_boundary(self):
        return self._spell_combat(True, False, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_die(self):
        return self._spell_combat(True, True, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_die_beyond_boundary(self):
        return self._spell_combat(True, True, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'special_type'), 'text': ('attack.trigger', 'spell.effect')})
    def simulate_attack_empty_board(self):
        return self._spell_unblocked(False)

    @simulate(evidence={'fields': ('attack', 'special_type'), 'text': ('attack.trigger', 'spell.effect')})
    def simulate_attack_opponent_passes(self):
        return self._spell_unblocked(True)

    def _set_grave(self, kind, library_count=None):
        library_count=self.scenario_count("library",library_count)
        self.player.graveyard.clear()
        if kind == "creature":
            card = self.scenario_creature(self.player, power=1, health=2, flags={}, zone="graveyard")
        elif kind != "none":
            cls = Pocket_Discovery if kind == "sorcery" else Arcane_Reflection if kind == "instant" else Time_Reversal
            self.stage_card(cls(self.player), self.player, zone="graveyard")
        if library_count is not None:
            self.scenario_replace_cards(self.player,"library",instant=(library_count, library_count))
            self.player.library = [card for card in self.player.library if card.type == "Instant"][:library_count]

    def _spell_combat(self, defending, enemy_dies, self_dies, margin=0):
        record = self.scenario_combat(defending, enemy_dies, self_dies, margin)
        self._set_grave("none")
        return record

    def _spell_unblocked(self, with_creature=False):
        record = self.scenario_unblocked(with_creature)
        self._set_grave("none")
        return record

    def _grave_attack(self, kind, blocked=False, library_count=None):
        library_count=self.scenario_count("library",library_count)
        record = self.scenario_combat(False, False, False) if blocked else self.scenario_unblocked()
        self._set_grave(kind, library_count)
        return record

    @simulate(evidence={'text': ('attack.trigger', 'spell.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_grave_none_blocked_False(self):
        return self._grave_attack('none', False)

    @simulate(evidence={'text': ('attack.trigger', 'spell.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_grave_none_blocked_True(self):
        return self._grave_attack('none', True)

    @simulate(evidence={'text': ('attack.trigger', 'spell.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_grave_creature_blocked_False(self):
        return self._grave_attack('creature', False)

    @simulate(evidence={'text': ('attack.trigger', 'spell.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_grave_creature_blocked_True(self):
        return self._grave_attack('creature', True)

    @simulate(evidence={'text': ('attack.trigger', 'spell.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_grave_counter_blocked_False(self):
        return self._grave_attack('counter', False)

    @simulate(evidence={'text': ('attack.trigger', 'spell.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_grave_counter_blocked_True(self):
        return self._grave_attack('counter', True)

    @simulate(evidence={'text': ('attack.trigger', 'spell.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_grave_instant_blocked_False(self):
        return self._grave_attack('instant', False)

    @simulate(evidence={'text': ('attack.trigger', 'spell.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_grave_instant_blocked_True(self):
        return self._grave_attack('instant', True)

    @simulate(evidence={'text': ('attack.trigger', 'spell.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_grave_sorcery_blocked_False(self):
        return self._grave_attack('sorcery', False)

    @simulate(evidence={'text': ('attack.trigger', 'spell.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_grave_sorcery_blocked_True(self):
        return self._grave_attack('sorcery', True)

    @simulate(evidence={'text': ('attack.trigger', 'spell.effect'), 'fields': ('attack', 'special_type')})
    def simulate_spell_library_0(self):
        return self._grave_attack("sorcery", library_count=0)

    @simulate(evidence={'text': ('attack.trigger', 'spell.effect'), 'fields': ('attack', 'special_type')})
    def simulate_spell_library_1(self):
        return self._grave_attack("sorcery", library_count=1)

    @simulate(evidence={'text': ('attack.trigger', 'spell.effect'), 'fields': ('attack', 'special_type')})
    def simulate_spell_library_5(self):
        return self._grave_attack("sorcery", library_count=5)

