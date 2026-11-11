from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.land.Celestial_Haven.model import Celestial_Haven


@bind_card(Celestial_Haven)
class Celestial_Haven_Simulation(Card_Simulation):
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
            "It also adds {mana_amount} white mana when it enters the battlefield.",
            "Its entry also adds {mana_amount} white mana to your mana pool.",
            "On entering the battlefield, it also produces {mana_amount} white mana.",
            "When it enters play, add {mana_amount} white mana to your mana pool.",
            "Its entry produces {mana_amount} white mana for you.",
            "Entering the battlefield also gives you {mana_amount} white mana.",
            "When this land enters the battlefield, add {mana_amount} white mana.",
            "Add {mana_amount} white mana to your pool when this land enters play.",
            "As this land enters play, it adds {mana_amount} white mana to your pool.",
            "On entry, you also receive {mana_amount} white mana.",
        ],
        "mana.effect": [
            "Tap this land to add {mana_amount} white mana.",
            "You may tap {card_name} to add {mana_amount} white mana to your pool.",
            "Tap {card_name} to produce {mana_amount} white mana.",
            "Tapping this land for mana adds {mana_amount} white mana.",
            "This land can be tapped for {mana_amount} white mana.",
            "You may tap this land for {mana_amount} white mana.",
            "Tap it for mana to add {mana_amount} white mana to your mana pool.",
            "By tapping {card_name} for mana, you gain {mana_amount} white mana.",
            "You can tap this land to produce {mana_amount} white mana.",
            "{card_name} can produce {mana_amount} white mana when tapped for mana.",
        ],
        "activate.effect": [
            "On manual activation with more than {life_cost} life, this land deals {life_cost} damage to you and taps, then heals damage dealt during combat until your turn ends.",
            "If manually activated while your life is above {life_cost}, it deals {life_cost} damage to you, taps, and restores damage suffered during combat until your turn ends.",
            "When manually activated with a life total greater than {life_cost}, it damages you for {life_cost}, taps, and heals combat damage until your turn ends.",
            "With more than {life_cost} life, manual activation deals {life_cost} damage to you, taps this land, and restores damage dealt in combat until your turn ends.",
            "If your life exceeds {life_cost}, manually activating this land damages you for {life_cost} and taps it, then heals damage during combat for before your turn ends.",
            "On a manual activation while you have over {life_cost} life, it deals {life_cost} damage to you and taps, enabling combat-damage healing until your turn ends.",
            "When you manually activate it with more than {life_cost} life, take {life_cost} damage and tap it, then it heals damage received in combat before your turn ends.",
            "If manually activated with life strictly above {life_cost}, it deals {life_cost} damage to you, taps, and restores damage received during combat until your turn ends.",
            "When manual activation occurs with your life greater than {life_cost}, it damages you for {life_cost}, taps, and heals combat damage until your turn ends.",
            "At a life total above {life_cost}, manual activation makes it deal {life_cost} damage to you and tap, then restore combat damage until before your turn ends ends.",
        ],
        "activate.fallback": [
            "If that manual mode is unavailable, activating this land instead taps it and adds {mana_amount} white mana.",
            "When the manual alternative cannot be used, tap this land and add {mana_amount} white mana instead.",
            "If the manual alternative is unavailable, the activation taps this land and produces {mana_amount} white mana.",
            "If the manual effect cannot be used, activate this land for {mana_amount} white mana and tap it.",
            "When that manual mode is unavailable, the activation gives you {mana_amount} white mana and taps this land.",
            "An activation without that manual mode adds {mana_amount} white mana and taps this land.",
            "If you cannot use the manual mode, this activation produces {mana_amount} white mana and taps it.",
            "If that alternative is not available, tap this land to add {mana_amount} white mana instead.",
            "If the manual mode is unavailable, this land taps and produces {mana_amount} white mana on activation.",
            "When unable to use that manual effect, its activation taps it and adds {mana_amount} white mana instead.",
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
    def simulate_activate_life_below(self):
        self.scenario_prepare()
        life = self.card.effect_params["life_cost"] + -1
        if not 1 <= life <= self.player.ini_life:
            return self.scenario_skip()
        self.player.life = life
        return self.room.simulate_activate_ability(self.card)

    @simulate(evidence={'text': ('activate.effect', 'activate.fallback')})
    def simulate_activate_life_equal(self):
        self.scenario_prepare()
        life = self.card.effect_params["life_cost"] + 0
        if not 1 <= life <= self.player.ini_life:
            return self.scenario_skip()
        self.player.life = life
        return self.room.simulate_activate_ability(self.card)

    @simulate(evidence={'text': ('activate.effect',)})
    def simulate_activate_life_above(self):
        self.scenario_prepare()
        life = self.card.effect_params["life_cost"] + 1
        if not 1 <= life <= self.player.ini_life:
            return self.scenario_skip()
        self.player.life = life
        return self.room.simulate_activate_ability(self.card)

