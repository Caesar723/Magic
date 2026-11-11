from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.land.Mystic_Reflection_Pool.model import Mystic_Reflection_Pool


@bind_card(Mystic_Reflection_Pool)
class Mystic_Reflection_Pool_Simulation(Card_Simulation):
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
            "It also adds {mana_amount} blue mana when it enters the battlefield.",
            "Its entry also adds {mana_amount} blue mana to your mana pool.",
            "On entering the battlefield, it also produces {mana_amount} blue mana.",
            "When it enters play, add {mana_amount} blue mana to your mana pool.",
            "Its entry produces {mana_amount} blue mana for you.",
            "Entering the battlefield also gives you {mana_amount} blue mana.",
            "When this land enters the battlefield, add {mana_amount} blue mana.",
            "Add {mana_amount} blue mana to your pool when this land enters play.",
            "As this land enters play, it adds {mana_amount} blue mana to your pool.",
            "On entry, you also receive {mana_amount} blue mana.",
        ],
        "mana.effect": [
            "Tap this land to add {mana_amount} blue mana.",
            "You may tap {card_name} to add {mana_amount} blue mana to your pool.",
            "Tap {card_name} to produce {mana_amount} blue mana.",
            "Tapping this land for mana adds {mana_amount} blue mana.",
            "This land can be tapped for {mana_amount} blue mana.",
            "You may tap this land for {mana_amount} blue mana.",
            "Tap it for mana to add {mana_amount} blue mana to your mana pool.",
            "By tapping {card_name} for mana, you gain {mana_amount} blue mana.",
            "You can tap this land to produce {mana_amount} blue mana.",
            "{card_name} can produce {mana_amount} blue mana when tapped for mana.",
        ],
        "activate.condition": [
            "If you manually activate it and can pay {activation_cost} mana without using this land,",
            "On manual activation, if {activation_cost} mana is payable without this land,",
            "If a manual activation can be funded with {activation_cost} mana from other sources,",
            "When activated manually with {activation_cost} mana available from elsewhere,",
            "If you activate it manually and can afford {activation_cost} mana from other sources,",
            "When manually activated with {activation_cost} mana payable without this land,",
            "On a manual activation for which {activation_cost} mana can be paid from elsewhere,",
            "If {activation_cost} mana can be paid without this land during manual activation,",
            "When you manually activate it with access to {activation_cost} mana from other sources,",
            "If manual activation has {activation_cost} mana available without using this land,",
        ],
        "activate.effect": [
            "pay that mana, scry {scry_count}, then draw {draw_count} card{draw_count_plural} and tap this land.",
            "pay the cost, scry {scry_count}, draw {draw_count} card{draw_count_plural}, and tap it.",
            "pay {activation_cost} mana, scry {scry_count}, then draw {draw_count} card{draw_count_plural} and tap it.",
            "pay the mana cost and scry {scry_count}, then draw {draw_count} card{draw_count_plural} and tap this land.",
            "spend that mana to scry {scry_count} and then draw {draw_count} card{draw_count_plural}, tapping this land.",
            "pay {activation_cost} mana to scry {scry_count} and then draw {draw_count} card{draw_count_plural}, and this land becomes tapped.",
            "spend the cost, scry {scry_count}, then draw {draw_count} card{draw_count_plural}, and tap {card_name}.",
            "pay that cost, perform scry {scry_count}, then draw {draw_count} card{draw_count_plural} and tap {card_name}.",
            "pay {activation_cost} mana, then scry {scry_count} and draw {draw_count} card{draw_count_plural}, tapping it.",
            "spend {activation_cost} mana to scry {scry_count}, draw {draw_count} card{draw_count_plural}, and tap this land.",
        ],
        "activate.fallback": [
            "If that manual mode is unavailable, activating this land instead taps it and adds {mana_amount} blue mana.",
            "When the manual alternative cannot be used, tap this land and add {mana_amount} blue mana instead.",
            "If the manual alternative is unavailable, the activation taps this land and produces {mana_amount} blue mana.",
            "If the manual effect cannot be used, activate this land for {mana_amount} blue mana and tap it.",
            "When that manual mode is unavailable, the activation gives you {mana_amount} blue mana and taps this land.",
            "An activation without that manual mode adds {mana_amount} blue mana and taps this land.",
            "If you cannot use the manual mode, this activation produces {mana_amount} blue mana and taps it.",
            "If that alternative is not available, tap this land to add {mana_amount} blue mana instead.",
            "If the manual mode is unavailable, this land taps and produces {mana_amount} blue mana on activation.",
            "When unable to use that manual effect, its activation taps it and adds {mana_amount} blue mana instead.",
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

    def _scry_scene(self, library_count, mana):
        self.scenario_prepare({"library": {"instant_number": (library_count, library_count), "creature_number": (0, 0), "sorcery_number": (0, 0), "land_number": (0, 0)}})
        self.player.library = self.player.library[:library_count]
        self.player.mana["colorless"] = mana
        return self.room.simulate_activate_ability(self.card)

    @simulate(evidence={'text': ('activate.condition', 'activate.effect')})
    def simulate_activate_empty(self):
        return self._scry_scene(0, self.card.effect_params["activation_cost"])

    @simulate(evidence={'text': ('activate.condition', 'activate.effect')})
    def simulate_activate_short(self):
        return self._scry_scene(max(0, self.card.effect_params["draw_count"] - 1), self.card.effect_params["activation_cost"])

    @simulate(evidence={'text': ('activate.condition', 'activate.effect')})
    def simulate_activate_exact_draw(self):
        return self._scry_scene(self.card.effect_params["draw_count"], self.card.effect_params["activation_cost"])

    @simulate(evidence={'text': ('activate.condition', 'activate.effect')})
    def simulate_activate_short_scry(self):
        return self._scry_scene(max(0, self.card.effect_params["scry_count"] - 1), self.card.effect_params["activation_cost"])

    @simulate(evidence={'text': ('activate.condition', 'activate.effect')})
    def simulate_activate_exact_scry(self):
        return self._scry_scene(self.card.effect_params["scry_count"], self.card.effect_params["activation_cost"])

    @simulate(evidence={'text': ('activate.condition', 'activate.effect')})
    def simulate_activate_plenty(self):
        return self._scry_scene(self.card.effect_params["scry_count"] + self.card.effect_params["draw_count"] + 2, self.card.effect_params["activation_cost"])

    @simulate(evidence={'text': ('activate.condition', 'activate.fallback')})
    def simulate_activate_insufficient_mana(self):
        return self._scry_scene(5, max(0, self.card.effect_params["activation_cost"] - 1))

