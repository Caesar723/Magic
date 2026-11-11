from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Mindweave.model import Mindweave


@bind_card(Mindweave)
class Mindweave_Simulation(Card_Simulation):
    text_parts = {
        "counter.condition": [
            "If your opponent cannot pay {mana_threshold} generic mana from their available sources,",
            "If {mana_threshold} generic mana is unaffordable for your opponent,",
            "When your opponent lacks the resources to pay {mana_threshold} generic mana,",
            "If the opponent cannot cover a cost of {mana_threshold} generic mana,",
            "If your opponent does not have enough available resources for {mana_threshold} generic mana,",
            "When the opponent cannot afford {mana_threshold} generic mana,",
            "If your opponent cannot produce enough mana to pay {mana_threshold} generic mana,",
            "If a generic mana cost of {mana_threshold} cannot be paid by your opponent,",
            "When your opponent has insufficient resources to pay {mana_threshold} generic mana,",
            "If your opponent's available mana sources cannot cover {mana_threshold} generic mana,",
        ],
        "counter.effect": [
            "counter the nonland spell on top of the stack.",
            "counter the top spell on the stack if it is not a land.",
            "remove the top nonland spell from the stack without resolving it.",
            "counter the nonland spell currently on top of the stack.",
            "stop the top nonland spell on the stack from resolving.",
            "counter the spell at the top of the stack, excluding lands.",
            "cancel the nonland spell at the top of the stack.",
            "counter the topmost spell on the stack if it is not a land.",
            "prevent the nonland spell on top of the stack from resolving.",
            "counter the current top spell on the stack, provided it is not a land.",
        ],
        "draw.effect": [
            "Draw {draw_count} card{draw_count_plural}.",
            "Draw {draw_count_word} card{draw_count_plural}.",
            "Take the top {draw_count} card{draw_count_plural} of your library into your hand.",
            "Put the top {draw_count} card{draw_count_plural} from your library into your hand.",
            "Add the top {draw_count} card{draw_count_plural} of your library to your hand.",
            "You draw {draw_count} card{draw_count_plural}.",
            "Draw a total of {draw_count} card{draw_count_plural}.",
            "You draw a total of {draw_count_word} card{draw_count_plural}.",
            "Take {draw_count} card{draw_count_plural} from the top of your library into your hand.",
            "Put {draw_count} card{draw_count_plural} from the top of your library into your hand.",
        ],
    }

    def _counter_scene(self, target_type="instant", own_target=False, cost=3, lower_count=0, library_count=5, mana_offset=-1, extra_lands=0):
        self.scenario_prepare()
        self.scenario_stack(target_type, own_target, cost, lower_count=lower_count)
        self.room.env_initinal_library(self.player, {"instant_number": (library_count, library_count), "sorcery_number": (library_count, library_count), "creature_number": (0, 0), "land_number": (0, 0)})
        self.player.library = [card for card in self.player.library if card.type == 'Instant'][:library_count]
        self.player.opponent.mana["colorless"] = max(0, self.card.effect_params["mana_threshold"] + mana_offset)
        if extra_lands:
            self.room.env_mana(self.player.opponent, {"G": (extra_lands, extra_lands)})
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_empty_stack(self):
        self.scenario_prepare()
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_outside_response(self):
        self.scenario_prepare()
        self.scenario_stack()
        return self.scenario_cast()

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        self.scenario_stack()
        return self.scenario_cast(in_stack=True, provide_mana=False)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_land_on_stack(self):
        self.scenario_prepare()
        self.scenario_stack()
        self.room.env_mana(self.player.opponent, {"W": (1, 1)})
        self.room.stack[-1]["card"] = self.player.opponent.land_area[-1]
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_blocking_creature(self):
        self.scenario_prepare()
        self.scenario_stack("creature")
        self.room.attacker = self.scenario_creature(self.player, flags={})
        self.room.flag_dict["attacker_defenders"] = True
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_cost_0(self):
        return self._counter_scene('instant', False, 0)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_cost_1(self):
        return self._counter_scene('instant', False, 1)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_cost_3(self):
        return self._counter_scene('instant', False, 3)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_cost_6(self):
        return self._counter_scene('instant', False, 6)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_cost_0(self):
        return self._counter_scene('instant', True, 0)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_cost_1(self):
        return self._counter_scene('instant', True, 1)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_cost_3(self):
        return self._counter_scene('instant', True, 3)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_cost_6(self):
        return self._counter_scene('instant', True, 6)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_cost_0(self):
        return self._counter_scene('sorcery', False, 0)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_cost_1(self):
        return self._counter_scene('sorcery', False, 1)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_cost_3(self):
        return self._counter_scene('sorcery', False, 3)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_cost_6(self):
        return self._counter_scene('sorcery', False, 6)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_cost_0(self):
        return self._counter_scene('sorcery', True, 0)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_cost_1(self):
        return self._counter_scene('sorcery', True, 1)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_cost_3(self):
        return self._counter_scene('sorcery', True, 3)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_cost_6(self):
        return self._counter_scene('sorcery', True, 6)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_0(self):
        return self._counter_scene('creature', False, 0)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_1(self):
        return self._counter_scene('creature', False, 1)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_3(self):
        return self._counter_scene('creature', False, 3)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_6(self):
        return self._counter_scene('creature', False, 6)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_0(self):
        return self._counter_scene('creature', True, 0)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_1(self):
        return self._counter_scene('creature', True, 1)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_3(self):
        return self._counter_scene('creature', True, 3)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_6(self):
        return self._counter_scene('creature', True, 6)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_library_empty(self):
        return self._counter_scene(library_count=0)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_library_short(self):
        return self._counter_scene(library_count=max(0, self.card.effect_params["draw_count"] - 1))

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_library_exact(self):
        return self._counter_scene(library_count=self.card.effect_params["draw_count"])

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_library_plenty(self):
        return self._counter_scene(library_count=self.card.effect_params["draw_count"] + 3)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_mana_below_enemy_spell(self):
        return self._counter_scene(own_target=False, mana_offset=-1)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_mana_below_self_spell(self):
        return self._counter_scene(own_target=True, mana_offset=-1)

    @simulate(evidence={'text': ('counter.condition',), 'fields': ('mana_cost',)})
    def simulate_mana_equal_enemy_spell(self):
        return self._counter_scene(own_target=False, mana_offset=0)

    @simulate(evidence={'text': ('counter.condition',), 'fields': ('mana_cost',)})
    def simulate_mana_equal_self_spell(self):
        return self._counter_scene(own_target=True, mana_offset=0)

    @simulate(evidence={'text': ('counter.condition',), 'fields': ('mana_cost',)})
    def simulate_mana_above_enemy_spell(self):
        return self._counter_scene(own_target=False, mana_offset=1)

    @simulate(evidence={'text': ('counter.condition',), 'fields': ('mana_cost',)})
    def simulate_mana_above_self_spell(self):
        return self._counter_scene(own_target=True, mana_offset=1)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_mana_available_in_lands(self):
        return self._counter_scene(mana_offset=-1, extra_lands=self.card.effect_params["mana_threshold"])

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_lower_stack_preserved(self):
        return self._counter_scene(lower_count=2)

