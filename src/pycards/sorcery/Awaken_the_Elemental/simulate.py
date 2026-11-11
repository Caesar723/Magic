from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.sorcery.Awaken_the_Elemental.model import Awaken_the_Elemental


@bind_card(Awaken_the_Elemental)
class Awaken_the_Elemental_Simulation(Card_Simulation):
    text_parts = {
        "return.effect": [
            "Put a fresh copy of a random creature in your graveyard onto your battlefield, leaving the original in your graveyard.",
            "Choose a creature in your graveyard randomly and create a fresh battlefield copy, retaining the original graveyard card.",
            "Copy a random creature card from your graveyard onto your battlefield without moving the original.",
            "Create a fresh copy on your battlefield of a random graveyard creature you own, leaving that card in the graveyard.",
            "Randomly select a creature in your graveyard and put its fresh copy into play while keeping the original in the graveyard.",
            "Put a fresh battlefield copy of a randomly chosen creature from your graveyard into play and keep the original card there.",
            "If a creature is available in your graveyard, put a random one's fresh copy onto your battlefield and retain the original.",
            "Create a fresh battlefield copy from one random creature in your graveyard without removing that graveyard card.",
            "Choose a random creature card from your graveyard to copy onto your battlefield, preserving the original in the graveyard.",
            "Put a fresh copy of one randomly selected graveyard creature onto your battlefield while the original stays in your graveyard.",
        ],
        "return.stats": [
            "Give the copy {counter_count} temporary +{power_bonus}/+{toughness_bonus} buffs until your end step.",
            "The copy receives {counter_count} separate +{power_bonus}/+{toughness_bonus} buffs until your turn ends.",
            "Apply +{power_bonus}/+{toughness_bonus} to the copy {counter_count} times, expiring at your end step.",
            "Until your end step, the new copy gets +{power_bonus}/+{toughness_bonus} repeated {counter_count} times.",
            "Buff the copy by +{power_bonus}/+{toughness_bonus} for each of {counter_count} applications, until your turn ends.",
            "Grant {counter_count} copies of a +{power_bonus}/+{toughness_bonus} buff to that creature until your end step.",
            "Give the new creature {counter_count} temporary bonuses of +{power_bonus}/+{toughness_bonus} through your turn.",
            "The fresh creature gains +{power_bonus}/+{toughness_bonus} {counter_count} times until your end step.",
            "Until your turn ends, apply {counter_count} separate +{power_bonus}/+{toughness_bonus} bonuses to the copy.",
            "Add {counter_count} temporary buffs, each granting +{power_bonus}/+{toughness_bonus}, to the copy until your end step.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _recursion_scene(self, own_count, enemy_count=0, other_count=0, offset=0, colored=False, library_count=None, hand_count=0):
        self.scenario_prepare()
        self.player.graveyard.clear()
        self.player.opponent.graveyard.clear()
        self.player.hand.clear()
        self.player.opponent.hand.clear()
        for owner, count in ((self.player, own_count), (self.player.opponent, enemy_count)):
            for index in range(count):
                threshold = self.card.effect_params.get("mana_threshold", 2)
                cost = "W" * (threshold + offset + index + 1) if colored else str(max(0, threshold + offset + index))
                creature = self.scenario_creature(owner, power=index + 2, health=index + 3, flags={})
                creature.mana_cost = cost
                owner.remove_card(creature, "battlefield")
                owner.append_card(creature, "graveyard")
        for _ in range(other_count):
            self.player.append_card(self.card.copy_for_player(self.player), "graveyard")
        if library_count is not None:
            self.room.env_initinal_library(self.player, {"instant_number": (library_count, library_count), "sorcery_number": (0, 0), "creature_number": (0, 0), "land_number": (0, 0)})
            self.player.library = [card for card in self.player.library if card.type == "Instant"][:library_count]
        for _ in range(hand_count):
            self.player.append_card(self.card.copy_for_player(self.player), "hand")
        return self.scenario_cast()

    @simulate(evidence={'text': ('return.effect', 'return.stats'), 'fields': ('mana_cost',)})
    def simulate_graves_none(self):
        return self._recursion_scene(0, 0, 0)

    @simulate(evidence={'text': ('return.effect', 'return.stats'), 'fields': ('mana_cost',)})
    def simulate_graves_one_own(self):
        return self._recursion_scene(1, 0, 0)

    @simulate(evidence={'text': ('return.effect', 'return.stats'), 'fields': ('mana_cost',)})
    def simulate_graves_one_enemy(self):
        return self._recursion_scene(0, 1, 0)

    @simulate(evidence={'text': ('return.effect', 'return.stats'), 'fields': ('mana_cost',)})
    def simulate_graves_both(self):
        return self._recursion_scene(1, 1, 0)

    @simulate(evidence={'text': ('return.effect', 'return.stats'), 'fields': ('mana_cost',)})
    def simulate_graves_several(self):
        return self._recursion_scene(3, 3, 0)

    @simulate(evidence={'text': ('return.effect', 'return.stats'), 'fields': ('mana_cost',)})
    def simulate_graves_noncreatures(self):
        return self._recursion_scene(0, 0, 3)

    @simulate(evidence={'text': ('return.effect', 'return.stats'), 'fields': ('mana_cost',)})
    def simulate_graves_mixed(self):
        return self._recursion_scene(3, 3, 3)

