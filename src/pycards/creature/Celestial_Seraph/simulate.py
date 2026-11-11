from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Celestial_Seraph.model import Celestial_Seraph


@bind_card(Celestial_Seraph)
class Celestial_Seraph_Simulation(Card_Simulation):
    text_parts = {
        "keyword.flying": [
            "Flying.",
            "This creature has flying.",
            "{card_name} has flying.",
            "This creature has the flying ability.",
            "{card_name} has the flying ability.",
            "Flying (Only creatures with flying or reach can block this creature).",
            "This creature can be blocked only by creatures with flying or reach.",
            "Only creatures with flying or reach can block this creature.",
            "Creatures without flying or reach cannot block this creature.",
            "This creature has flying. Creatures without flying or reach cannot block it.",
        ],
        "keyword.lifelink": [
            "Lifelink.",
            "This creature has lifelink.",
            "{card_name} has lifelink.",
            "This creature has the lifelink ability.",
            "{card_name} has the lifelink ability.",
            "Lifelink (Damage dealt by this creature also causes you to gain that much life).",
            "Damage dealt by this creature also causes you to gain that much life.",
            "Damage dealt by {card_name} also causes you to gain that much life.",
            "This creature has lifelink, so its damage also causes you to gain that much life.",
            "{card_name} has lifelink, so its damage also causes you to gain that much life.",
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
            "exile one random opposing creature, if available, and store it for this creature's leave-battlefield effect.",
            "randomly exile an available opposing creature and remember it until this creature leaves play.",
            "choose an opposing creature at random to exile and store for this creature's departure effect.",
            "put one random opposing creature into exile, if present, and retain it in this creature's stored list.",
            "randomly exile a creature your opponent controls and store it for this creature's leave trigger.",
            "exile a randomly selected opposing creature, if possible, and remember that object for this creature's departure.",
            "take a random opposing creature into exile and add it to this creature's stored creatures.",
            "if any opposing creature exists, randomly exile one and store it until this creature leaves play.",
            "randomly select an available opposing creature to exile and keep in this creature's stored list.",
            "exile one opposing creature at random when available, retaining it for this creature's leave effect.",
        ],
        "leave.effect": [
            "When this creature leaves the battlefield, create fresh opposing battlefield copies of every stored creature, leaving their exiled originals in exile.",
            "On leaving play, this creature returns fresh copies of its stored creatures to the opposing battlefield while the originals remain exiled.",
            "When this creature leaves play, put fresh copies of all stored creatures onto your opponent's battlefield without removing the originals from exile.",
            "Its departure from the battlefield creates fresh copies of the stored creatures for your opponent, preserving the exiled originals.",
            "When this creature leaves the battlefield, your opponent gets fresh copies of all creatures it stored, with the originals still in exile.",
            "On this creature's departure, return fresh battlefield copies of its stored creatures to your opponent and retain the originals in exile.",
            "When this creature leaves play, copy all its stored creatures onto your opponent's battlefield while leaving the original cards exiled.",
            "Leaving the battlefield makes this creature create fresh copies of all stored creatures for your opponent without moving the originals from exile.",
            "When this creature departs, all stored creatures produce fresh copies on the opposing battlefield, and the original cards stay exiled.",
            "Upon leaving play, this creature returns fresh copies of every stored creature to your opponent's battlefield, retaining originals in exile.",
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

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_dies_self_survives(self):
        return self.scenario_combat(True, True, False, margin=0)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(True, True, False, margin=1)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_survive(self):
        return self.scenario_combat(True, False, False, margin=0)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_survive_beyond_boundary(self):
        return self.scenario_combat(True, False, False, margin=1)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_survives_self_dies(self):
        return self.scenario_combat(True, False, True, margin=0)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(True, False, True, margin=1)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_die(self):
        return self.scenario_combat(True, True, True, margin=0)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_die_beyond_boundary(self):
        return self.scenario_combat(True, True, True, margin=1)

    @simulate(evidence={'text': ('keyword.lifelink', 'attack.trigger', 'attack.effect'), 'fields': ('attack', 'special_type')})
    def simulate_attack_empty_board(self):
        return self.scenario_unblocked(False)

    @simulate(evidence={'text': ('keyword.lifelink', 'attack.trigger', 'attack.effect'), 'fields': ('attack', 'special_type')})
    def simulate_attack_opponent_passes(self):
        return self.scenario_unblocked(True)

    @simulate(evidence={'text': ('keyword.flying',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_block_flying_creature(self):
        return self.scenario_combat(True, False, False, enemy_flags={"flying": True})

    def _exile_combat(self, count, self_dies, offset):
        self.scenario_prepare()
        for index in range(count):
            self.scenario_creature(self.player.opponent, power=self.card.state[1] if self_dies else self.card.state[1] - 1, health=max(1, self.card.state[0] + offset + index), flags={"reach": True, "Hexproof": True})
        record = self.room.simulate_creature_attack(self.card)
        self.stage_card(self.card)
        self.scenario_block()
        return record

    def _stored_defense(self, enemy_dies, self_dies):
        record = self.scenario_combat(True, enemy_dies, self_dies)
        creature = self.scenario_creature(self.player.opponent, power=1, health=3, flags={})
        self.player.opponent.remove_card(creature, "battlefield")
        self.player.opponent.append_card(creature, "exile_area")
        creature.flag_dict["exile"] = True
        self.card.creature_store.append(creature)
        return record

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect', 'leave.effect', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_exile_count_1_self_dies_False_low(self):
        return self._exile_combat(1, False, -1)

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect', 'leave.effect', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_exile_count_1_self_dies_False_equal(self):
        return self._exile_combat(1, False, 0)

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect', 'leave.effect', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_exile_count_1_self_dies_False_high(self):
        return self._exile_combat(1, False, 1)

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect', 'leave.effect', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_exile_count_1_self_dies_True_low(self):
        return self._exile_combat(1, True, -1)

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect', 'leave.effect', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_exile_count_1_self_dies_True_equal(self):
        return self._exile_combat(1, True, 0)

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect', 'leave.effect', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_exile_count_1_self_dies_True_high(self):
        return self._exile_combat(1, True, 1)

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect', 'leave.effect', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_exile_count_3_self_dies_False_low(self):
        return self._exile_combat(3, False, -1)

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect', 'leave.effect', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_exile_count_3_self_dies_False_equal(self):
        return self._exile_combat(3, False, 0)

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect', 'leave.effect', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_exile_count_3_self_dies_False_high(self):
        return self._exile_combat(3, False, 1)

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect', 'leave.effect', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_exile_count_3_self_dies_True_low(self):
        return self._exile_combat(3, True, -1)

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect', 'leave.effect', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_exile_count_3_self_dies_True_equal(self):
        return self._exile_combat(3, True, 0)

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect', 'leave.effect', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_exile_count_3_self_dies_True_high(self):
        return self._exile_combat(3, True, 1)

    @simulate(evidence={'text': ('leave.effect', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_stored_defense_enemy_dies_False_self_dies_False(self):
        return self._stored_defense(False, False)

    @simulate(evidence={'text': ('leave.effect', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_stored_defense_enemy_dies_False_self_dies_True(self):
        return self._stored_defense(False, True)

    @simulate(evidence={'text': ('leave.effect', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_stored_defense_enemy_dies_True_self_dies_False(self):
        return self._stored_defense(True, False)

    @simulate(evidence={'text': ('leave.effect', 'keyword.lifelink'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_stored_defense_enemy_dies_True_self_dies_True(self):
        return self._stored_defense(True, True)

