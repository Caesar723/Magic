from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Phantom_Shield.model import Phantom_Shield


@bind_card(Phantom_Shield)
class Phantom_Shield_Simulation(Card_Simulation):
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
            "Prevent all damage to it until its controller's end step.",
            "It takes no damage until its controller's turn ends.",
            "All damage dealt to it is prevented until its controller's end step.",
            "Until its controller's turn ends, prevent damage dealt to it.",
            "It is protected from all incoming damage until its controller's end step.",
            "Damage to that creature is reduced to zero until its controller's turn ends.",
            "No damage can be dealt to it before its controller's end step.",
            "Prevent incoming damage to that creature until the end step of its controller.",
            "It receives damage prevention until its controller's end step.",
            "All damage it would receive becomes zero until its controller's turn ends.",
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

    @simulate(evidence={'text': ('target.scope', 'protect.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_health_3(self):
        return self._protection_scene(0, 0, health=3)

    @simulate(evidence={'text': ('target.scope', 'protect.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_health_3(self):
        return self._protection_scene(1, 0, health=3)

    @simulate(evidence={'text': ('target.scope', 'protect.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_health_3(self):
        return self._protection_scene(0, 1, health=3)

    @simulate(evidence={'text': ('target.scope', 'protect.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_health_3(self):
        return self._protection_scene(1, 1, health=3)

    @simulate(evidence={'text': ('target.scope', 'protect.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_health_3(self):
        return self._protection_scene(3, 3, health=3)

    @simulate(evidence={'text': ('target.scope', 'protect.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_health_3(self):
        return self._protection_scene(0, 5, health=3)

    @simulate(evidence={'text': ('target.scope', 'protect.effect'), 'fields': ('mana_cost',)})
    def simulate_already_tapped(self):
        return self._protection_scene(3, 3, tapped=True)

