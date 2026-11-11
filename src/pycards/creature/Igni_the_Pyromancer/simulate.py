from pycards.sorcery.Pocket_Discovery.model import Pocket_Discovery
from pycards.Instant.Arcane_Reflection.model import Arcane_Reflection
from pycards.Instant.Time_Reversal.model import Time_Reversal
from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Igni_the_Pyromancer.model import Igni_the_Pyromancer


@bind_card(Igni_the_Pyromancer)
class Igni_the_Pyromancer_Simulation(Card_Simulation):
    scenario_locks={
        '_set_grave':('self.graveyard', 'self.library'),
        '_spell_combat':(),
        '_spell_unblocked':(),
        '_grave_attack':(),
    }

    text_parts = {
        "damage.trigger": [
            "Whenever this creature deals damage to a player,",
            "When this creature damages a player,",
            "After this creature deals damage to a player,",
            "Each time this creature deals damage to a player,",
            "Whenever a player receives damage from this creature,",
            "When this creature inflicts damage on a player,",
            "For each damage event from this creature to a player,",
            "After a player is damaged by this creature,",
            "Whenever damage from this creature reaches a player,",
            "Each time a player is dealt damage by this creature,",
        ],
        "spell.effect": [
            "randomly resolve the ability of an available non-counter instant or sorcery from your graveyard without paying its cost. The card remains in your graveyard.",
            "choose a non-counter instant or sorcery in your graveyard at random and resolve the ability of it for free, if available. The card remains in your graveyard.",
            "directly resolve the ability of a random instant or sorcery from your graveyard, excluding counterspells, when possible. The card remains in your graveyard.",
            "randomly select an available graveyard instant or sorcery other than a counterspell and resolve the ability of it without mana. The card remains in your graveyard.",
            "resolve the ability of one random non-counter instant or sorcery from your graveyard for no mana cost, if one exists. The card remains in your graveyard.",
            "take a random eligible instant or sorcery in your graveyard and resolve the ability of it without paying, excluding counters. The card remains in your graveyard.",
            "if available, directly resolve the ability of one randomly chosen non-counter instant or sorcery in your graveyard. The card remains in your graveyard.",
            "randomly resolve the ability of one of your graveyard instants or sorceries that is not a counterspell, paying nothing. The card remains in your graveyard.",
            "resolve the ability of for free a randomly selected non-counter instant or sorcery from your graveyard, if possible. The card remains in your graveyard.",
            "choose and resolve the ability of one random available non-counter instant or sorcery from your graveyard without mana. The card remains in your graveyard.",
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

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('damage.trigger', 'spell.effect')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self._spell_combat(False, True, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('damage.trigger', 'spell.effect')})
    def simulate_attack_opponent_dies_self_survives_beyond_boundary(self):
        return self._spell_combat(False, True, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('damage.trigger', 'spell.effect')})
    def simulate_attack_both_survive(self):
        return self._spell_combat(False, False, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('damage.trigger', 'spell.effect')})
    def simulate_attack_both_survive_beyond_boundary(self):
        return self._spell_combat(False, False, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('damage.trigger', 'spell.effect')})
    def simulate_attack_opponent_survives_self_dies(self):
        return self._spell_combat(False, False, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('damage.trigger', 'spell.effect')})
    def simulate_attack_opponent_survives_self_dies_beyond_boundary(self):
        return self._spell_combat(False, False, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('damage.trigger', 'spell.effect')})
    def simulate_attack_both_die(self):
        return self._spell_combat(False, True, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('damage.trigger', 'spell.effect')})
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

    @simulate(evidence={'fields': ('attack', 'special_type'), 'text': ('damage.trigger', 'spell.effect')})
    def simulate_attack_empty_board(self):
        return self._spell_unblocked(False)

    @simulate(evidence={'fields': ('attack', 'special_type'), 'text': ('damage.trigger', 'spell.effect')})
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

    @simulate(evidence={'text': ('damage.trigger', 'spell.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_grave_none_blocked_False(self):
        return self._grave_attack('none', False)

    @simulate(evidence={'text': ('damage.trigger', 'spell.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_grave_none_blocked_True(self):
        return self._grave_attack('none', True)

    @simulate(evidence={'text': ('damage.trigger', 'spell.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_grave_creature_blocked_False(self):
        return self._grave_attack('creature', False)

    @simulate(evidence={'text': ('damage.trigger', 'spell.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_grave_creature_blocked_True(self):
        return self._grave_attack('creature', True)

    @simulate(evidence={'text': ('damage.trigger', 'spell.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_grave_counter_blocked_False(self):
        return self._grave_attack('counter', False)

    @simulate(evidence={'text': ('damage.trigger', 'spell.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_grave_counter_blocked_True(self):
        return self._grave_attack('counter', True)

    @simulate(evidence={'text': ('damage.trigger', 'spell.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_grave_instant_blocked_False(self):
        return self._grave_attack('instant', False)

    @simulate(evidence={'text': ('damage.trigger', 'spell.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_grave_instant_blocked_True(self):
        return self._grave_attack('instant', True)

    @simulate(evidence={'text': ('damage.trigger', 'spell.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_grave_sorcery_blocked_False(self):
        return self._grave_attack('sorcery', False)

    @simulate(evidence={'text': ('damage.trigger', 'spell.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_grave_sorcery_blocked_True(self):
        return self._grave_attack('sorcery', True)

    @simulate(evidence={'text': ('damage.trigger', 'spell.effect'), 'fields': ('attack', 'special_type')})
    def simulate_spell_library_0(self):
        return self._grave_attack("sorcery", library_count=0)

    @simulate(evidence={'text': ('damage.trigger', 'spell.effect'), 'fields': ('attack', 'special_type')})
    def simulate_spell_library_1(self):
        return self._grave_attack("sorcery", library_count=1)

    @simulate(evidence={'text': ('damage.trigger', 'spell.effect'), 'fields': ('attack', 'special_type')})
    def simulate_spell_library_5(self):
        return self._grave_attack("sorcery", library_count=5)

