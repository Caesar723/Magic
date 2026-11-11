from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Alchemist_s_Chaotic_Blend.model import Alchemist_s_Chaotic_Blend


@bind_card(Alchemist_s_Chaotic_Blend)
class Alchemist_s_Chaotic_Blend_Simulation(Card_Simulation):
    text_parts = {
        "counter.effect": [
            "Counter the nonland spell on top of the stack.",
            "Counter the top spell on the stack if it is not a land.",
            "Remove the top nonland spell from the stack without resolving it.",
            "Counter the nonland spell currently on top of the stack.",
            "Stop the top nonland spell on the stack from resolving.",
            "Counter the spell at the top of the stack, excluding lands.",
            "Cancel the nonland spell at the top of the stack.",
            "Counter the topmost spell on the stack if it is not a land.",
            "Prevent the nonland spell on top of the stack from resolving.",
            "Counter the current top spell on the stack, provided it is not a land.",
        ],
        "spell.selection": [
            "Choose a random instant or sorcery from your library, excluding counterspell cards.",
            "Randomly select an instant or sorcery card in your library that is not a counterspell.",
            "Pick a random eligible instant or sorcery from your library, excluding counterspells.",
            "From the instants and sorceries in your library other than counterspells, choose one at random.",
            "Choose one card at random from your library's noncounter instants and sorceries.",
            "Randomly pick an instant or sorcery in your library, leaving counterspells ineligible.",
            "Choose a library instant or sorcery at random from those that are not counterspells.",
            "Pick a card at random from the noncounter instant and sorcery cards in your library.",
            "Randomly choose an instant or sorcery from your library except for counterspells.",
            "From your library, randomly select one instant or sorcery that is not a counterspell.",
        ],
        "spell.effect": [
            "If one is available, remove it from your library and prepare its effect with automatic target selection. If preparation succeeds, put its effect on the stack without paying mana.",
            "If such a card exists, take it out of your library and prepare its effect using automatically chosen targets, then put the prepared effect on the stack at no mana cost if successful.",
            "When a card is found, remove it from the library, automatically prepare its targets, and put its effect on the stack for free if preparation succeeds.",
            "If available, remove that card from your library and prepare its effect with automatic choices, adding the effect to the stack without mana payment if it can be prepared.",
            "If one exists, take it out of your library and prepare its effect automatically, placing the prepared effect on the stack for no mana when successful.",
            "When available, the selected card leaves your library and its effect is prepared with automatic targets, then added to the stack for free if preparation succeeds.",
            "If an eligible card exists, remove it from your library, prepare its effect with automatic selection, and put that effect on the stack without mana if successful.",
            "If a card was found, remove it from the library and automatically prepare its effect, adding that effect to the stack at no cost when preparation succeeds.",
            "For an available selection, remove it from your library and prepare its effect with automatic targets, then place that effect on the stack without paying mana if possible.",
            "If one is found, take it out of your library and automatically prepare its effect, which goes on the stack for free if preparation succeeds.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        self.scenario_stack()
        return self.scenario_cast(in_stack=True, provide_mana=False)

    def _library_spell_scene(self, kind, count, creature_targets=True):
        self.scenario_prepare({"library": {"instant_number": (count, count), "sorcery_number": (count, count), "creature_number": (count, count), "land_number": (count, count)}})
        self.player.library = [card for card in self.player.library if card.type == kind][:count]
        self.scenario_stack()
        self.room.env_mana(self.player.opponent, {"G": (1, 1)})
        if creature_targets:
            for owner in (self.player, self.player.opponent):
                self.scenario_creature(owner, flags={})
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'spell.selection', 'spell.effect'), 'fields': ('mana_cost',)})
    def simulate_instant_0_library_cards(self):
        return self._library_spell_scene('Instant', 0)

    @simulate(evidence={'text': ('counter.effect', 'spell.selection', 'spell.effect'), 'fields': ('mana_cost',)})
    def simulate_instant_1_library_cards(self):
        return self._library_spell_scene('Instant', 1)

    @simulate(evidence={'text': ('counter.effect', 'spell.selection', 'spell.effect'), 'fields': ('mana_cost',)})
    def simulate_instant_3_library_cards(self):
        return self._library_spell_scene('Instant', 3)

    @simulate(evidence={'text': ('counter.effect', 'spell.selection', 'spell.effect'), 'fields': ('mana_cost',)})
    def simulate_sorcery_0_library_cards(self):
        return self._library_spell_scene('Sorcery', 0)

    @simulate(evidence={'text': ('counter.effect', 'spell.selection', 'spell.effect'), 'fields': ('mana_cost',)})
    def simulate_sorcery_1_library_cards(self):
        return self._library_spell_scene('Sorcery', 1)

    @simulate(evidence={'text': ('counter.effect', 'spell.selection', 'spell.effect'), 'fields': ('mana_cost',)})
    def simulate_sorcery_3_library_cards(self):
        return self._library_spell_scene('Sorcery', 3)

    @simulate(evidence={'text': ('counter.effect', 'spell.selection', 'spell.effect'), 'fields': ('mana_cost',)})
    def simulate_creature_0_library_cards(self):
        return self._library_spell_scene('Creature', 0)

    @simulate(evidence={'text': ('counter.effect', 'spell.selection', 'spell.effect'), 'fields': ('mana_cost',)})
    def simulate_creature_1_library_cards(self):
        return self._library_spell_scene('Creature', 1)

    @simulate(evidence={'text': ('counter.effect', 'spell.selection', 'spell.effect'), 'fields': ('mana_cost',)})
    def simulate_creature_3_library_cards(self):
        return self._library_spell_scene('Creature', 3)

    @simulate(evidence={'text': ('counter.effect', 'spell.selection', 'spell.effect'), 'fields': ('mana_cost',)})
    def simulate_land_0_library_cards(self):
        return self._library_spell_scene('Land', 0)

    @simulate(evidence={'text': ('counter.effect', 'spell.selection', 'spell.effect'), 'fields': ('mana_cost',)})
    def simulate_land_1_library_cards(self):
        return self._library_spell_scene('Land', 1)

    @simulate(evidence={'text': ('counter.effect', 'spell.selection', 'spell.effect'), 'fields': ('mana_cost',)})
    def simulate_land_3_library_cards(self):
        return self._library_spell_scene('Land', 3)

    @simulate(evidence={'text': ('counter.effect', 'spell.selection', 'spell.effect'), 'fields': ('mana_cost',)})
    def simulate_without_creature_targets(self):
        return self._library_spell_scene("Instant", 3, False)

