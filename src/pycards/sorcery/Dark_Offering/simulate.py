from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.sorcery.Dark_Offering.model import Dark_Offering


@bind_card(Dark_Offering)
class Dark_Offering_Simulation(Card_Simulation):
    text_parts = {
        "damage.effect": [
            "{card_name} deals {life_loss} damage to your opponent.",
            "Deal {life_loss} damage to the opposing player.",
            "Your opponent takes {life_loss} damage from {card_name}.",
            "{card_name} inflicts {life_loss} damage on your opponent.",
            "The opposing player is dealt {life_loss} damage.",
            "Hit your opponent for {life_loss} damage.",
            "Inflict {life_loss} damage on the opposing player.",
            "Deal your opponent an amount of damage equal to {life_loss}.",
            "{card_name} hits the opposing player for {life_loss} damage.",
            "Your opponent is dealt a total of {life_loss} damage.",
        ],
        "heal.effect": [
            "you gain {heal} life.",
            "gain {heal} life.",
            "you gain a total of {heal} life.",
            "gain a total of {heal} life.",
            "increase your life total by {heal}.",
            "you increase your life total by {heal}.",
            "restore {heal} life.",
            "you restore {heal} life.",
            "gain an amount of life equal to {heal}.",
            "you gain an amount of life equal to {heal}.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _drain_scene(self, life, opponent_life):
        self.scenario_prepare()
        if not (1 <= life <= self.player.ini_life and 1 <= opponent_life <= self.player.opponent.ini_life):
            return self.scenario_skip()
        self.player.life = life
        self.player.opponent.life = opponent_life
        return self.scenario_cast()

    @simulate(evidence={'text': ('damage.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_drain_injured_below_lethal(self):
        return self._drain_scene(1, self.card.effect_params["life_loss"] + -1)

    @simulate(evidence={'text': ('damage.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_drain_injured_equal_lethal(self):
        return self._drain_scene(1, self.card.effect_params["life_loss"] + 0)

    @simulate(evidence={'text': ('damage.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_drain_injured_above_lethal(self):
        return self._drain_scene(1, self.card.effect_params["life_loss"] + 1)

    @simulate(evidence={'text': ('damage.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_drain_exact_heal_below_lethal(self):
        return self._drain_scene(self.player.ini_life - self.card.effect_params["heal"], self.card.effect_params["life_loss"] + -1)

    @simulate(evidence={'text': ('damage.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_drain_exact_heal_equal_lethal(self):
        return self._drain_scene(self.player.ini_life - self.card.effect_params["heal"], self.card.effect_params["life_loss"] + 0)

    @simulate(evidence={'text': ('damage.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_drain_exact_heal_above_lethal(self):
        return self._drain_scene(self.player.ini_life - self.card.effect_params["heal"], self.card.effect_params["life_loss"] + 1)

    @simulate(evidence={'text': ('damage.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_drain_near_full_below_lethal(self):
        return self._drain_scene(self.player.ini_life - 1, self.card.effect_params["life_loss"] + -1)

    @simulate(evidence={'text': ('damage.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_drain_near_full_equal_lethal(self):
        return self._drain_scene(self.player.ini_life - 1, self.card.effect_params["life_loss"] + 0)

    @simulate(evidence={'text': ('damage.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_drain_near_full_above_lethal(self):
        return self._drain_scene(self.player.ini_life - 1, self.card.effect_params["life_loss"] + 1)

    @simulate(evidence={'text': ('damage.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_drain_full_below_lethal(self):
        return self._drain_scene(self.player.ini_life, self.card.effect_params["life_loss"] + -1)

    @simulate(evidence={'text': ('damage.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_drain_full_equal_lethal(self):
        return self._drain_scene(self.player.ini_life, self.card.effect_params["life_loss"] + 0)

    @simulate(evidence={'text': ('damage.effect', 'heal.effect'), 'fields': ('mana_cost',)})
    def simulate_drain_full_above_lethal(self):
        return self._drain_scene(self.player.ini_life, self.card.effect_params["life_loss"] + 1)

