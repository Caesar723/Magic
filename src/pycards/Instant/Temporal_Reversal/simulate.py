from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.land.Plains.model import Plains
from pycards.Instant.Temporal_Reversal.model import Temporal_Reversal


@bind_card(Temporal_Reversal)
class Temporal_Reversal_Simulation(Card_Simulation):
    scenario_locks={
        '_return_scene':('opponent.battlefield', 'opponent.land_area', 'self.battlefield', 'self.land_area', 'self.library'),
    }

    text_parts = {
        "return.effect": [
            "Return the selected creature to its owner's hand.",
            "Put the target creature into its owner's hand.",
            "The chosen creature returns to its owner's hand.",
            "Move that creature from the battlefield to its owner's hand.",
            "Return the creature you targeted to the hand of its owner.",
            "Put that creature back into its owner's hand.",
            "The targeted creature goes back to its owner's hand.",
            "Return your chosen creature from play to its owner's hand.",
            "Take that creature off the battlefield and put it into its owner's hand.",
            "Move the targeted creature back to its owner's hand.",
        ],
        "untap.effect": [
            "Then untap the first {untap_count} tapped land{untap_count_plural} you control, or all of them if fewer.",
            "Untap up to {untap_count} of your tapped lands in battlefield order.",
            "Afterward, untap your earliest {untap_count} tapped land{untap_count_plural}, taking all if fewer exist.",
            "Untap the first available {untap_count} tapped land{untap_count_plural} on your side.",
            "Then untap as many as {untap_count} of your tapped lands, starting from the first.",
            "In your land order, untap the first {untap_count} tapped land{untap_count_plural} available.",
            "Untap your tapped lands in order until {untap_count} have been untapped or none remain.",
            "Following the return, untap up to {untap_count} of your tapped lands in order.",
            "Next, untap the first {untap_count} tapped land{untap_count_plural} you have, if available.",
            "Go through your lands in order and untap up to {untap_count} that are tapped.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _return_scene(self, role, tapped=0, library_count=None, flags=None):
        library_count=self.scenario_count("library",library_count)
        self.scenario_prepare()
        for index in range(tapped + 1):
            land = Plains(self.player)
            if index < tapped:
                self.scenario_tapped(land)
            self.stage_card(land, zone="land_area")
        if library_count is not None:
            self.scenario_replace_cards(self.player,"library",instant=(library_count, library_count))
            self.player.library = [card for card in self.player.library if card.type == "Instant"][:library_count]
        subaction = 0
        if role in ("self", "enemy"):
            owner = self.player if role == "self" else self.player.opponent
            target = self.scenario_creature(owner, power=2, health=4, flags=flags or {})
            target.actual_live = 2
            subaction = 11 if role == "self" else 1
        elif role == "player":
            subaction = 21
        self.player.mana.update(self.card.calculate_cost())
        return self.scenario_cast((subaction,), provide_mana=False)

    @simulate(evidence={'text': ('return.effect', 'untap.effect'), 'fields': ('mana_cost',)})
    def simulate_return_self(self):
        return self._return_scene('self')

    @simulate(evidence={'text': ('return.effect', 'untap.effect'), 'fields': ('mana_cost',)})
    def simulate_return_enemy(self):
        return self._return_scene('enemy')

    @simulate(evidence={'text': ('return.effect', 'untap.effect'), 'fields': ('mana_cost',)})
    def simulate_return_none(self):
        return self._return_scene('none')

    @simulate(evidence={'text': ('return.effect', 'untap.effect'), 'fields': ('mana_cost',)})
    def simulate_return_player(self):
        return self._return_scene('player')

    @simulate(evidence={'text': ('return.effect', 'untap.effect'), 'fields': ('mana_cost',)})
    def simulate_self_hexproof(self):
        return self._return_scene('self', flags={'Hexproof': True})

    @simulate(evidence={'text': ('return.effect', 'untap.effect'), 'fields': ('mana_cost',)})
    def simulate_self_tap(self):
        return self._return_scene('self', flags={'tap': True})

    @simulate(evidence={'text': ('return.effect', 'untap.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_hexproof(self):
        return self._return_scene('enemy', flags={'Hexproof': True})

    @simulate(evidence={'text': ('return.effect', 'untap.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_tap(self):
        return self._return_scene('enemy', flags={'tap': True})

    @simulate(evidence={'text': ('return.effect', 'untap.effect'), 'fields': ('mana_cost',)})
    def simulate_tapped_none(self):
        return self._return_scene("enemy", tapped=0)

    @simulate(evidence={'text': ('return.effect', 'untap.effect'), 'fields': ('mana_cost',)})
    def simulate_tapped_short(self):
        return self._return_scene("enemy", tapped=max(0, self.card.effect_params["untap_count"] - 1))

    @simulate(evidence={'text': ('return.effect', 'untap.effect'), 'fields': ('mana_cost',)})
    def simulate_tapped_exact(self):
        return self._return_scene("enemy", tapped=self.card.effect_params["untap_count"])

    @simulate(evidence={'text': ('return.effect', 'untap.effect'), 'fields': ('mana_cost',)})
    def simulate_tapped_plenty(self):
        return self._return_scene("enemy", tapped=self.card.effect_params["untap_count"] + 2)

