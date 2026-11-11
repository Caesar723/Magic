from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Mystic_Tide.model import Mystic_Tide
from pycards.land.Island.model import Island


@bind_card(Mystic_Tide)
class Mystic_Tide_Simulation(Card_Simulation):
    text_parts = {
        "counter.condition": [
            "If your opponent cannot pay {mana_threshold} generic mana from their available sources and the top spell belongs to your opponent,",
            "If {mana_threshold} generic mana is unaffordable for your opponent and the top spell belongs to your opponent,",
            "When your opponent lacks the resources to pay {mana_threshold} generic mana and the top spell belongs to your opponent,",
            "If the opponent cannot cover a cost of {mana_threshold} generic mana and the top spell belongs to your opponent,",
            "If your opponent does not have enough available resources for {mana_threshold} generic mana and the top spell belongs to your opponent,",
            "When the opponent cannot afford {mana_threshold} generic mana and the top spell belongs to your opponent,",
            "If your opponent cannot produce enough mana to pay {mana_threshold} generic mana and the top spell belongs to your opponent,",
            "If a generic mana cost of {mana_threshold} cannot be paid by your opponent and the top spell belongs to your opponent,",
            "When your opponent has insufficient resources to pay {mana_threshold} generic mana and the top spell belongs to your opponent,",
            "If your opponent's available mana sources cannot cover {mana_threshold} generic mana and the top spell belongs to your opponent,",
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
        "return.condition": [
            "If you also control a land named Island and your opponent still controls a creature after the counter,",
            "When a land named Island is under your control and an opposing creature remains after countering,",
            "If you have a land named Island and there is an opposing creature left after the counter,",
            "If a land called Island is among your lands and an opposing creature is still present,",
            "When you control an Island-named land and your opponent has a creature remaining,",
            "If your land area includes a land named Island and your opponent still has a creature,",
            "If you control a land whose name is Island and an opposing creature remains available,",
            "When a land with the name Island is on your side and an opposing creature remains in play,",
            "If you have an Island-named land and your opponent retains a creature after the counter,",
            "If a land named Island is under your control and your opponent still has at least one creature,",
        ],
        "return.effect": [
            "remove a random opposing creature from the battlefield and add a fresh copy to its owner's hand.",
            "choose an opposing creature at random, remove it from play, and put a copy into its owner's hand.",
            "pick a random opposing creature and replace its battlefield object with a fresh copy in its owner's hand.",
            "move a random opposing creature out of the battlefield and create a copy in its owner's hand.",
            "remove one randomly selected opposing creature from play and give its owner a copy in hand.",
            "choose a random opposing creature, take it off the battlefield, and create its copy in its owner's hand.",
            "put a fresh copy of a random opposing creature into its owner's hand and remove the original from the battlefield.",
            "pick one opposing creature at random, remove it from the battlefield, and add a copy to its owner's hand.",
            "remove a randomly chosen opposing creature from play and place a new copy in its owner's hand.",
            "choose one opposing creature randomly and take it out of play, putting a fresh copy in its owner's hand.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        self.scenario_stack()
        return self.scenario_cast(in_stack=True, provide_mana=False)

    def _bounce_scene(self, count, has_island, mana_offset, own_target=False, target_type="instant", enemy_lands=0):
        self.scenario_prepare()
        self.scenario_stack(target_type, own_target)
        for _ in range(count):
            self.scenario_creature(self.player.opponent, flags={})
        if has_island:
            self.stage_card(Island(self.player), zone="land_area")
        self.player.opponent.mana["colorless"] = max(0, self.card.effect_params["mana_threshold"] + mana_offset)
        if enemy_lands:
            self.room.env_mana(self.player.opponent, {"G": (enemy_lands, enemy_lands)})
        self.player.mana.update(self.card.calculate_cost())
        return self.scenario_cast(in_stack=True, provide_mana=False)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'return.condition'), 'fields': ('mana_cost',)})
    def simulate_0_creatures_no_island_below_mana(self):
        return self._bounce_scene(0, False, -1)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'return.condition'), 'fields': ('mana_cost',)})
    def simulate_0_creatures_no_island_equal_mana(self):
        return self._bounce_scene(0, False, 0)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'return.condition'), 'fields': ('mana_cost',)})
    def simulate_0_creatures_no_island_above_mana(self):
        return self._bounce_scene(0, False, 1)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'return.condition'), 'fields': ('mana_cost',)})
    def simulate_0_creatures_island_below_mana(self):
        return self._bounce_scene(0, True, -1)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'return.condition'), 'fields': ('mana_cost',)})
    def simulate_0_creatures_island_equal_mana(self):
        return self._bounce_scene(0, True, 0)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'return.condition'), 'fields': ('mana_cost',)})
    def simulate_0_creatures_island_above_mana(self):
        return self._bounce_scene(0, True, 1)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'return.condition'), 'fields': ('mana_cost',)})
    def simulate_1_creatures_no_island_below_mana(self):
        return self._bounce_scene(1, False, -1)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'return.condition'), 'fields': ('mana_cost',)})
    def simulate_1_creatures_no_island_equal_mana(self):
        return self._bounce_scene(1, False, 0)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'return.condition'), 'fields': ('mana_cost',)})
    def simulate_1_creatures_no_island_above_mana(self):
        return self._bounce_scene(1, False, 1)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'return.condition', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_1_creatures_island_below_mana(self):
        return self._bounce_scene(1, True, -1)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'return.condition'), 'fields': ('mana_cost',)})
    def simulate_1_creatures_island_equal_mana(self):
        return self._bounce_scene(1, True, 0)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'return.condition'), 'fields': ('mana_cost',)})
    def simulate_1_creatures_island_above_mana(self):
        return self._bounce_scene(1, True, 1)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'return.condition'), 'fields': ('mana_cost',)})
    def simulate_3_creatures_no_island_below_mana(self):
        return self._bounce_scene(3, False, -1)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'return.condition'), 'fields': ('mana_cost',)})
    def simulate_3_creatures_no_island_equal_mana(self):
        return self._bounce_scene(3, False, 0)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'return.condition'), 'fields': ('mana_cost',)})
    def simulate_3_creatures_no_island_above_mana(self):
        return self._bounce_scene(3, False, 1)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'return.condition', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_3_creatures_island_below_mana(self):
        return self._bounce_scene(3, True, -1)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'return.condition'), 'fields': ('mana_cost',)})
    def simulate_3_creatures_island_equal_mana(self):
        return self._bounce_scene(3, True, 0)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'return.condition'), 'fields': ('mana_cost',)})
    def simulate_3_creatures_island_above_mana(self):
        return self._bounce_scene(3, True, 1)

    @simulate(evidence={'text': ('counter.condition',), 'fields': ('mana_cost',)})
    def simulate_own_spell(self):
        return self._bounce_scene(3, True, -1, own_target=True)

    @simulate(evidence={'text': ('counter.condition', 'counter.effect', 'return.condition', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_counter_only_creature(self):
        return self._bounce_scene(0, True, -1, target_type="creature")

    @simulate(evidence={'text': ('counter.condition',), 'fields': ('mana_cost',)})
    def simulate_opponent_available_land_mana(self):
        return self._bounce_scene(3, True, -1, enemy_lands=self.card.effect_params["mana_threshold"])

