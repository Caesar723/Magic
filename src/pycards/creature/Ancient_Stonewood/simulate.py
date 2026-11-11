from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Ancient_Stonewood.model import Ancient_Stonewood


@bind_card(Ancient_Stonewood)
class Ancient_Stonewood_Simulation(Card_Simulation):
    scenario_locks={
        '_reflect_combat':('opponent.battlefield', 'self.battlefield'),
        '_reflect_group':('opponent.battlefield', 'self.battlefield'),
    }

    text_parts = {
        "keyword.indestructible": [
            "Indestructible. Lethal damage is reduced to leave this creature at one health, and destruction attempts are ignored.",
            "This creature has indestructible, retaining one health from lethal damage and ignoring destruction attempts.",
            "Lethal damage leaves this indestructible creature at one health, and it ignores attempted destruction.",
            "This creature ignores destruction and reduces otherwise lethal damage to keep one health.",
            "Indestructible protects this creature from destruction, with lethal damage reduced to retain one health.",
            "Attempted destruction is ignored by this creature, and damage that would kill it leaves one health instead.",
            "This creature cannot be destroyed, and otherwise lethal damage is reduced so that one health remains.",
            "Destruction does nothing to this creature, and lethal damage is limited to leave it at one health.",
            "This creature has indestructible and keeps one health when damage would otherwise kill it.",
            "Indestructible makes this creature ignore destruction and reduce lethal damage to retain one health.",
        ],
        "hurt.trigger": [
            "Whenever this creature receives positive damage after damage reduction,",
            "When this creature takes a positive amount of damage after reduction,",
            "Each positive damage amount this creature actually receives triggers this ability.",
            "If this creature takes more than zero damage after damage reduction,",
            "Whenever a positive amount of damage reaches this creature,",
            "When damage greater than zero is received by this creature after reduction,",
            "After this creature takes positive damage that survives reduction,",
            "Whenever this creature is damaged for a positive amount after reductions,",
            "Each time this creature receives more than zero actual damage,",
            "When this creature takes positive damage after any reduction,",
        ],
        "hurt.effect": [
            "deal that much damage to a random opposing creature, if any are available.",
            "randomly choose an opposing creature and deal it the same damage, if possible.",
            "hit one random available opposing creature for the amount of damage this creature received.",
            "deal an equal amount of damage to a randomly selected opposing creature, if one exists.",
            "damage one random opposing creature by the amount this creature actually took, if available.",
            "choose an opposing creature at random to receive that same damage amount, if possible.",
            "randomly deal the received damage amount to one available opposing creature.",
            "if your opponent has any creatures, deal the same damage to one chosen at random.",
            "return that damage amount to a randomly chosen opposing creature, if available.",
            "deal damage equal to what this creature received to one random opposing creature, if present.",
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

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.indestructible', 'hurt.trigger', 'hurt.effect')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self._reflect_combat(False,True,margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.indestructible', 'hurt.trigger', 'hurt.effect')})
    def simulate_attack_opponent_dies_self_survives_beyond_boundary(self):
        return self._reflect_combat(False,True,margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.indestructible', 'hurt.trigger', 'hurt.effect')})
    def simulate_attack_both_survive(self):
        return self._reflect_combat(False,False,margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.indestructible', 'hurt.trigger', 'hurt.effect')})
    def simulate_attack_both_survive_beyond_boundary(self):
        return self._reflect_combat(False,False,margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.indestructible', 'hurt.trigger', 'hurt.effect')})
    def simulate_defend_opponent_dies_self_survives(self):
        return self._reflect_combat(True,True,margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.indestructible', 'hurt.trigger', 'hurt.effect')})
    def simulate_defend_opponent_dies_self_survives_beyond_boundary(self):
        return self._reflect_combat(True,True,margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.indestructible', 'hurt.trigger', 'hurt.effect')})
    def simulate_defend_both_survive(self):
        return self._reflect_combat(True,False,margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.indestructible', 'hurt.trigger', 'hurt.effect')})
    def simulate_defend_both_survive_beyond_boundary(self):
        return self._reflect_combat(True,False,margin=1)

    @simulate(evidence={'fields': ('attack', 'special_type')})
    def simulate_attack_empty_board(self):
        return self.scenario_unblocked(False)

    @simulate(evidence={'fields': ('attack', 'special_type')})
    def simulate_attack_opponent_passes(self):
        return self.scenario_unblocked(True)

    def _reflect_combat(self,defending,enemy_dies,margin=0):
        self.scenario_prepare()
        power, health = self.card.state
        if health <= 0:
            return self.scenario_skip()
        enemy_power = health + margin
        reflected = min(enemy_power, max(0, health - 1))
        total = power + reflected
        enemy_health = total - margin if enemy_dies else total + 1 + margin
        if enemy_power < 0 or enemy_health <= 0:
            return self.scenario_skip()
        self.scenario_creature(self.player.opponent, power=enemy_power, health=enemy_health, flags={})
        record = self.room.simulate_creature_defend(self.card) if defending else self.room.simulate_creature_attack(self.card)
        self.stage_card(self.card)
        if not defending:
            self.scenario_block()
        return record

    def _reflect_group(self, count, incoming):
        self.scenario_prepare()
        for _ in range(count):
            self.scenario_creature(self.player.opponent, power=incoming, health=self.card.state[0] + self.card.state[1] + 10, flags={})
        record = self.room.simulate_creature_attack(self.card)
        self.stage_card(self.card)
        self.scenario_block()
        return record

    @simulate(evidence={'text': ('keyword.indestructible', 'hurt.trigger', 'hurt.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_reflect_count_1_incoming_zero(self):
        return self._reflect_group(1, 0)

    @simulate(evidence={'text': ('keyword.indestructible', 'hurt.trigger', 'hurt.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_reflect_count_1_incoming_one(self):
        return self._reflect_group(1, 1)

    @simulate(evidence={'text': ('keyword.indestructible', 'hurt.trigger', 'hurt.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_reflect_count_1_incoming_lethal(self):
        return self._reflect_group(1, self.card.state[1] + 3)

    @simulate(evidence={'text': ('keyword.indestructible', 'hurt.trigger', 'hurt.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_reflect_count_3_incoming_zero(self):
        return self._reflect_group(3, 0)

    @simulate(evidence={'text': ('keyword.indestructible', 'hurt.trigger', 'hurt.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_reflect_count_3_incoming_one(self):
        return self._reflect_group(3, 1)

    @simulate(evidence={'text': ('keyword.indestructible', 'hurt.trigger', 'hurt.effect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_reflect_count_3_incoming_lethal(self):
        return self._reflect_group(3, self.card.state[1] + 3)

