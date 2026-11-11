from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Mechanist_s_Disruption_Device.model import Mechanist_s_Disruption_Device


@bind_card(Mechanist_s_Disruption_Device)
class Mechanist_s_Disruption_Device_Simulation(Card_Simulation):
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
        "land.effect": [
            "If your hand contains a land afterward, move a random land from your hand into your land area.",
            "Then put one random land from your hand into your land area if any are available.",
            "After drawing, move one randomly selected hand land into your land area, if possible.",
            "If a land is in your hand after the draw, put one such land chosen at random into your land area.",
            "Then choose a land card from your hand at random and move it into your land area if one exists.",
            "If any hand lands remain after drawing, place one chosen at random in your land area.",
            "Next, put a randomly chosen land from your hand into your land area if your hand has one.",
            "Following the draw, move a random hand land into your land area when available.",
            "Then move one randomly selected land card from your hand to your land area, if any.",
            "If your hand has a land after drawing, a random one is moved into your land area.",
        ],
    }

    def _counter_scene(self, target_type="instant", own_target=False, cost=3, lower_count=0, library_count=5, hand_lands=0):
        self.scenario_prepare()
        self.scenario_stack(target_type, own_target, cost, lower_count=lower_count)
        self.room.env_initinal_library(self.player, {"instant_number": (library_count, library_count), "sorcery_number": (library_count, library_count), "creature_number": (0, 0), "land_number": (0, 0)})
        self.player.library = [card for card in self.player.library if card.type == 'Instant'][:library_count]
        self.room.env_initinal_hand(self.player, {"land_number": (hand_lands + 1, hand_lands + 1), "instant_number": (0, 0), "sorcery_number": (0, 0), "creature_number": (0, 0)})
        if not hand_lands:
            self.player.hand.clear()
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_empty_stack(self):
        self.scenario_prepare()
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_outside_response(self):
        self.scenario_prepare()
        self.scenario_stack()
        return self.scenario_cast()

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        self.scenario_stack()
        return self.scenario_cast(in_stack=True, provide_mana=False)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_land_on_stack(self):
        self.scenario_prepare()
        self.scenario_stack()
        self.room.env_mana(self.player.opponent, {"W": (1, 1)})
        self.room.stack[-1]["card"] = self.player.opponent.land_area[-1]
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_blocking_creature(self):
        self.scenario_prepare()
        self.scenario_stack("creature")
        self.room.attacker = self.scenario_creature(self.player, flags={})
        self.room.flag_dict["attacker_defenders"] = True
        return self.scenario_cast(in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_cost_0(self):
        return self._counter_scene('instant', False, 0)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_cost_1(self):
        return self._counter_scene('instant', False, 1)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_cost_3(self):
        return self._counter_scene('instant', False, 3)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_instant_cost_6(self):
        return self._counter_scene('instant', False, 6)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_cost_0(self):
        return self._counter_scene('instant', True, 0)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_cost_1(self):
        return self._counter_scene('instant', True, 1)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_cost_3(self):
        return self._counter_scene('instant', True, 3)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_self_instant_cost_6(self):
        return self._counter_scene('instant', True, 6)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_cost_0(self):
        return self._counter_scene('sorcery', False, 0)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_cost_1(self):
        return self._counter_scene('sorcery', False, 1)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_cost_3(self):
        return self._counter_scene('sorcery', False, 3)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_sorcery_cost_6(self):
        return self._counter_scene('sorcery', False, 6)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_cost_0(self):
        return self._counter_scene('sorcery', True, 0)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_cost_1(self):
        return self._counter_scene('sorcery', True, 1)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_cost_3(self):
        return self._counter_scene('sorcery', True, 3)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_self_sorcery_cost_6(self):
        return self._counter_scene('sorcery', True, 6)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_0(self):
        return self._counter_scene('creature', False, 0)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_1(self):
        return self._counter_scene('creature', False, 1)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_3(self):
        return self._counter_scene('creature', False, 3)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_creature_cost_6(self):
        return self._counter_scene('creature', False, 6)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_0(self):
        return self._counter_scene('creature', True, 0)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_1(self):
        return self._counter_scene('creature', True, 1)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_3(self):
        return self._counter_scene('creature', True, 3)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_self_creature_cost_6(self):
        return self._counter_scene('creature', True, 6)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_library_empty(self):
        return self._counter_scene(library_count=0)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_library_short(self):
        return self._counter_scene(library_count=max(0, self.card.effect_params["draw_count"] - 1))

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_library_exact(self):
        return self._counter_scene(library_count=self.card.effect_params["draw_count"])

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_library_plenty(self):
        return self._counter_scene(library_count=self.card.effect_params["draw_count"] + 3)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_hand_0_lands(self):
        return self._counter_scene(hand_lands=0)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_hand_1_lands(self):
        return self._counter_scene(hand_lands=1)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_hand_3_lands(self):
        return self._counter_scene(hand_lands=3)

    @simulate(evidence={'text': ('counter.effect', 'draw.effect', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_lower_stack_preserved(self):
        return self._counter_scene(lower_count=2)

