from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Monk_s_Inner_Rebound.model import Monk_s_Inner_Rebound


@bind_card(Monk_s_Inner_Rebound)
class Monk_s_Inner_Rebound_Simulation(Card_Simulation):
    scenario_locks={
        '_repeat_scene':('opponent.battlefield', 'opponent.land_area', 'self.battlefield'),
    }

    text_parts = {
        "counter.effect": [
            "Counter the nonland spell on top of the stack.",
            "Counter the top spell on the stack if it is not a land.",
            "Remove the top nonland spell from the stack without resolving it.",
            "Counter the nonland spell currently on top of the stack.",
            "Stop the top nonland spell on the stack from resolving.",
            "Counter the spell at the top of the stack, excluding lands.",
            "Cancel the nonland spell at the top of the stack.",
            "Counter the topmost spell on the stack if it is not a land.",
            "Prevent the nonland spell on top of the stack from resolving.",
            "Counter the current top spell on the stack, provided it is not a land.",
        ],
        "spell.condition": [
            "If the countered card is an instant other than a counterspell, or a sorcery,",
            "If that card is a noncounter instant or a sorcery,",
            "When the countered spell is a sorcery or an instant that is not a counterspell,",
            "If you countered a sorcery or an instant other than a counterspell,",
            "If the countered spell is an eligible instant or sorcery, excluding counterspells,",
            "When that countered card is a sorcery or noncounter instant,",
            "If that spell was a sorcery, or an instant that is not a counterspell,",
            "If the card you countered is a noncounter instant or sorcery,",
            "When a sorcery or a noncounter instant was countered,",
            "If the countered card belongs to the noncounter instant or sorcery types,",
        ],
        "spell.effect": [
            "create a copy under your control, prepare its effect with automatic target selection, and put that effect on the stack.",
            "make a copy for yourself, automatically prepare its effect, and add that effect to the stack.",
            "copy it for yourself and put its effect on the stack after preparing it with automatic targets.",
            "create your own copy, prepare its effect using automatic choices, and place the effect on the stack.",
            "put a copy's effect on the stack under your control after automatic target preparation.",
            "make a copy you control and automatically prepare its effect, then add that effect to the stack.",
            "create a copy for yourself, choose its targets automatically, and put its prepared effect on the stack.",
            "copy that card under your control and prepare its effect automatically before adding it to the stack.",
            "make a new copy for yourself and place its automatically prepared effect on the stack.",
            "create a copy controlled by you and put its effect on the stack with automatic target selection.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        self.scenario_stack()
        return self.scenario_cast(in_stack=True, provide_mana=False)

    def _repeat_scene(self, target_type, own_target=False):
        self.scenario_prepare()
        self.scenario_stack(target_type, own_target)
        self.room.env_mana(self.player.opponent, {"G": (1, 1)})
        for owner in (self.player, self.player.opponent):
            self.scenario_creature(owner, flags={})
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'spell.condition', 'spell.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant(self):
        return self._repeat_scene('instant', False)

    @simulate(evidence={'text': ('counter.effect', 'spell.condition', 'spell.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant(self):
        return self._repeat_scene('instant', True)

    @simulate(evidence={'text': ('counter.effect', 'spell.condition', 'spell.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery(self):
        return self._repeat_scene('sorcery', False)

    @simulate(evidence={'text': ('counter.effect', 'spell.condition', 'spell.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery(self):
        return self._repeat_scene('sorcery', True)

    @simulate(evidence={'text': ('counter.effect', 'spell.condition'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature(self):
        return self._repeat_scene('creature', False)

    @simulate(evidence={'text': ('counter.effect', 'spell.condition'), 'fields': ('mana_cost',)})
    def simulate_self_creature(self):
        return self._repeat_scene('creature', True)

