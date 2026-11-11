from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.land.Nexus_of_the_Eternal_Seas.model import Nexus_of_the_Eternal_Seas


@bind_card(Nexus_of_the_Eternal_Seas)
class Nexus_of_the_Eternal_Seas_Simulation(Card_Simulation):
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
        "activate.effect": [
            "When manually activated while your opponent controls a creature, tap it and return a random opposing creature to its owner's hand.",
            "On manual activation with an opposing creature present, tap it and move a random opposing creature to its owner's hand.",
            "If manually activated with opposing creatures in play, tap this land and return one of them at random to its owner's hand.",
            "When you manually activate it and an opposing creature exists, tap it to return a random one to its owner's hand.",
            "If your opponent has a creature during manual activation, tap this land and bounce one random opposing creature to its owner's hand.",
            "On manual activation, tap this land and return a random opposing creature to its owner's hand if any exist.",
            "When activated manually with at least one opposing creature, tap it and return one of those creatures at random to its owner's hand.",
            "If manually activated while an opponent has creatures, tap it and move one randomly chosen opposing creature back to its owner's hand.",
            "Manually activating it with an opposing creature present taps it and returns a random opposing creature to its owner's hand.",
            "When this land is manually activated and your opponent has a creature, tap it and return a randomly selected one to its owner's hand.",
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

    @simulate(evidence={'text': ('activate.effect', 'activate.fallback')})
    def simulate_activate_0_targets(self):
        self.scenario_prepare()
        for _ in range(0):
            self.scenario_creature(self.player.opponent, flags={})
        return self.room.simulate_activate_ability(self.card)

    @simulate(evidence={'text': ('activate.effect',)})
    def simulate_activate_1_targets(self):
        self.scenario_prepare()
        for _ in range(1):
            self.scenario_creature(self.player.opponent, flags={})
        return self.room.simulate_activate_ability(self.card)

    @simulate(evidence={'text': ('activate.effect',)})
    def simulate_activate_3_targets(self):
        self.scenario_prepare()
        for _ in range(3):
            self.scenario_creature(self.player.opponent, flags={})
        return self.room.simulate_activate_ability(self.card)

