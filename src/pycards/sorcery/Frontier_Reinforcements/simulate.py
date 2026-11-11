from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.sorcery.Frontier_Reinforcements.model import Frontier_Reinforcements


@bind_card(Frontier_Reinforcements)
class Frontier_Reinforcements_Simulation(Card_Simulation):
    text_parts = {
        "empty.condition": [
            "If you control no creatures,",
            "If there are no creatures on your battlefield,",
            "When your battlefield has no creatures,",
            "If you have no creatures in play,",
            "If you do not control a creature,",
            "When there is no creature under your control,",
            "If your side of the battlefield is empty of creatures,",
            "If you have zero creatures on the battlefield,",
            "When you control zero creatures,",
            "If none of the creatures in play are under your control,",
        ],
        "empty.tokens": [
            "create {token_count_empty} {token_power}/{token_toughness} green Scout creature token{token_count_empty_plural}.",
            "put {token_count_empty} {token_power}/{token_toughness} green Scout creature token{token_count_empty_plural} onto the battlefield.",
            "summon {token_count_empty} green {token_power}/{token_toughness} Scout creature token{token_count_empty_plural}.",
            "create {token_count_empty_word} green Scout creature token{token_count_empty_plural} with power {token_power} and toughness {token_toughness}.",
            "create {token_count_empty_word} {token_power}/{token_toughness} green Scout creature token{token_count_empty_plural} under your control.",
            "put {token_count_empty_word} green {token_power}/{token_toughness} Scout creature token{token_count_empty_plural} into play.",
            "create a total of {token_count_empty} green Scout creature token{token_count_empty_plural}, each {token_power}/{token_toughness}.",
            "add {token_count_empty} {token_power}/{token_toughness} green Scout creature token{token_count_empty_plural} to your battlefield.",
            "bring {token_count_empty_word} green Scout creature token{token_count_empty_plural} into play with {token_power} power and {token_toughness} toughness each.",
            "create {token_count_empty} Scout creature token{token_count_empty_plural} that are green and {token_power}/{token_toughness}.",
        ],
        "occupied.tokens": [
            "Otherwise, create {token_count} {token_power}/{token_toughness} green Scout creature token{token_count_plural}.",
            "Otherwise, put {token_count} {token_power}/{token_toughness} green Scout creature token{token_count_plural} onto the battlefield.",
            "Otherwise, summon {token_count} green {token_power}/{token_toughness} Scout creature token{token_count_plural}.",
            "Otherwise, create {token_count_word} green Scout creature token{token_count_plural} with power {token_power} and toughness {token_toughness}.",
            "Otherwise, create {token_count_word} {token_power}/{token_toughness} green Scout creature token{token_count_plural} under your control.",
            "Otherwise, put {token_count_word} green {token_power}/{token_toughness} Scout creature token{token_count_plural} into play.",
            "Otherwise, create a total of {token_count} green Scout creature token{token_count_plural}, each {token_power}/{token_toughness}.",
            "Otherwise, add {token_count} {token_power}/{token_toughness} green Scout creature token{token_count_plural} to your battlefield.",
            "Otherwise, bring {token_count_word} green Scout creature token{token_count_plural} into play with {token_power} power and {token_toughness} toughness each.",
            "Otherwise, create {token_count} Scout creature token{token_count_plural} that are green and {token_power}/{token_toughness}.",
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

    @simulate(evidence={'text': ('empty.condition', 'empty.tokens'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_normal(self):
        return self._token_scene(0, 0, 0)

    @simulate(evidence={'text': ('empty.condition', 'occupied.tokens'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_normal(self):
        return self._token_scene(1, 0, 0)

    @simulate(evidence={'text': ('empty.condition', 'empty.tokens'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_normal(self):
        return self._token_scene(0, 1, 0)

    @simulate(evidence={'text': ('empty.condition', 'occupied.tokens'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_normal(self):
        return self._token_scene(1, 1, 0)

    @simulate(evidence={'text': ('empty.condition', 'occupied.tokens'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_normal(self):
        return self._token_scene(3, 3, 0)

    @simulate(evidence={'text': ('empty.condition', 'occupied.tokens'), 'fields': ('mana_cost',)})
    def simulate_self_fill_board_enemy_0_normal(self):
        return self._token_scene(max(0, 10 - self.card.effect_params["token_count"]), 0, 0)

