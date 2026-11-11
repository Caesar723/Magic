from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.land.Sanctum_of_Eternal_Flames.model import Sanctum_of_Eternal_Flames


@bind_card(Sanctum_of_Eternal_Flames)
class Sanctum_of_Eternal_Flames_Simulation(Card_Simulation):
    scenario_locks={
        'simulate_enter_land_limit':('self.hand',),
        '_damage_scene':('self.land_area',),
    }

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
            "It also adds {mana_amount} red mana when it enters the battlefield.",
            "Its entry also adds {mana_amount} red mana to your mana pool.",
            "On entering the battlefield, it also produces {mana_amount} red mana.",
            "When it enters play, add {mana_amount} red mana to your mana pool.",
            "Its entry produces {mana_amount} red mana for you.",
            "Entering the battlefield also gives you {mana_amount} red mana.",
            "When this land enters the battlefield, add {mana_amount} red mana.",
            "Add {mana_amount} red mana to your pool when this land enters play.",
            "As this land enters play, it adds {mana_amount} red mana to your pool.",
            "On entry, you also receive {mana_amount} red mana.",
        ],
        "mana.effect": [
            "Tap this land to add {mana_amount} red mana.",
            "You may tap {card_name} to add {mana_amount} red mana to your pool.",
            "Tap {card_name} to produce {mana_amount} red mana.",
            "Tapping this land for mana adds {mana_amount} red mana.",
            "This land can be tapped for {mana_amount} red mana.",
            "You may tap this land for {mana_amount} red mana.",
            "Tap it for mana to add {mana_amount} red mana to your mana pool.",
            "By tapping {card_name} for mana, you gain {mana_amount} red mana.",
            "You can tap this land to produce {mana_amount} red mana.",
            "{card_name} can produce {mana_amount} red mana when tapped for mana.",
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
            "pay {activation_cost} mana, tap this land, and deal {damage} damage to a random object among your opponent and their creatures.",
            "spend {activation_cost} mana and tap it to deal {damage} damage to a random opposing creature or the opposing player.",
            "pay the cost and tap it, dealing {damage} damage to one random choice among your opponent and all their creatures.",
            "pay {activation_cost} mana and tap this land, then deal {damage} damage to a randomly chosen opposing creature or your opponent.",
            "spend that mana and tap this land to deal {damage} damage to a random choice from the opposing player and their creatures.",
            "pay the cost, tap {card_name}, and deal {damage} damage to a random opposing creature or player.",
            "pay {activation_cost} mana to tap it and deal {damage} damage to one randomly selected opposing creature or the opponent.",
            "spend {activation_cost} mana, tap this land, and deal {damage} damage to a random member of the opponent and their creatures.",
            "pay that mana, tap it, and deal {damage} damage to a randomly selected object from your opponent and their creatures.",
            "pay the mana cost and tap this land to deal {damage} damage to a random choice among the opposing creatures and player.",
        ],
        "activate.fallback": [
            "If that manual mode is unavailable, activating this land instead taps it and adds {mana_amount} red mana.",
            "When the manual alternative cannot be used, tap this land and add {mana_amount} red mana instead.",
            "If the manual alternative is unavailable, the activation taps this land and produces {mana_amount} red mana.",
            "If the manual effect cannot be used, activate this land for {mana_amount} red mana and tap it.",
            "When that manual mode is unavailable, the activation gives you {mana_amount} red mana and taps this land.",
            "An activation without that manual mode adds {mana_amount} red mana and taps this land.",
            "If you cannot use the manual mode, this activation produces {mana_amount} red mana and taps it.",
            "If that alternative is not available, tap this land to add {mana_amount} red mana instead.",
            "If the manual mode is unavailable, this land taps and produces {mana_amount} red mana on activation.",
            "When unable to use that manual effect, its activation taps it and adds {mana_amount} red mana instead.",
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

    def _damage_scene(self, creatures, life_offset, mana_offset=0):
        self.scenario_prepare()
        damage = self.card.effect_params["damage"]
        life = damage + life_offset
        if not 1 <= life <= self.player.opponent.ini_life:
            return self.scenario_skip()
        self.player.opponent.life = life
        for _ in range(creatures):
            self.scenario_creature(self.player.opponent, power=1, health=life, flags={})
        self.player.mana["colorless"] = max(0, self.card.effect_params["activation_cost"] + mana_offset)
        return self.room.simulate_activate_ability(self.card)

    @simulate(evidence={'text': ('activate.condition', 'activate.effect')})
    def simulate_activate_0_creatures_below_lethal(self):
        return self._damage_scene(0, -1)

    @simulate(evidence={'text': ('activate.condition', 'activate.effect')})
    def simulate_activate_0_creatures_equal_lethal(self):
        return self._damage_scene(0, 0)

    @simulate(evidence={'text': ('activate.condition', 'activate.effect')})
    def simulate_activate_0_creatures_above_lethal(self):
        return self._damage_scene(0, 1)

    @simulate(evidence={'text': ('activate.condition', 'activate.effect')})
    def simulate_activate_1_creatures_below_lethal(self):
        return self._damage_scene(1, -1)

    @simulate(evidence={'text': ('activate.condition', 'activate.effect')})
    def simulate_activate_1_creatures_equal_lethal(self):
        return self._damage_scene(1, 0)

    @simulate(evidence={'text': ('activate.condition', 'activate.effect')})
    def simulate_activate_1_creatures_above_lethal(self):
        return self._damage_scene(1, 1)

    @simulate(evidence={'text': ('activate.condition', 'activate.effect')})
    def simulate_activate_3_creatures_below_lethal(self):
        return self._damage_scene(3, -1)

    @simulate(evidence={'text': ('activate.condition', 'activate.effect')})
    def simulate_activate_3_creatures_equal_lethal(self):
        return self._damage_scene(3, 0)

    @simulate(evidence={'text': ('activate.condition', 'activate.effect')})
    def simulate_activate_3_creatures_above_lethal(self):
        return self._damage_scene(3, 1)

    @simulate(evidence={'text': ('activate.condition', 'activate.fallback')})
    def simulate_activate_insufficient_mana(self):
        return self._damage_scene(1, 1, -1)

