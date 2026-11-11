from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Blightsteel_Colossus.model import Blightsteel_Colossus


@bind_card(Blightsteel_Colossus)
class Blightsteel_Colossus_Simulation(Card_Simulation):
    scenario_locks={
        '_infect_combat':('opponent.battlefield', 'self.battlefield'),
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
        "keyword.infect": [
            "Infect. Damage to creatures applies an equal negative power and health buff. Damage to players removes life normally.",
            "This creature applies creature damage as equal power and health reductions, while player damage reduces life.",
            "Creature damage from this creature becomes negative power and health buffs. Player damage still removes life.",
            "Infect converts this creature's damage to creatures into power and health reductions, with ordinary life damage to players.",
            "Damage dealt to a creature is applied as a negative power and health buff. Damage to a player affects life.",
            "This creature reduces a damaged creature's power and health by the damage amount, but damages players through life loss.",
            "Infect applies matching power and health reductions to creatures, while damage to players reduces their life total.",
            "This creature's creature damage becomes equal negative power and health buffs, and its player damage remains life damage.",
            "When this creature damages a creature, reduce that creature's power and health by the amount. Player damage removes life.",
            "Creature targets receive power and health reductions for this creature's damage, while player targets lose life normally.",
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

    @simulate(evidence={'text': ('keyword.trample', 'keyword.infect', 'keyword.indestructible'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self._infect_combat(False, True, False, margin=0)

    @simulate(evidence={'text': ('keyword.trample', 'keyword.infect', 'keyword.indestructible'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives_beyond_boundary(self):
        return self._infect_combat(False, True, False, margin=1)

    @simulate(evidence={'text': ('keyword.trample', 'keyword.infect', 'keyword.indestructible'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive(self):
        return self._infect_combat(False, False, False, margin=0)

    @simulate(evidence={'text': ('keyword.trample', 'keyword.infect', 'keyword.indestructible'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive_beyond_boundary(self):
        return self._infect_combat(False, False, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.infect', 'keyword.indestructible')})
    def simulate_defend_opponent_dies_self_survives(self):
        return self._infect_combat(True, True, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.infect', 'keyword.indestructible')})
    def simulate_defend_opponent_dies_self_survives_beyond_boundary(self):
        return self._infect_combat(True, True, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.infect', 'keyword.indestructible')})
    def simulate_defend_both_survive(self):
        return self._infect_combat(True, False, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.infect', 'keyword.indestructible')})
    def simulate_defend_both_survive_beyond_boundary(self):
        return self._infect_combat(True, False, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'special_type'), 'text': ('keyword.infect',)})
    def simulate_attack_empty_board(self):
        return self.scenario_unblocked(False)

    @simulate(evidence={'fields': ('attack', 'special_type'), 'text': ('keyword.infect',)})
    def simulate_attack_opponent_passes(self):
        return self.scenario_unblocked(True)

    def _infect_combat(self, defending, enemy_dies, self_dies=False, margin=0):
        self.scenario_prepare()
        power, health = self.card.state
        if health <= 0:
            return self.scenario_skip()
        enemy_power = health + margin if self_dies else health - 1 - margin
        if not defending:
            enemy_power += power
        enemy_health = power - margin if enemy_dies else power + 1 + margin
        if enemy_power < 0 or enemy_health <= 0:
            return self.scenario_skip()
        self.scenario_creature(self.player.opponent, power=enemy_power, health=enemy_health, flags={})
        record = self.room.simulate_creature_defend(self.card) if defending else self.room.simulate_creature_attack(self.card)
        self.stage_card(self.card)
        if not defending:
            self.scenario_block()
        return record

