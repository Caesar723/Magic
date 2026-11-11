from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.land.Luminous_Glade.model import Luminous_Glade


@bind_card(Luminous_Glade)
class Luminous_Glade_Simulation(Card_Simulation):
    scenario_locks={
        'simulate_enter_land_limit':('self.hand',),
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
            "Manual activation taps this land and heals up to {prevent_damage} damage from the next positive damage event to a creature or player before your turn ends.",
            "When manually activated, tap this land and restore up to {prevent_damage} damage from the next damage event to any creature or player before your turn ends.",
            "On manual activation, this land taps and restores at most {prevent_damage} damage from the next positive damage event before your turn ends.",
            "Manually activating it taps it and heals up to {prevent_damage} damage to the creature or player that next takes positive damage before your turn ends.",
            "When activated manually, it taps and heals at most {prevent_damage} of the next positive damage dealt to a creature or player before your turn ends.",
            "A manual activation taps this land and restores up to {prevent_damage} of the next damage event suffered by any creature or player before your turn ends.",
            "Manual activation taps it and restores at most {prevent_damage} damage from the next positive hit to any creature or player before your turn ends.",
            "Tap this land on manual activation to heal up to {prevent_damage} damage from the next positive damage event to a creature or player before your turn ends.",
            "On being manually activated, it taps and heals up to {prevent_damage} of the damage in the next positive damage event before your turn ends.",
            "Activate manually to tap this land and restore at most {prevent_damage} of the next positive damage to any creature or player before your turn ends.",
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

    @simulate(evidence={'text': ('activate.effect',)})
    def simulate_activate_next_damage(self):
        self.scenario_prepare()
        return self.room.simulate_activate_ability(self.card)

