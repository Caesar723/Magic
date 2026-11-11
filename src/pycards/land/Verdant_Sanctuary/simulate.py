from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.land.Verdant_Sanctuary.model import Verdant_Sanctuary
from pycards.land.Forest.model import Forest


@bind_card(Verdant_Sanctuary)
class Verdant_Sanctuary_Simulation(Card_Simulation):
    text_parts = {
        "enter.tap": [
            "When {card_name} enters the battlefield, it becomes tapped.",
            "{card_name} enters the battlefield tapped.",
            "This land enters the battlefield tapped.",
            "When this land enters play, it becomes tapped.",
            "When {card_name} enters play, tap it.",
            "When this land enters the battlefield, tap it.",
            "{card_name} comes into play tapped.",
            "This land comes into play tapped.",
            "As {card_name} enters the battlefield, it becomes tapped.",
            "As this land enters the battlefield, it becomes tapped.",
        ],
        "enter.mana": [
            "It also adds {mana_amount} green mana when it enters the battlefield.",
            "Its entry also adds {mana_amount} green mana to your mana pool.",
            "On entering the battlefield, it also produces {mana_amount} green mana.",
            "When it enters play, add {mana_amount} green mana to your mana pool.",
            "Its entry produces {mana_amount} green mana for you.",
            "Entering the battlefield also gives you {mana_amount} green mana.",
            "When this land enters the battlefield, add {mana_amount} green mana.",
            "Add {mana_amount} green mana to your pool when this land enters play.",
            "As this land enters play, it adds {mana_amount} green mana to your pool.",
            "On entry, you also receive {mana_amount} green mana.",
        ],
        "mana.effect": [
            "Tap this land to add {mana_amount} green mana.",
            "You may tap {card_name} to add {mana_amount} green mana to your pool.",
            "Tap {card_name} to produce {mana_amount} green mana.",
            "Tapping this land for mana adds {mana_amount} green mana.",
            "This land can be tapped for {mana_amount} green mana.",
            "You may tap this land for {mana_amount} green mana.",
            "Tap it for mana to add {mana_amount} green mana to your mana pool.",
            "By tapping {card_name} for mana, you gain {mana_amount} green mana.",
            "You can tap this land to produce {mana_amount} green mana.",
            "{card_name} can produce {mana_amount} green mana when tapped for mana.",
        ],
        "activate.condition": [
            "If manually activated while you have at least {damage} life and a basic Forest in your library,",
            "On manual activation, if your life is {damage} or higher and your library contains a basic Forest,",
            "When manually activated with a basic Forest in your library and at least {damage} life,",
            "If you manually activate it with {damage} or more life and a library Forest,",
            "If your life total is at least {damage} and a basic Forest is in your library during manual activation,",
            "On a manual activation with a library Forest and a life total no lower than {damage},",
            "When manually activated while a basic Forest is in your library and your life is at least {damage},",
            "If manual activation occurs with {damage} or more life and a basic Forest available in your library,",
            "When you manually activate it with a library Forest and at least {damage} life remaining,",
            "If you have at least {damage} life and a basic Forest in your library when activating manually,",
        ],
        "activate.effect": [
            "tap this land, deal {damage} damage to yourself, and move a random basic Forest from your library to your land area tapped.",
            "tap this land, deal {damage} damage to yourself, and put a random basic Forest from your library into play tapped.",
            "tap this land, deal {damage} damage to yourself, and choose a basic Forest at random from your library and put it into your land area tapped.",
            "tap this land, deal {damage} damage to yourself, and move one randomly chosen basic Forest from your library onto the battlefield tapped.",
            "tap this land, deal {damage} damage to yourself, and put one randomly selected basic Forest in your library into your land area tapped.",
            "tap this land, deal {damage} damage to yourself, and bring a random basic Forest from your library into play tapped.",
            "tap this land, deal {damage} damage to yourself, and find a basic Forest at random in your library and put it onto the battlefield tapped.",
            "tap this land, deal {damage} damage to yourself, and take a random basic Forest out of your library and place it in your land area tapped.",
            "tap this land, deal {damage} damage to yourself, and put a randomly chosen basic Forest from your library onto the battlefield tapped.",
            "tap this land, deal {damage} damage to yourself, and move a basic Forest chosen at random from your library into play tapped.",
        ],
        "activate.fallback": [
            "If that manual mode is unavailable, activating this land instead taps it and adds {mana_amount} green mana.",
            "When the manual alternative cannot be used, tap this land and add {mana_amount} green mana instead.",
            "If the manual alternative is unavailable, the activation taps this land and produces {mana_amount} green mana.",
            "If the manual effect cannot be used, activate this land for {mana_amount} green mana and tap it.",
            "When that manual mode is unavailable, the activation gives you {mana_amount} green mana and taps this land.",
            "An activation without that manual mode adds {mana_amount} green mana and taps this land.",
            "If you cannot use the manual mode, this activation produces {mana_amount} green mana and taps it.",
            "If that alternative is not available, tap this land to add {mana_amount} green mana instead.",
            "If the manual mode is unavailable, this land taps and produces {mana_amount} green mana on activation.",
            "When unable to use that manual effect, its activation taps it and adds {mana_amount} green mana instead.",
        ],
    }

    @simulate(evidence={'text': ('enter.tap', 'enter.mana'), 'fields': ('card_type',)})
    def simulate_enter(self):
        self.scenario_prepare()
        return self.scenario_cast()

    @simulate(evidence={'fields': ('card_type',)})
    def simulate_enter_land_limit(self):
        self.scenario_prepare()
        record = self.scenario_cast()
        self.player.counter_dict["lands_summon"] = self.player.get_counter_from_dict("lands_summon_max")
        record["action"] = self.room.sample_card_action(self.player.hand.index(self.card), (0,))
        return record

    @simulate(evidence={})
    def simulate_activate_tapped(self):
        self.scenario_prepare()
        record = self.room.simulate_activate_ability(self.card)
        self.card.flag_dict["tap"] = True
        record["action"] = self.room.sample_action((22, 23))
        return record

    def _forest_scene(self, count, offset):
        self.scenario_prepare()
        self.player.library = [card for card in self.player.library if not isinstance(card, Forest)]
        self.player.library += [Forest(self.player) for _ in range(count)]
        life = self.card.effect_params["damage"] + offset
        if not 1 <= life <= self.player.ini_life:
            return self.scenario_skip()
        self.player.life = life
        return self.room.simulate_activate_ability(self.card)

    @simulate(evidence={'text': ('activate.condition', 'activate.fallback')})
    def simulate_activate_0_forests_below_cost(self):
        return self._forest_scene(0, -1)

    @simulate(evidence={'text': ('activate.condition', 'activate.fallback')})
    def simulate_activate_0_forests_equal_cost(self):
        return self._forest_scene(0, 0)

    @simulate(evidence={'text': ('activate.condition', 'activate.fallback')})
    def simulate_activate_0_forests_above_cost(self):
        return self._forest_scene(0, 1)

    @simulate(evidence={'text': ('activate.condition', 'activate.fallback')})
    def simulate_activate_1_forests_below_cost(self):
        return self._forest_scene(1, -1)

    @simulate(evidence={'text': ('activate.condition', 'activate.effect')})
    def simulate_activate_1_forests_equal_cost(self):
        return self._forest_scene(1, 0)

    @simulate(evidence={'text': ('activate.condition', 'activate.effect')})
    def simulate_activate_1_forests_above_cost(self):
        return self._forest_scene(1, 1)

    @simulate(evidence={'text': ('activate.condition', 'activate.fallback')})
    def simulate_activate_3_forests_below_cost(self):
        return self._forest_scene(3, -1)

    @simulate(evidence={'text': ('activate.condition', 'activate.effect')})
    def simulate_activate_3_forests_equal_cost(self):
        return self._forest_scene(3, 0)

    @simulate(evidence={'text': ('activate.condition', 'activate.effect')})
    def simulate_activate_3_forests_above_cost(self):
        return self._forest_scene(3, 1)

    @simulate(evidence={'text': ('activate.condition', 'activate.fallback')})
    def simulate_activate_empty_library(self):
        self.scenario_prepare()
        self.player.library.clear()
        self.player.life = self.player.ini_life
        return self.room.simulate_activate_ability(self.card)

