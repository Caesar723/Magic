from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.land.Elysian_Grove.model import Elysian_Grove


@bind_card(Elysian_Grove)
class Elysian_Grove_Simulation(Card_Simulation):
    scenario_locks={
        'simulate_enter_land_limit':('self.hand',),
        'simulate_activate_0_targets':('opponent.land_area',),
        'simulate_activate_1_targets':('opponent.land_area',),
        'simulate_activate_3_targets':('opponent.land_area',),
        'simulate_activate_already_tapped_target':('opponent.land_area',),
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
        "activate.effect": [
            "When manually activated while your opponent controls a land, tap this land and a random opposing land. The opposing land cannot be untapped until its controller's turn ends, when it becomes untapped.",
            "On manual activation with an opposing land present, tap this land and one random opposing land. The opposing land cannot be untapped until its controller's turn ends, when it becomes untapped.",
            "If manually activated with opposing lands in play, tap this land and one of them chosen at random. The opposing land cannot be untapped until its controller's turn ends, when it becomes untapped.",
            "When you manually activate it and an opposing land exists, tap it and a random opposing land. The opposing land cannot be untapped until its controller's turn ends, when it becomes untapped.",
            "If your opponent has a land during manual activation, tap this land and one random opposing land. The opposing land cannot be untapped until its controller's turn ends, when it becomes untapped.",
            "On manual activation, tap this land and a random opposing land if any exist. The opposing land cannot be untapped until its controller's turn ends, when it becomes untapped.",
            "When activated manually with at least one opposing land, tap this land and one of those lands at random. The opposing land cannot be untapped until its controller's turn ends, when it becomes untapped.",
            "If manually activated while an opponent has lands, tap this land and one randomly chosen opposing land. The opposing land cannot be untapped until its controller's turn ends, when it becomes untapped.",
            "Manually activating it with an opposing land present taps this land and a random opposing land. The opposing land cannot be untapped until its controller's turn ends, when it becomes untapped.",
            "When this land is manually activated and your opponent has a land, tap it and a randomly selected opposing land. The opposing land cannot be untapped until its controller's turn ends, when it becomes untapped.",
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

    @simulate(evidence={'text': ('activate.effect', 'activate.fallback')})
    def simulate_activate_0_targets(self):
        self.scenario_prepare()
        self.room.env_mana(self.player.opponent, {"G": (0, 0)})
        return self.room.simulate_activate_ability(self.card)

    @simulate(evidence={'text': ('activate.effect',)})
    def simulate_activate_1_targets(self):
        self.scenario_prepare()
        self.room.env_mana(self.player.opponent, {"G": (1, 1)})
        return self.room.simulate_activate_ability(self.card)

    @simulate(evidence={'text': ('activate.effect',)})
    def simulate_activate_3_targets(self):
        self.scenario_prepare()
        self.room.env_mana(self.player.opponent, {"G": (3, 3)})
        return self.room.simulate_activate_ability(self.card)

    @simulate(evidence={'text': ('activate.effect',)})
    def simulate_activate_already_tapped_target(self):
        self.scenario_prepare()
        self.room.env_mana(self.player.opponent, {"G": (1, 1)})
        self.scenario_tapped(self.player.opponent.land_area[0])
        return self.room.simulate_activate_ability(self.card)

