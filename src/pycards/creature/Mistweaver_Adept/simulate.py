from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Mistweaver_Adept.model import Mistweaver_Adept


@bind_card(Mistweaver_Adept)
class Mistweaver_Adept_Simulation(Card_Simulation):
    scenario_locks={
        '_enter_scene':('opponent.battlefield', 'self.battlefield', 'self.hand', 'self.land_area'),
    }

    text_parts = {
        "enter.trigger": [
            "When {card_name} enters the battlefield,",
            "Whenever {card_name} enters the battlefield,",
            "When this creature enters the battlefield,",
            "Whenever this creature enters the battlefield,",
            "When {card_name} enters play,",
            "Whenever {card_name} enters play,",
            "When this creature enters play,",
            "Whenever this creature enters play,",
            "When {card_name} comes into play,",
            "Whenever {card_name} comes into play,",
        ],
        "enter.option": [
            "You may choose to use this ability.",
            "You can choose whether to use this ability.",
            "You may accept or decline the following ability.",
            "Using this ability is optional.",
            "Choose whether to use the following effect.",
            "You may opt into the following ability.",
            "You can decline this ability or use it.",
            "Accepting the following ability is optional.",
            "You may decide to perform the following effect.",
            "You may use this ability or do nothing.",
        ],
        "enter.effect": [
            "Return the selected creature to its owner's hand.",
            "Put the target creature into its owner's hand.",
            "The chosen creature returns to its owner's hand.",
            "Move that creature from the battlefield to its owner's hand.",
            "Return the creature you targeted to the hand of its owner.",
            "Put that creature back into its owner's hand.",
            "The targeted creature goes back to its owner's hand.",
            "Return your chosen creature from play to its owner's hand.",
            "Take that creature off the battlefield and put it into its owner's hand.",
            "Move the targeted creature back to its owner's hand.",
        ],
        "enter.scry": [
            "If the creature was returned, scry {scry_count}.",
            "After returning that creature, scry {scry_count}.",
            "Then scry {scry_count} if the creature was returned this way.",
            "A successful return is followed by scry {scry_count}.",
            "When you return the creature, you scry {scry_count}.",
            "Returning that creature lets you scry {scry_count}.",
            "Scry {scry_count} after the creature goes back to hand.",
            "If you return the creature this way, scry {scry_count}.",
            "Follow the creature's return with scry {scry_count}.",
            "Once the creature has returned, you scry {scry_count}.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_cast_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self.scenario_combat(False, True, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(False, True, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive(self):
        return self.scenario_combat(False, False, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive_beyond_boundary(self):
        return self.scenario_combat(False, False, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies(self):
        return self.scenario_combat(False, False, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(False, False, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die(self):
        return self.scenario_combat(False, True, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die_beyond_boundary(self):
        return self.scenario_combat(False, True, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_dies_self_survives(self):
        return self.scenario_combat(True, True, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(True, True, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_survive(self):
        return self.scenario_combat(True, False, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_survive_beyond_boundary(self):
        return self.scenario_combat(True, False, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_survives_self_dies(self):
        return self.scenario_combat(True, False, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(True, False, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_die(self):
        return self.scenario_combat(True, True, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_die_beyond_boundary(self):
        return self.scenario_combat(True, True, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'special_type')})
    def simulate_attack_empty_board(self):
        return self.scenario_unblocked(False)

    @simulate(evidence={'fields': ('attack', 'special_type')})
    def simulate_attack_opponent_passes(self):
        return self.scenario_unblocked(True)

    def _enter_scene(self,role,offset=1,option=1,hand_count=None,hexproof=False,power_offset=0,in_stack=False):
        hand_count=self.scenario_count("hand",hand_count,minimum=1)
        self.scenario_prepare()
        self.player.hand.clear()
        self.scenario_random_cards(self.player,"hand",hand_count)
        subaction = 0
        if role in ("self_creature", "enemy_creature"):
            owner = self.player if role == "self_creature" else self.player.opponent
            health = self.card.effect_params.get("damage", 2) + offset
            if health <= 0:
                return self.scenario_skip()
            power = max(0, self.card.effect_params.get("power_threshold", 2) + power_offset)
            self.scenario_creature(owner, power=power, health=health, flags={"Hexproof": hexproof})
            subaction = 11 if owner is self.player else 1
        elif role in ("self_player", "enemy_player"):
            owner = self.player if role == "self_player" else self.player.opponent
            life = self.card.effect_params.get("damage", 2) + offset
            if not 1 <= life <= owner.ini_life:
                return self.scenario_skip()
            owner.life = life
            subaction = 22 if owner is self.player else 21
        self.scenario_option(option)
        self.card.select_range = 'all_creatures' if option == 1 and role != "none" else ""
        if not self.card.select_range:
            subaction = 0
        self.player.mana.update(self.card.calculate_cost())
        return self.scenario_cast((subaction,), provide_mana=False, in_stack=in_stack)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option', 'enter.effect', 'enter.scry'), 'fields': ('mana_cost',)})
    def simulate_enter_self_creature_normal(self):
        return self._enter_scene('self_creature',offset=1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option', 'enter.effect', 'enter.scry'), 'fields': ('mana_cost',)})
    def simulate_enter_enemy_creature_normal(self):
        return self._enter_scene('enemy_creature',offset=1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option', 'enter.effect', 'enter.scry'), 'fields': ('mana_cost',)})
    def simulate_enter_none_normal(self):
        return self._enter_scene('none',offset=1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option', 'enter.effect', 'enter.scry'), 'fields': ('mana_cost',)})
    def simulate_enter_self_creature_hexproof(self):
        return self._enter_scene('self_creature',hexproof=True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option', 'enter.effect', 'enter.scry'), 'fields': ('mana_cost',)})
    def simulate_enter_enemy_creature_hexproof(self):
        return self._enter_scene('enemy_creature',hexproof=True)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option'), 'fields': ('mana_cost',)})
    def simulate_enter_decline_self_creature(self):
        return self._enter_scene('self_creature',option=2)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option'), 'fields': ('mana_cost',)})
    def simulate_enter_decline_enemy_creature(self):
        return self._enter_scene('enemy_creature',option=2)

    @simulate(evidence={'text': ('enter.trigger', 'enter.option'), 'fields': ('mana_cost',)})
    def simulate_enter_decline_none(self):
        return self._enter_scene('none',option=2)

