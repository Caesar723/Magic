from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.sorcery.Apocalypse_Riders.model import Apocalypse_Riders


@bind_card(Apocalypse_Riders)
class Apocalypse_Riders_Simulation(Card_Simulation):
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
        "token.abilities": [
            "Each token gets a different ability, assigned in order from trample, haste, lifelink, and flying.",
            "In order, give the first token trample, the second haste, the third lifelink, and the fourth flying.",
            "Assign one different ability to each token in this order, trample, haste, lifelink, flying.",
            "The tokens receive distinct abilities in sequence, trample, then haste, then lifelink, then flying.",
            "Give the tokens one unique ability each, in order from trample through haste, lifelink, and flying.",
            "Each token gains the next ability in the ordered list of trample, haste, lifelink, and flying.",
            "Tokens are granted one different ability apiece, following the order trample, haste, lifelink, flying.",
            "The first four tokens, if created, have trample, haste, lifelink, and flying respectively.",
            "Apply trample to the first token, haste to the second, lifelink to the third, and flying to the fourth, if present.",
            "Grant each created token a distinct ability in sequence from trample, haste, lifelink, and flying.",
        ],
    }

    def _token_scene(self, own_count, enemy_count, offset=0):
        self.scenario_prepare()
        if not 0 <= self.card.effect_params["token_count"] <= 4:
            return self.scenario_skip()
        damage = self.card.effect_params.get("damage", 3)
        for owner, count in ((self.player, own_count), (self.player.opponent, enemy_count)):
            for index in range(count):
                self.scenario_creature(owner, power=index + 1, health=max(1, damage + offset), flags={})
        return self.scenario_cast()

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('token.effect', 'token.abilities'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_normal(self):
        return self._token_scene(0, 0, 0)

    @simulate(evidence={'text': ('token.effect', 'token.abilities'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_normal(self):
        return self._token_scene(1, 0, 0)

    @simulate(evidence={'text': ('token.effect', 'token.abilities'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_normal(self):
        return self._token_scene(0, 1, 0)

    @simulate(evidence={'text': ('token.effect', 'token.abilities'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_normal(self):
        return self._token_scene(1, 1, 0)

    @simulate(evidence={'text': ('token.effect', 'token.abilities'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_normal(self):
        return self._token_scene(3, 3, 0)

    @simulate(evidence={'text': ('token.effect', 'token.abilities'), 'fields': ('mana_cost',)})
    def simulate_self_fill_board_enemy_0_normal(self):
        return self._token_scene(max(0, 10 - self.card.effect_params["token_count"]), 0, 0)

