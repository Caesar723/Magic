from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Roar_of_the_Behemoth.model import Roar_of_the_Behemoth


@bind_card(Roar_of_the_Behemoth)
class Roar_of_the_Behemoth_Simulation(Card_Simulation):
    scenario_locks={
        '_protection_scene':('opponent.battlefield', 'self.battlefield', 'self.library'),
    }

    text_parts = {
        "target.scope": [
            "Apply this to all creatures your opponent controls.",
            "Affect every creature on your opponent's battlefield.",
            "The following effect applies to all creatures under your opponent's control.",
            "Apply the effect to each creature your opponent controls.",
            "Give every creature on your opponent's side the following effect.",
            "All opposing creatures receive this effect.",
            "Affect each creature under your opponent's control with this effect.",
            "The effect applies to every creature your opponent has in play.",
            "Apply the following effect to all creatures on your opponent's side.",
            "Give this effect to all creatures your opponent controls.",
        ],
        "stats.effect": [
            "Set its power to {power_set} until your end step.",
            "Its power becomes {power_set} until your turn ends.",
            "Give it exactly {power_set} power until the end of your turn.",
            "Until your end step, its power is {power_set}.",
            "Replace its current power with {power_set} until your turn ends.",
            "Make its power equal to {power_set} until your end step.",
            "The creature has {power_set} power until the end of your turn.",
            "Its power is overridden to {power_set} until your end step.",
            "Until your turn ends, use {power_set} as its power.",
            "Force its power to be {power_set} until your end step.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _protection_scene(self,own_count,enemy_count,health=3,tapped=False,knight=False,creature_knight=False,library_count=None):
        library_count=self.scenario_count("library",library_count)
        self.scenario_prepare()
        for owner, count in ((self.player, own_count), (self.player.opponent, enemy_count)):
            for index in range(count):
                creature = self.scenario_creature(owner, power=index + 1, health=health + index, flags={"tap": tapped, "Hexproof": owner is self.player.opponent and index % 2 == 0})
                if knight:
                    creature.type_card = "Human Knight"
                if creature_knight:
                    creature.type_creature = "Knight"
        if library_count is not None:
            self.scenario_replace_cards(self.player,"library",instant=(library_count, library_count))
            self.player.library = [card for card in self.player.library if card.type == "Instant"][:library_count]
        return self.scenario_cast()

    @simulate(evidence={'text': ('target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_health_3(self):
        return self._protection_scene(0,0,health=3)

    @simulate(evidence={'text': ('target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_health_3(self):
        return self._protection_scene(1,0,health=3)

    @simulate(evidence={'text': ('target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_health_3(self):
        return self._protection_scene(0,1,health=3)

    @simulate(evidence={'text': ('target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_health_3(self):
        return self._protection_scene(1,1,health=3)

    @simulate(evidence={'text': ('target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_health_3(self):
        return self._protection_scene(3,3,health=3)

    @simulate(evidence={'text': ('target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_health_3(self):
        return self._protection_scene(0,5,health=3)

    @simulate(evidence={'text': ('target.scope', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_already_tapped(self):
        return self._protection_scene(3,3,tapped=True)

