from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.sorcery.Falling_Stars.model import Falling_Stars


@bind_card(Falling_Stars)
class Falling_Stars_Simulation(Card_Simulation):
    text_parts = {
        "damage.effect": [
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
        "token.effect": [
            "create {token_count} {token_power}/{token_toughness} red Star Beast creature token{token_count_plural}.",
            "put {token_count} {token_power}/{token_toughness} red Star Beast creature token{token_count_plural} onto the battlefield.",
            "summon {token_count} red {token_power}/{token_toughness} Star Beast creature token{token_count_plural}.",
            "create {token_count_word} red Star Beast creature token{token_count_plural} with power {token_power} and toughness {token_toughness}.",
            "create {token_count_word} {token_power}/{token_toughness} red Star Beast creature token{token_count_plural} under your control.",
            "put {token_count_word} red {token_power}/{token_toughness} Star Beast creature token{token_count_plural} into play.",
            "create a total of {token_count} red Star Beast creature token{token_count_plural}, each {token_power}/{token_toughness}.",
            "add {token_count} {token_power}/{token_toughness} red Star Beast creature token{token_count_plural} to your battlefield.",
            "bring {token_count_word} red Star Beast creature token{token_count_plural} into play with {token_power} power and {token_toughness} toughness each.",
            "create {token_count} Star Beast creature token{token_count_plural} that are red and {token_power}/{token_toughness}.",
        ],
    }

    def _token_scene(self, own_count, enemy_count, offset=0):
        self.scenario_prepare()
        damage = self.card.effect_params.get("damage", 3)
        for owner, count in ((self.player, own_count), (self.player.opponent, enemy_count)):
            for index in range(count):
                self.scenario_creature(owner, power=index + 1, health=max(1, damage + offset), flags={})
        return self.scenario_cast()

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_below(self):
        return self._token_scene(0, 0, -1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_equal(self):
        return self._token_scene(0, 0, 0)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_above(self):
        return self._token_scene(0, 0, 1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_below(self):
        return self._token_scene(1, 0, -1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_equal(self):
        return self._token_scene(1, 0, 0)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_above(self):
        return self._token_scene(1, 0, 1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_below(self):
        return self._token_scene(0, 1, -1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_equal(self):
        return self._token_scene(0, 1, 0)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_above(self):
        return self._token_scene(0, 1, 1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_below(self):
        return self._token_scene(1, 1, -1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_equal(self):
        return self._token_scene(1, 1, 0)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_above(self):
        return self._token_scene(1, 1, 1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_below(self):
        return self._token_scene(3, 3, -1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_equal(self):
        return self._token_scene(3, 3, 0)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_above(self):
        return self._token_scene(3, 3, 1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_fill_board_enemy_0_below(self):
        return self._token_scene(max(0, 10 - self.card.effect_params["token_count"]), 0, -1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_fill_board_enemy_0_equal(self):
        return self._token_scene(max(0, 10 - self.card.effect_params["token_count"]), 0, 0)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_fill_board_enemy_0_above(self):
        return self._token_scene(max(0, 10 - self.card.effect_params["token_count"]), 0, 1)

