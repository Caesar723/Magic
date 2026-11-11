from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.land.Sanctum_of_Verdant_Growth.model import Sanctum_of_Verdant_Growth
from pycards.land.Forest.model import Forest


@bind_card(Sanctum_of_Verdant_Growth)
class Sanctum_of_Verdant_Growth_Simulation(Card_Simulation):
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
            "If manually activated with {activation_cost} mana payable without this land and a basic Forest in your library,",
            "On manual activation, if you have a basic Forest in your library and can pay {activation_cost} mana from elsewhere,",
            "If you manually activate it with a basic Forest available in your library and {activation_cost} mana from other sources,",
            "When manually activated with a basic Forest in your library and {activation_cost} mana payable without this land,",
            "If a manual activation has a library Forest and {activation_cost} mana available from other sources,",
            "On a manual activation for which a basic Forest is in your library and {activation_cost} mana can be paid from elsewhere,",
            "When you manually activate it with a library Forest and access to {activation_cost} mana without this land,",
            "If {activation_cost} mana is payable without this land and your library contains a basic Forest during manual activation,",
            "When activated manually while a basic Forest is in your library and {activation_cost} mana is available from elsewhere,",
            "If you activate it manually, can pay {activation_cost} mana without this land, and have a library Forest,",
        ],
        "activate.effect": [
            "pay {activation_cost} mana, tap this land, and move a random basic Forest from your library to your land area tapped.",
            "pay {activation_cost} mana, tap this land, and put a random basic Forest from your library into play tapped.",
            "pay {activation_cost} mana, tap this land, and choose a basic Forest at random from your library and put it into your land area tapped.",
            "pay {activation_cost} mana, tap this land, and move one randomly chosen basic Forest from your library onto the battlefield tapped.",
            "pay {activation_cost} mana, tap this land, and put one randomly selected basic Forest in your library into your land area tapped.",
            "pay {activation_cost} mana, tap this land, and bring a random basic Forest from your library into play tapped.",
            "pay {activation_cost} mana, tap this land, and find a basic Forest at random in your library and put it onto the battlefield tapped.",
            "pay {activation_cost} mana, tap this land, and take a random basic Forest out of your library and place it in your land area tapped.",
            "pay {activation_cost} mana, tap this land, and put a randomly chosen basic Forest from your library onto the battlefield tapped.",
            "pay {activation_cost} mana, tap this land, and move a basic Forest chosen at random from your library into play tapped.",
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
        self.player.mana["colorless"] = max(0, self.card.effect_params["activation_cost"] + offset)
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
        self.player.mana["colorless"] = self.card.effect_params["activation_cost"]
        return self.room.simulate_activate_ability(self.card)

