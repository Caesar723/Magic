from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.sorcery.Sanctuary_Judgment.model import Sanctuary_Judgment


@bind_card(Sanctuary_Judgment)
class Sanctuary_Judgment_Simulation(Card_Simulation):
    text_parts = {
        "clear.effect": [
            "Destroy all creatures.",
            "Destroy every creature in play.",
            "Destroy each creature on the battlefield.",
            "Destroy all creatures on both sides.",
            "All creatures are destroyed.",
            "Destroy every creature on either battlefield.",
            "Destroy each creature in play.",
            "Destroy all creatures on the battlefield.",
            "Every creature in play is destroyed.",
            "Destroy each creature controlled by either player.",
        ],
        "token.effect": [
            "create {token_count} {token_power}/{token_toughness} white Knight creature token{token_count_plural}.",
            "put {token_count} {token_power}/{token_toughness} white Knight creature token{token_count_plural} onto the battlefield.",
            "summon {token_count} white {token_power}/{token_toughness} Knight creature token{token_count_plural}.",
            "create {token_count_word} white Knight creature token{token_count_plural} with power {token_power} and toughness {token_toughness}.",
            "create {token_count_word} {token_power}/{token_toughness} white Knight creature token{token_count_plural} under your control.",
            "put {token_count_word} white {token_power}/{token_toughness} Knight creature token{token_count_plural} into play.",
            "create a total of {token_count} white Knight creature token{token_count_plural}, each {token_power}/{token_toughness}.",
            "add {token_count} {token_power}/{token_toughness} white Knight creature token{token_count_plural} to your battlefield.",
            "bring {token_count_word} white Knight creature token{token_count_plural} into play with {token_power} power and {token_toughness} toughness each.",
            "create {token_count} Knight creature token{token_count_plural} that are white and {token_power}/{token_toughness}.",
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

    @simulate(evidence={'text': ('clear.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_normal(self):
        return self._token_scene(0, 0, 0)

    @simulate(evidence={'text': ('clear.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_normal(self):
        return self._token_scene(1, 0, 0)

    @simulate(evidence={'text': ('clear.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_normal(self):
        return self._token_scene(0, 1, 0)

    @simulate(evidence={'text': ('clear.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_normal(self):
        return self._token_scene(1, 1, 0)

    @simulate(evidence={'text': ('clear.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_normal(self):
        return self._token_scene(3, 3, 0)

    @simulate(evidence={'text': ('clear.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_fill_board_enemy_0_normal(self):
        return self._token_scene(max(0, 10 - self.card.effect_params["token_count"]), 0, 0)

