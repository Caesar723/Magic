from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Vorinclex__Apex_of_Mutation.model import Vorinclex__Apex_of_Mutation


@bind_card(Vorinclex__Apex_of_Mutation)
class Vorinclex__Apex_of_Mutation_Simulation(Card_Simulation):
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
        "cast.trigger": [
            "Whenever you cast another nonland card while this creature is on your battlefield,",
            "When you cast a different nonland card with this creature in play,",
            "Each other nonland card you cast while this creature is on your battlefield triggers this.",
            "Whenever this creature is on your battlefield and you cast another card that is not a land,",
            "For every different nonland card you cast with this creature in play,",
            "When another nonland card is cast by you while this creature remains on your battlefield,",
            "While this creature is on your battlefield, each other nonland card you cast triggers this.",
            "If you cast a different nonland card while this creature is in play,",
            "Whenever you cast another card other than a land with this creature on your battlefield,",
            "Each time you cast a different nonland card while controlling this creature on the battlefield,",
        ],
        "proliferate.effect": [
            "choose {proliferate_count} random creatures from both battlefields without replacement, or all if fewer, and duplicate one buff of each distinct content on each selected creature.",
            "randomly select up to {proliferate_count} different creatures from both sides, taking all if fewer, and copy one instance of each distinct buff content on each.",
            "pick {proliferate_count} different creatures randomly across both battlefields, limited by availability, and duplicate one buff per distinct content on each.",
            "randomly take as many as {proliferate_count} available creatures without replacement and add one copy of each distinct buff content to each.",
            "select up to {proliferate_count} different creatures at random from both sides, taking all available if fewer, and duplicate one buff per unique content on each.",
            "choose {proliferate_count} random distinct battlefield creatures if available and copy each distinct buff content once on every chosen creature.",
            "randomly select different creatures from both battlefields up to {proliferate_count}, taking all if fewer, and duplicate one buff for each unique content on them.",
            "pick random creatures without replacement across both sides, up to {proliferate_count}, and copy one instance of every distinct buff content on each.",
            "choose as many as {proliferate_count} available creatures randomly without replacement and duplicate each unique buff content once per selected creature.",
            "select {proliferate_count} distinct creatures randomly from both battlefields, or all available if fewer, then add one copy of each different buff content on each.",
        ],
        "damage.effect": [
            "For each selected opposing creature with any buffs, deal {life_cost} damage to your opponent.",
            "Deal {life_cost} damage to your opponent for every selected opposing creature that has buffs.",
            "Each chosen opposing creature carrying buffs causes {life_cost} damage to your opponent.",
            "For every selected buffed opposing creature, hit your opponent for {life_cost} damage.",
            "When a selected creature belongs to your opponent and has buffs, deal {life_cost} damage to that opponent.",
            "A chosen opposing creature with at least one buff triggers {life_cost} damage to your opponent.",
            "Hit the opposing player for {life_cost} damage per selected opposing creature that has any buff.",
            "Deal your opponent {life_cost} damage for each chosen buffed creature on their side.",
            "Each selected creature your opponent controls with any buffs makes this creature deal {life_cost} damage to that opponent.",
            "For every chosen opposing creature carrying at least one buff, inflict {life_cost} damage on your opponent.",
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

    @simulate(evidence={'text': ('keyword.trample', 'keyword.infect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self._infect_combat(False, True, False, margin=0)

    @simulate(evidence={'text': ('keyword.trample', 'keyword.infect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives_beyond_boundary(self):
        return self._infect_combat(False, True, False, margin=1)

    @simulate(evidence={'text': ('keyword.trample', 'keyword.infect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive(self):
        return self._infect_combat(False, False, False, margin=0)

    @simulate(evidence={'text': ('keyword.trample', 'keyword.infect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive_beyond_boundary(self):
        return self._infect_combat(False, False, False, margin=1)

    @simulate(evidence={'text': ('keyword.trample', 'keyword.infect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies(self):
        return self._infect_combat(False, False, True, margin=0)

    @simulate(evidence={'text': ('keyword.trample', 'keyword.infect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies_beyond_boundary(self):
        return self._infect_combat(False, False, True, margin=1)

    @simulate(evidence={'text': ('keyword.trample', 'keyword.infect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die(self):
        return self._infect_combat(False, True, True, margin=0)

    @simulate(evidence={'text': ('keyword.trample', 'keyword.infect'), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die_beyond_boundary(self):
        return self._infect_combat(False, True, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.infect',)})
    def simulate_defend_opponent_dies_self_survives(self):
        return self.scenario_combat(True, True, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.infect',)})
    def simulate_defend_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(True, True, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.infect',)})
    def simulate_defend_both_survive(self):
        return self.scenario_combat(True, False, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.infect',)})
    def simulate_defend_both_survive_beyond_boundary(self):
        return self.scenario_combat(True, False, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.infect',)})
    def simulate_defend_opponent_survives_self_dies(self):
        return self.scenario_combat(True, False, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.infect',)})
    def simulate_defend_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(True, False, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.infect',)})
    def simulate_defend_both_die(self):
        return self.scenario_combat(True, True, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('keyword.infect',)})
    def simulate_defend_both_die_beyond_boundary(self):
        return self.scenario_combat(True, True, True, margin=1)

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

