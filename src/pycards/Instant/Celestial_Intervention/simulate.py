from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Celestial_Intervention.model import Celestial_Intervention


@bind_card(Celestial_Intervention)
class Celestial_Intervention_Simulation(Card_Simulation):
    text_parts = {
        "target.scope": [
            "Apply this to all creatures you control.",
            "Affect every creature on your battlefield.",
            "The following effect applies to all creatures under your control.",
            "Apply the effect to each creature you control.",
            "Give every creature on your side the following effect.",
            "All your creatures receive this effect.",
            "Affect each creature under your control with this effect.",
            "The effect applies to every creature you have in play.",
            "Apply the following effect to all creatures on your side.",
            "Give this effect to all creatures you control.",
        ],
        "protect.effect": [
            "It gains indestructible until its controller's end step.",
            "Give it indestructible until its controller's turn ends.",
            "The creature receives indestructible until the end of its controller's turn.",
            "Until its controller's turn ends, it has indestructible.",
            "Grant it indestructible through the rest of its controller's turn.",
            "It cannot be destroyed by a destruction effect until its controller's end step.",
            "The creature is protected from destruction until its controller's turn ends.",
            "Give the creature indestructible until its controller's end step occurs.",
            "It has the indestructible ability until the end step of its controller.",
            "The creature is granted indestructible until its controller's end step.",
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
        return self.scenario_cast()

    @simulate(evidence={'text': ('target.scope', 'protect.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_health_3(self):
        return self._protection_scene(0, 0, health=3)

    @simulate(evidence={'text': ('target.scope', 'protect.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_health_3(self):
        return self._protection_scene(1, 0, health=3)

    @simulate(evidence={'text': ('target.scope', 'protect.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_health_3(self):
        return self._protection_scene(0, 1, health=3)

    @simulate(evidence={'text': ('target.scope', 'protect.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_health_3(self):
        return self._protection_scene(1, 1, health=3)

    @simulate(evidence={'text': ('target.scope', 'protect.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_health_3(self):
        return self._protection_scene(3, 3, health=3)

    @simulate(evidence={'text': ('target.scope', 'protect.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_health_3(self):
        return self._protection_scene(0, 5, health=3)

    @simulate(evidence={'text': ('target.scope', 'protect.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_already_tapped(self):
        return self._protection_scene(3, 3, tapped=True)

    @simulate(evidence={'text': ('target.scope', 'protect.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_library_empty(self):
        return self._protection_scene(2, 2, library_count=0)

    @simulate(evidence={'text': ('target.scope', 'protect.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_library_short(self):
        return self._protection_scene(2, 2, library_count=max(0, self.card.effect_params["draw_count"] - 1))

    @simulate(evidence={'text': ('target.scope', 'protect.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_library_exact(self):
        return self._protection_scene(2, 2, library_count=self.card.effect_params["draw_count"])

