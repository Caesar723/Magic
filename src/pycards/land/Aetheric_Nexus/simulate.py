from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.land.Aetheric_Nexus.model import Aetheric_Nexus


@bind_card(Aetheric_Nexus)
class Aetheric_Nexus_Simulation(Card_Simulation):
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
            "It also adds {mana_amount} colorless mana when it enters the battlefield.",
            "Its entry also adds {mana_amount} colorless mana to your mana pool.",
            "On entering the battlefield, it also produces {mana_amount} colorless mana.",
            "When it enters play, add {mana_amount} colorless mana to your mana pool.",
            "Its entry produces {mana_amount} colorless mana for you.",
            "Entering the battlefield also gives you {mana_amount} colorless mana.",
            "When this land enters the battlefield, add {mana_amount} colorless mana.",
            "Add {mana_amount} colorless mana to your pool when this land enters play.",
            "As this land enters play, it adds {mana_amount} colorless mana to your pool.",
            "On entry, you also receive {mana_amount} colorless mana.",
        ],
        "mana.effect": [
            "Tap this land to add {mana_amount} colorless mana.",
            "You may tap {card_name} to add {mana_amount} colorless mana to your pool.",
            "Tap {card_name} to produce {mana_amount} colorless mana.",
            "Tapping this land for mana adds {mana_amount} colorless mana.",
            "This land can be tapped for {mana_amount} colorless mana.",
            "You may tap this land for {mana_amount} colorless mana.",
            "Tap it for mana to add {mana_amount} colorless mana to your mana pool.",
            "By tapping {card_name} for mana, you gain {mana_amount} colorless mana.",
            "You can tap this land to produce {mana_amount} colorless mana.",
            "{card_name} can produce {mana_amount} colorless mana when tapped for mana.",
        ],
        "activate.condition": [
            "It can be activated only while you control a creature.",
            "You can activate it only if you have a creature on the battlefield.",
            "Its activation requires at least one creature on your battlefield.",
            "Activate it only when you control at least one creature.",
            "This ability is available only if you control a creature.",
            "This land can produce mana only while a creature is on your side.",
            "You need a creature on your battlefield to activate this land.",
            "An activation is allowed only if you control one or more creatures.",
            "You may activate it only with a creature under your control.",
            "The mana ability requires you to control a creature.",
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

    @simulate(evidence={'text': ('activate.condition', 'mana.effect'), 'fields': ('color_identity',)})
    def simulate_activate_0_creatures(self):
        self.scenario_prepare()
        for _ in range(0):
            self.scenario_creature(self.player, flags={})
        return self.room.simulate_activate_ability(self.card)

    @simulate(evidence={'text': ('activate.condition', 'mana.effect'), 'fields': ('color_identity',)})
    def simulate_activate_1_creatures(self):
        self.scenario_prepare()
        for _ in range(1):
            self.scenario_creature(self.player, flags={})
        return self.room.simulate_activate_ability(self.card)

    @simulate(evidence={'text': ('activate.condition', 'mana.effect'), 'fields': ('color_identity',)})
    def simulate_activate_3_creatures(self):
        self.scenario_prepare()
        for _ in range(3):
            self.scenario_creature(self.player, flags={})
        return self.room.simulate_activate_ability(self.card)

