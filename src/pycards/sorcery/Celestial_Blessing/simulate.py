from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.sorcery.Celestial_Blessing.model import Celestial_Blessing


@bind_card(Celestial_Blessing)
class Celestial_Blessing_Simulation(Card_Simulation):
    text_parts = {
        "target.scope": [
            "Choose a target creature you control.",
            "Target one of your creatures.",
            "Select a creature you control as the target.",
            "Choose one creature on your battlefield.",
            "Target a creature under your control.",
            "Choose one of your creatures as the target.",
            "Select a target from your own creatures.",
            "Target one creature on your side.",
            "Choose a creature under your control as the target.",
            "Select one creature on your battlefield as the target.",
        ],
        "lifelink.effect": [
            "Give the target lifelink, and also its first untapped adjacent creature in battlefield order if one exists, until your end step.",
            "Until your end step, the target and its first available untapped neighbor gain lifelink, preferring the left neighbor.",
            "The target gains lifelink until your turn ends, together with its left untapped neighbor or otherwise its right untapped neighbor.",
            "Grant lifelink until your end step to the target and the first untapped creature directly beside it in field order.",
            "The target and at most one untapped adjacent creature gain lifelink until your turn ends, choosing left before right.",
            "Give lifelink until your end step to the target and, if available, the first untapped neighbor in battlefield order.",
            "Grant the target lifelink through your turn, plus its untapped left neighbor or, if unavailable, its untapped right neighbor.",
            "Until your turn ends, give the chosen creature and its first untapped adjacent ally in field order lifelink.",
            "The target receives lifelink until your end step, along with the earliest untapped creature immediately beside it.",
            "Give lifelink until your end step to the target and one untapped neighboring creature, favoring the left one.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _protection_scene(self, own_count, enemy_count, role="self", selected_index=0, health=3, tapped=False, knight=False, creature_knight=False, library_count=None, time_count=0, stack_type="instant", own_stack=False):
        self.scenario_prepare()
        for owner, count in ((self.player, own_count), (self.player.opponent, enemy_count)):
            for index in range(count):
                creature = self.scenario_creature(owner, power=index + 1, health=health + index, flags={"tap": tapped, "Hexproof": owner is self.player.opponent and index % 2 == 0})
                if knight:
                    creature.type_card = "Human Knight"
                if creature_knight:
                    creature.type_creature = "Knight"
        if library_count is not None:
            self.room.env_initinal_library(self.player, {"instant_number": (library_count, library_count), "sorcery_number": (0, 0), "creature_number": (0, 0), "land_number": (0, 0)})
            self.player.library = [card for card in self.player.library if card.type == "Instant"][:library_count]
        subaction = 11 + selected_index if role == "self" else 1 + selected_index
        return self.scenario_cast((subaction,))

    @simulate(evidence={'text': ('target.scope', 'lifelink.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_tapped_False(self):
        return self._protection_scene(0, 0, tapped=False)

    @simulate(evidence={'text': ('target.scope', 'lifelink.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_tapped_True(self):
        return self._protection_scene(0, 0, tapped=True)

    @simulate(evidence={'text': ('target.scope', 'lifelink.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_tapped_False(self):
        return self._protection_scene(1, 0, tapped=False)

    @simulate(evidence={'text': ('target.scope', 'lifelink.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_tapped_True(self):
        return self._protection_scene(1, 0, tapped=True)

    @simulate(evidence={'text': ('target.scope', 'lifelink.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_2_tapped_False(self):
        return self._protection_scene(3, 2, tapped=False)

    @simulate(evidence={'text': ('target.scope', 'lifelink.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_2_tapped_True(self):
        return self._protection_scene(3, 2, tapped=True)

    @simulate(evidence={'text': ('target.scope', 'lifelink.effect'), 'fields': ('mana_cost',)})
    def simulate_wrong_owner(self):
        return self._protection_scene(0, 2, role="enemy")

    @simulate(evidence={'text': ('target.scope', 'lifelink.effect'), 'fields': ('mana_cost',)})
    def simulate_target_slot_0_tapped_False(self):
        return self._protection_scene(3, 1, selected_index=0, tapped=False)

    @simulate(evidence={'text': ('target.scope', 'lifelink.effect'), 'fields': ('mana_cost',)})
    def simulate_target_slot_0_tapped_True(self):
        return self._protection_scene(3, 1, selected_index=0, tapped=True)

    @simulate(evidence={'text': ('target.scope', 'lifelink.effect'), 'fields': ('mana_cost',)})
    def simulate_target_slot_1_tapped_False(self):
        return self._protection_scene(3, 1, selected_index=1, tapped=False)

    @simulate(evidence={'text': ('target.scope', 'lifelink.effect'), 'fields': ('mana_cost',)})
    def simulate_target_slot_1_tapped_True(self):
        return self._protection_scene(3, 1, selected_index=1, tapped=True)

    @simulate(evidence={'text': ('target.scope', 'lifelink.effect'), 'fields': ('mana_cost',)})
    def simulate_target_slot_2_tapped_False(self):
        return self._protection_scene(3, 1, selected_index=2, tapped=False)

    @simulate(evidence={'text': ('target.scope', 'lifelink.effect'), 'fields': ('mana_cost',)})
    def simulate_target_slot_2_tapped_True(self):
        return self._protection_scene(3, 1, selected_index=2, tapped=True)

