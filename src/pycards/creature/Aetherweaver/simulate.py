from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Aetherweaver.model import Aetherweaver


@bind_card(Aetherweaver)
class Aetherweaver_Simulation(Card_Simulation):
    scenario_locks={
        '_simulate_library':('self.library',),
        'simulate_enter_empty_library':('self.library',),
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
        "enter.look": [
            "find the first {look_count} instant or sorcery cards in your library, or all such cards if there are fewer.",
            "find up to {look_count} instant or sorcery cards by scanning your library from the top.",
            "look through your library from the top and take the first {look_count} instant or sorcery cards available.",
            "consider the first {look_count} cards in your library that are instants or sorceries, taking fewer if necessary.",
            "identify up to {look_count} instants or sorceries in library order, starting at the top.",
            "look at the first {look_count} instant or sorcery cards found anywhere in your library, or fewer if necessary.",
            "scan your entire library from the top for up to {look_count} instant or sorcery cards.",
            "find up to {look_count} cards of type instant or sorcery in their current library order.",
            "examine the earliest {look_count} instant or sorcery cards in your library, or all of them if fewer exist.",
            "search from the top of your library for its first {look_count} instant or sorcery cards, stopping if none remain.",
        ],
        "enter.choose": [
            "If any are found, choose one and put it into your hand.",
            "If there is at least one, select one of those cards and add it to your hand.",
            "If that group is not empty, move one chosen card from it to your hand.",
            "If any such cards exist, put one of them into your hand.",
            "Choose one of those cards, if available, and move it into your hand.",
            "Put one selected card from that group into your hand if the group is nonempty.",
            "If any cards were found, take one of them into your hand.",
            "When that group contains a card, choose one to add to your hand.",
            "If possible, select one card from that group and place it in your hand.",
            "From those cards, put one into your hand whenever at least one is available.",
        ],
        "enter.rest": [
            "Put the other found cards on the bottom of your library in their existing relative order.",
            "Move the remaining cards from that group to the bottom of your library, preserving their order.",
            "Place the unchosen cards from that group on the bottom in their current order.",
            "Put the rest of that group on the bottom of your library without reordering them.",
            "Move the other examined cards to the bottom in the order in which they were found.",
            "Return the unchosen cards from that group to the bottom, maintaining their relative order.",
            "Place any remaining found cards at the bottom of your library in the same order.",
            "The remaining found cards go to the bottom of your library in their original relative order.",
            "Put all other cards from that group at the bottom, retaining their existing order.",
            "Move the cards not chosen from that group to the bottom in library order.",
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

    def _simulate_library(self, spell_count, leading_count=0):
        self.scenario_prepare({"library": {"instant_number": (spell_count, spell_count), "sorcery_number": (0, 0), "creature_number": (leading_count, leading_count), "land_number": (0, 0)}})
        spells = [card for card in self.player.library if card.type in ("Instant", "Sorcery")]
        others = [card for card in self.player.library if card.type not in ("Instant", "Sorcery")]
        self.player.library = others + spells
        return self.scenario_cast()

    @simulate(evidence={'text': ('enter.trigger', 'enter.look'), 'fields': ('mana_cost',)})
    def simulate_enter_no_spells(self):
        return self._simulate_library(0)

    @simulate(evidence={'text': ('enter.trigger', 'enter.look', 'enter.choose', 'enter.rest'), 'fields': ('mana_cost',)})
    def simulate_enter_one_spell(self):
        return self._simulate_library(1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.look', 'enter.choose', 'enter.rest'), 'fields': ('mana_cost',)})
    def simulate_enter_fewer_spells(self):
        return self._simulate_library(max(0, self.card.effect_params["look_count"] - 1))

    @simulate(evidence={'text': ('enter.trigger', 'enter.look', 'enter.choose', 'enter.rest'), 'fields': ('mana_cost',)})
    def simulate_enter_exact_spells(self):
        return self._simulate_library(self.card.effect_params["look_count"])

    @simulate(evidence={'text': ('enter.trigger', 'enter.look', 'enter.choose', 'enter.rest'), 'fields': ('mana_cost',)})
    def simulate_enter_more_spells(self):
        return self._simulate_library(self.card.effect_params["look_count"] + 2)

    @simulate(evidence={'text': ('enter.trigger', 'enter.look', 'enter.choose', 'enter.rest'), 'fields': ('mana_cost',)})
    def simulate_enter_spells_below_nonspells(self):
        return self._simulate_library(self.card.effect_params["look_count"] + 2, leading_count=3)

    @simulate(evidence={'text': ('enter.trigger', 'enter.look'), 'fields': ('mana_cost',)})
    def simulate_enter_empty_library(self):
        self.scenario_prepare()
        self.player.library.clear()
        return self.scenario_cast()

