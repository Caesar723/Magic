from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Aquatic_Evasion.model import Aquatic_Evasion


@bind_card(Aquatic_Evasion)
class Aquatic_Evasion_Simulation(Card_Simulation):
    text_parts = {
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
        "protect.effect": [
            "It gains hexproof until its controller's end step.",
            "Give it hexproof until its controller's turn ends.",
            "The creature receives hexproof until the end of its controller's turn.",
            "Until its controller's turn ends, it has hexproof.",
            "Grant it hexproof through the rest of its controller's turn.",
            "It cannot be targeted by opposing spells or abilities until its controller's end step.",
            "The creature is protected from targeting by opposing spells or abilities until its controller's turn ends.",
            "Give the creature hexproof until its controller's end step occurs.",
            "It has the hexproof ability until the end step of its controller.",
            "The creature is granted hexproof until its controller's end step.",
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

    @simulate(evidence={'text': ('draw.effect', 'target.scope', 'protect.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_tapped_False(self):
        return self._protection_scene(0, 0, tapped=False)

    @simulate(evidence={'text': ('draw.effect', 'target.scope', 'protect.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_tapped_True(self):
        return self._protection_scene(0, 0, tapped=True)

    @simulate(evidence={'text': ('draw.effect', 'target.scope', 'protect.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_tapped_False(self):
        return self._protection_scene(1, 0, tapped=False)

    @simulate(evidence={'text': ('draw.effect', 'target.scope', 'protect.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_tapped_True(self):
        return self._protection_scene(1, 0, tapped=True)

    @simulate(evidence={'text': ('draw.effect', 'target.scope', 'protect.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_2_tapped_False(self):
        return self._protection_scene(3, 2, tapped=False)

    @simulate(evidence={'text': ('draw.effect', 'target.scope', 'protect.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_2_tapped_True(self):
        return self._protection_scene(3, 2, tapped=True)

    @simulate(evidence={'text': ('draw.effect', 'target.scope', 'protect.effect'), 'fields': ('mana_cost',)})
    def simulate_wrong_owner(self):
        return self._protection_scene(0, 2, role="enemy")

    @simulate(evidence={'text': ('draw.effect', 'target.scope', 'protect.effect'), 'fields': ('mana_cost',)})
    def simulate_library_empty(self):
        return self._protection_scene(2, 2, library_count=0)

    @simulate(evidence={'text': ('draw.effect', 'target.scope', 'protect.effect'), 'fields': ('mana_cost',)})
    def simulate_library_short(self):
        return self._protection_scene(2, 2, library_count=max(0, self.card.effect_params["draw_count"] - 1))

    @simulate(evidence={'text': ('draw.effect', 'target.scope', 'protect.effect'), 'fields': ('mana_cost',)})
    def simulate_library_exact(self):
        return self._protection_scene(2, 2, library_count=self.card.effect_params["draw_count"])

