from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Honorable_Protection.model import Honorable_Protection


@bind_card(Honorable_Protection)
class Honorable_Protection_Simulation(Card_Simulation):
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
        "stats.condition": [
            "If Knight occurs in its card-type label,",
            "If its card type contains Knight,",
            "When Knight is included in the target's card type,",
            "If the target has Knight in its card-type text,",
            "If its card-type label includes Knight,",
            "When its card type has Knight as part of the label,",
            "If Knight appears in its card type,",
            "If the text Knight is in the target's card-type label,",
            "When the target's card type includes the word Knight,",
            "If its card-type text contains Knight,",
        ],
        "stats.effect": [
            "It permanently gets +{power_bonus}/+{toughness_bonus}.",
            "Give it a permanent +{power_bonus}/+{toughness_bonus} bonus.",
            "Its power permanently increases by {power_bonus} and health by {toughness_bonus}.",
            "Add {power_bonus} power and {toughness_bonus} health to it permanently.",
            "The creature receives a permanent +{power_bonus}/+{toughness_bonus} buff.",
            "Permanently grant it +{power_bonus}/+{toughness_bonus}.",
            "Increase its power by {power_bonus} and its health by {toughness_bonus} with no turn expiry.",
            "It gains an extra {power_bonus} power and {toughness_bonus} health permanently.",
            "Apply a permanent +{power_bonus}/+{toughness_bonus} bonus to that creature.",
            "The creature gets +{power_bonus}/+{toughness_bonus} without an end-step expiry.",
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

    @simulate(evidence={'text': ('target.scope', 'protect.effect', 'stats.condition', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_tapped_False(self):
        return self._protection_scene(0, 0, tapped=False)

    @simulate(evidence={'text': ('target.scope', 'protect.effect', 'stats.condition', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_tapped_True(self):
        return self._protection_scene(0, 0, tapped=True)

    @simulate(evidence={'text': ('target.scope', 'protect.effect', 'stats.condition', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_tapped_False(self):
        return self._protection_scene(1, 0, tapped=False)

    @simulate(evidence={'text': ('target.scope', 'protect.effect', 'stats.condition', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_tapped_True(self):
        return self._protection_scene(1, 0, tapped=True)

    @simulate(evidence={'text': ('target.scope', 'protect.effect', 'stats.condition', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_2_tapped_False(self):
        return self._protection_scene(3, 2, tapped=False)

    @simulate(evidence={'text': ('target.scope', 'protect.effect', 'stats.condition', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_2_tapped_True(self):
        return self._protection_scene(3, 2, tapped=True)

    @simulate(evidence={'text': ('target.scope', 'protect.effect', 'stats.condition', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_wrong_owner(self):
        return self._protection_scene(0, 2, role="enemy")

    @simulate(evidence={'text': ('target.scope', 'protect.effect', 'stats.condition', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_knight_card_type(self):
        return self._protection_scene(1, 0, knight=True, creature_knight=False)

    @simulate(evidence={'text': ('target.scope', 'protect.effect', 'stats.condition', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_knight_creature_type(self):
        return self._protection_scene(1, 0, knight=False, creature_knight=True)

    @simulate(evidence={'text': ('target.scope', 'protect.effect', 'stats.condition', 'stats.effect'), 'fields': ('mana_cost',)})
    def simulate_knight_both(self):
        return self._protection_scene(1, 0, knight=True, creature_knight=True)

