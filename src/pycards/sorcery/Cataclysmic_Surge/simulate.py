from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.sorcery.Cataclysmic_Surge.model import Cataclysmic_Surge


@bind_card(Cataclysmic_Surge)
class Cataclysmic_Surge_Simulation(Card_Simulation):
    text_parts = {
        "damage.creatures": [
            "{card_name} deals {damage} damage to every creature.",
            "Deal {damage} damage to each creature on the battlefield.",
            "Every creature takes {damage} damage from {card_name}.",
            "Inflict {damage} damage on all creatures.",
            "Deal {damage} damage to all creatures on both sides.",
            "{card_name} hits each creature for {damage} damage.",
            "Each creature on either battlefield is dealt {damage} damage.",
            "{card_name} deals {damage} damage to all creatures in play.",
            "Deal an amount of damage equal to {damage} to each creature.",
            "All creatures take {damage} damage each.",
        ],
        "damage.players": [
            "Then it deals {damage} damage to each player.",
            "It also deals {damage} damage to both players.",
            "Afterward, each player takes {damage} damage.",
            "Next, deal {damage} damage to every player.",
            "It then hits both players for {damage} damage each.",
            "Then inflict {damage} damage on each player.",
            "Both players are then dealt {damage} damage.",
            "It deals {damage} damage to you and your opponent afterward.",
            "Next, both you and your opponent take {damage} damage.",
            "Then deal an amount of damage equal to {damage} to each player.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _sweep_scene(self, own_count, enemy_count, life_offset, enemy_life_offset):
        self.scenario_prepare()
        damage = self.card.effect_params["damage"]
        for owner, count in ((self.player, own_count), (self.player.opponent, enemy_count)):
            for index in range(count):
                self.scenario_creature(owner, power=index + 1, health=max(1, damage + index - 1), flags={})
        own_life = damage + life_offset
        enemy_life = self.card.effect_params.get("opponent_damage", damage) + enemy_life_offset
        if not (1 <= own_life <= self.player.ini_life and 1 <= enemy_life <= self.player.opponent.ini_life):
            return self.scenario_skip()
        self.player.life = own_life
        self.player.opponent.life = enemy_life
        return self.scenario_cast()

    @simulate(evidence={'text': ('damage.creatures', 'damage.players'), 'fields': ('mana_cost',)})
    def simulate_sweep_self_0_enemy_0_below_lethal(self):
        return self._sweep_scene(0, 0, -1, -1)

    @simulate(evidence={'text': ('damage.creatures', 'damage.players'), 'fields': ('mana_cost',)})
    def simulate_sweep_self_0_enemy_0_equal_lethal(self):
        return self._sweep_scene(0, 0, 0, 0)

    @simulate(evidence={'text': ('damage.creatures', 'damage.players'), 'fields': ('mana_cost',)})
    def simulate_sweep_self_0_enemy_0_above_lethal(self):
        return self._sweep_scene(0, 0, 1, 1)

    @simulate(evidence={'text': ('damage.creatures', 'damage.players'), 'fields': ('mana_cost',)})
    def simulate_sweep_self_0_enemy_1_below_lethal(self):
        return self._sweep_scene(0, 1, -1, -1)

    @simulate(evidence={'text': ('damage.creatures', 'damage.players'), 'fields': ('mana_cost',)})
    def simulate_sweep_self_0_enemy_1_equal_lethal(self):
        return self._sweep_scene(0, 1, 0, 0)

    @simulate(evidence={'text': ('damage.creatures', 'damage.players'), 'fields': ('mana_cost',)})
    def simulate_sweep_self_0_enemy_1_above_lethal(self):
        return self._sweep_scene(0, 1, 1, 1)

    @simulate(evidence={'text': ('damage.creatures', 'damage.players'), 'fields': ('mana_cost',)})
    def simulate_sweep_self_1_enemy_0_below_lethal(self):
        return self._sweep_scene(1, 0, -1, -1)

    @simulate(evidence={'text': ('damage.creatures', 'damage.players'), 'fields': ('mana_cost',)})
    def simulate_sweep_self_1_enemy_0_equal_lethal(self):
        return self._sweep_scene(1, 0, 0, 0)

    @simulate(evidence={'text': ('damage.creatures', 'damage.players'), 'fields': ('mana_cost',)})
    def simulate_sweep_self_1_enemy_0_above_lethal(self):
        return self._sweep_scene(1, 0, 1, 1)

    @simulate(evidence={'text': ('damage.creatures', 'damage.players'), 'fields': ('mana_cost',)})
    def simulate_sweep_self_1_enemy_1_below_lethal(self):
        return self._sweep_scene(1, 1, -1, -1)

    @simulate(evidence={'text': ('damage.creatures', 'damage.players'), 'fields': ('mana_cost',)})
    def simulate_sweep_self_1_enemy_1_equal_lethal(self):
        return self._sweep_scene(1, 1, 0, 0)

    @simulate(evidence={'text': ('damage.creatures', 'damage.players'), 'fields': ('mana_cost',)})
    def simulate_sweep_self_1_enemy_1_above_lethal(self):
        return self._sweep_scene(1, 1, 1, 1)

    @simulate(evidence={'text': ('damage.creatures', 'damage.players'), 'fields': ('mana_cost',)})
    def simulate_sweep_self_3_enemy_3_below_lethal(self):
        return self._sweep_scene(3, 3, -1, -1)

    @simulate(evidence={'text': ('damage.creatures', 'damage.players'), 'fields': ('mana_cost',)})
    def simulate_sweep_self_3_enemy_3_equal_lethal(self):
        return self._sweep_scene(3, 3, 0, 0)

    @simulate(evidence={'text': ('damage.creatures', 'damage.players'), 'fields': ('mana_cost',)})
    def simulate_sweep_self_3_enemy_3_above_lethal(self):
        return self._sweep_scene(3, 3, 1, 1)

