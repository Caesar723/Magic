from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.sorcery.Radiant_Procession.model import Radiant_Procession


@bind_card(Radiant_Procession)
class Radiant_Procession_Simulation(Card_Simulation):
    scenario_locks={
        '_token_scene':('opponent.battlefield', 'self.battlefield'),
    }

    text_parts = {
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
        "token.keyword": [
            "Each of these tokens has vigilance.",
            "All of these tokens have vigilance.",
            "Every token created this way has vigilance.",
            "Give each created token vigilance.",
            "Each new token has the vigilance ability.",
            "All tokens created by this effect have vigilance.",
            "The created tokens all have vigilance.",
            "Each token created by this spell has vigilance.",
            "Every newly created token receives vigilance.",
            "These tokens are each created with vigilance.",
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

    @simulate(evidence={'text': ('token.effect', 'token.keyword'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_normal(self):
        return self._token_scene(0, 0, 0)

    @simulate(evidence={'text': ('token.effect', 'token.keyword'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_normal(self):
        return self._token_scene(1, 0, 0)

    @simulate(evidence={'text': ('token.effect', 'token.keyword'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_normal(self):
        return self._token_scene(0, 1, 0)

    @simulate(evidence={'text': ('token.effect', 'token.keyword'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_normal(self):
        return self._token_scene(1, 1, 0)

    @simulate(evidence={'text': ('token.effect', 'token.keyword'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_normal(self):
        return self._token_scene(3, 3, 0)

    @simulate(evidence={'text': ('token.effect', 'token.keyword'), 'fields': ('mana_cost',)})
    def simulate_self_fill_board_enemy_0_normal(self):
        return self._token_scene(max(0, 10 - self.card.effect_params["token_count"]), 0, 0)

