from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.land.Forest.model import Forest


@bind_card(Forest)
class Forest_Simulation(Card_Simulation):
    text_parts = {
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
    }

    @simulate(evidence={'fields': ('card_type',)})
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

    @simulate(evidence={'text': ('mana.effect',), 'fields': ('color_identity',)})
    def simulate_activate_mana(self):
        self.scenario_prepare()
        return self.room.simulate_activate_ability(self.card)

