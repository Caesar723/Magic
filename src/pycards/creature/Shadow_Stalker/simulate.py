from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Shadow_Stalker.model import Shadow_Stalker


@bind_card(Shadow_Stalker)
class Shadow_Stalker_Simulation(Card_Simulation):
    text_parts = {
        "keyword.hexproof": [
            "Hexproof.",
            "This creature has hexproof.",
            "{card_name} has hexproof.",
            "This creature cannot be targeted by opposing spells or abilities.",
            "Opposing spells and abilities cannot target this creature.",
            "{card_name} cannot be targeted by spells or abilities from its opponent.",
            "This creature carries the hexproof keyword.",
            "Hexproof protects this creature from opposing targeting.",
            "The creature has the hexproof ability.",
            "{card_name} is protected by hexproof.",
        ],
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
        "attack.effect": [
            "randomly remove {discard_count} cards from your opponent's hand, or all available if fewer.",
            "take {discard_count} random opposing hand cards out of that hand, limited by availability.",
            "remove up to {discard_count} random cards from the opposing hand, taking all if fewer remain.",
            "randomly select and remove {discard_count} cards from your opponent's hand if available.",
            "remove random cards from the opposing hand {discard_count} times while any remain.",
            "choose {discard_count} opposing hand cards at random to remove, stopping if the hand empties.",
            "randomly take as many as {discard_count} available cards out of your opponent's hand.",
            "remove {discard_count} randomly chosen opposing hand cards, or all if fewer exist.",
            "take random cards out of the opposing hand until {discard_count} are removed or none remain.",
            "remove a random set of up to {discard_count} cards from your opponent's hand, taking all available if fewer.",
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

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'attack.effect')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self.scenario_combat(False, True, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'attack.effect')})
    def simulate_attack_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(False, True, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'attack.effect')})
    def simulate_attack_both_survive(self):
        return self.scenario_combat(False, False, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'attack.effect')})
    def simulate_attack_both_survive_beyond_boundary(self):
        return self.scenario_combat(False, False, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'attack.effect')})
    def simulate_attack_opponent_survives_self_dies(self):
        return self.scenario_combat(False, False, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'attack.effect')})
    def simulate_attack_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(False, False, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'attack.effect')})
    def simulate_attack_both_die(self):
        return self.scenario_combat(False, True, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'attack.effect')})
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

    @simulate(evidence={'fields': ('attack', 'special_type'), 'text': ('attack.trigger', 'attack.effect')})
    def simulate_attack_empty_board(self):
        return self.scenario_unblocked(False)

    @simulate(evidence={'fields': ('attack', 'special_type'), 'text': ('attack.trigger', 'attack.effect')})
    def simulate_attack_opponent_passes(self):
        return self.scenario_unblocked(True)

    def _hand_attack(self, count):
        record = self.scenario_unblocked()
        self.room.env_initinal_hand(self.player.opponent, {"instant_number": (count, count), "sorcery_number": (0, 0), "creature_number": (0, 0), "land_number": (0, 0)})
        self.player.opponent.hand = [card for card in self.player.opponent.hand if card.type == "Instant"][:count]
        return record

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect'), 'fields': ('attack', 'special_type')})
    def simulate_hand_empty(self):
        return self._hand_attack(0)

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect'), 'fields': ('attack', 'special_type')})
    def simulate_hand_one(self):
        return self._hand_attack(1)

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect'), 'fields': ('attack', 'special_type')})
    def simulate_hand_exact(self):
        return self._hand_attack(self.card.effect_params["discard_count"])

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect'), 'fields': ('attack', 'special_type')})
    def simulate_hand_plenty(self):
        return self._hand_attack(self.card.effect_params["discard_count"] + 2)

