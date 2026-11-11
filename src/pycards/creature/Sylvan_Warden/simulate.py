from game.type_cards.land import Land
from pycards.land.Plains.model import Plains
from pycards.land.Forest.model import Forest
from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Sylvan_Warden.model import Sylvan_Warden


@bind_card(Sylvan_Warden)
class Sylvan_Warden_Simulation(Card_Simulation):
    scenario_locks={
        '_warden_combat':('opponent.battlefield', 'self.battlefield'),
        '_friendly_attack':('self.battlefield',),
        '_enter_library':('self.land_area', 'self.library'),
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
        "land.effect": [
            "Put the first basic land in your library onto your battlefield tapped, if one is available.",
            "If your library has a basic land, put its earliest one onto your battlefield tapped.",
            "Take the earliest basic land from your library and put it into play tapped, if possible.",
            "Move the first available basic land from your library onto your battlefield tapped.",
            "Your library's first basic land enters your battlefield tapped, if present.",
            "Find the first basic land in library order and put it into play tapped.",
            "Put the earliest available basic land in your library onto your battlefield in a tapped state.",
            "From your library, put the first basic land you find onto your battlefield tapped.",
            "If any basic lands remain in your library, move the first one into play tapped.",
            "Scan your library in order and put its first basic land onto your battlefield tapped.",
        ],
        "attack.trigger": [
            "Whenever this creature attacks,",
            "When this creature attacks,",
            "Each time this creature attacks,",
            "Whenever this creature starts attacking,",
            "When this creature begins an attack,",
            "As this creature attacks,",
            "When an attack by this creature begins,",
            "On each attack by this creature,",
            "Whenever this creature begins attacking,",
            "At the start of this creature's attack,",
        ],
        "attack.effect": [
            "a random creature you control, including this one, permanently gets +{power_bonus}/+{toughness_bonus}.",
            "give one random friendly creature, possibly this creature, a permanent +{power_bonus}/+{toughness_bonus} buff.",
            "randomly select a creature you control, including itself, to gain +{power_bonus}/+{toughness_bonus} permanently.",
            "one of your creatures chosen at random, possibly this one, gains permanent +{power_bonus}/+{toughness_bonus}.",
            "apply a permanent +{power_bonus}/+{toughness_bonus} buff to a random friendly creature, including this creature.",
            "randomly give a creature on your battlefield, possibly itself, +{power_bonus}/+{toughness_bonus} without expiry.",
            "a randomly chosen friendly creature, including this one, gains {power_bonus} power and {toughness_bonus} health permanently.",
            "choose one of your creatures randomly, with this creature eligible, and grant it permanent +{power_bonus}/+{toughness_bonus}.",
            "one randomly selected creature under your control gets +{power_bonus}/+{toughness_bonus} permanently, possibly this creature.",
            "grant permanent +{power_bonus}/+{toughness_bonus} to a random creature you control, allowing this creature itself.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',), 'text': ('enter.trigger', 'land.effect')})
    def simulate_when_cast(self):
        self.scenario_prepare()
        return self.scenario_cast()

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_cast_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'attack.effect')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self._warden_combat(False, True, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'attack.effect')})
    def simulate_attack_opponent_dies_self_survives_beyond_boundary(self):
        return self._warden_combat(False, True, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'attack.effect')})
    def simulate_attack_both_survive(self):
        return self._warden_combat(False, False, False, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'attack.effect')})
    def simulate_attack_both_survive_beyond_boundary(self):
        return self._warden_combat(False, False, False, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'attack.effect')})
    def simulate_attack_opponent_survives_self_dies(self):
        return self._warden_combat(False, False, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'attack.effect')})
    def simulate_attack_opponent_survives_self_dies_beyond_boundary(self):
        return self._warden_combat(False, False, True, margin=1)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'attack.effect')})
    def simulate_attack_both_die(self):
        return self._warden_combat(False, True, True, margin=0)

    @simulate(evidence={'fields': ('attack', 'defend', 'special_type'), 'text': ('attack.trigger', 'attack.effect')})
    def simulate_attack_both_die_beyond_boundary(self):
        return self._warden_combat(False, True, True, margin=1)

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

    @simulate(evidence={'fields': ('attack', 'special_type'), 'text': ('attack.trigger', 'attack.effect')})
    def simulate_attack_empty_board(self):
        return self.scenario_unblocked(False)

    @simulate(evidence={'fields': ('attack', 'special_type'), 'text': ('attack.trigger', 'attack.effect')})
    def simulate_attack_opponent_passes(self):
        return self.scenario_unblocked(True)

    def _warden_combat(self, defending, enemy_dies, self_dies, margin=0):
        self.scenario_prepare()
        power = self.card.state[0] + (0 if defending else self.card.effect_params["power_bonus"])
        health = self.card.state[1] + (0 if defending else self.card.effect_params["toughness_bonus"])
        if health <= 0 or (enemy_dies and power <= margin) or (not self_dies and health <= margin):
            return self.scenario_skip()
        self.scenario_creature(self.player.opponent, power=health + margin if self_dies else health - 1 - margin, health=power - margin if enemy_dies else power + 1 + margin, flags={})
        record = self.room.simulate_creature_defend(self.card) if defending else self.room.simulate_creature_attack(self.card)
        self.stage_card(self.card)
        if not defending:
            self.scenario_block()
        return record

    def _friendly_attack(self, count):
        record = self.scenario_unblocked()
        for _ in range(count):
            self.scenario_creature(self.player, power=1, health=3, flags={})
        return record

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect'), 'fields': ('attack', 'special_type')})
    def simulate_random_friendly_0(self):
        return self._friendly_attack(0)

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect'), 'fields': ('attack', 'special_type')})
    def simulate_random_friendly_1(self):
        return self._friendly_attack(1)

    @simulate(evidence={'text': ('attack.trigger', 'attack.effect'), 'fields': ('attack', 'special_type')})
    def simulate_random_friendly_3(self):
        return self._friendly_attack(3)

    def _enter_library(self, basics, forests=0, nonbasic=False, only_lands=False):
        self.scenario_prepare()
        if only_lands:
            self.player.library.clear()
        else:
            self.player.library = [card for card in self.player.library if card.type != "Land"][:3]
        for _ in range(basics):
            self.player.library.append(Plains(self.player))
        for _ in range(forests):
            self.player.library.append(Forest(self.player))
        if nonbasic:
            land = self.scenario_cards(self.player,land=1,basic=False)[0]
            self.player.library.insert(0, land)
        self.player.mana.update(self.card.calculate_cost())
        return self.scenario_cast(provide_mana=False)


    @simulate(evidence={'text': ('enter.trigger', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_library_none(self):
        return self._enter_library(0, 0, nonbasic=False)


    @simulate(evidence={'text': ('enter.trigger', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_library_plains_only(self):
        return self._enter_library(1, 0, nonbasic=False)


    @simulate(evidence={'text': ('enter.trigger', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_library_forest_only(self):
        return self._enter_library(0, 1, nonbasic=False)


    @simulate(evidence={'text': ('enter.trigger', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_library_many(self):
        return self._enter_library(3, 2, nonbasic=False)


    @simulate(evidence={'text': ('enter.trigger', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_library_nonbasic_only(self):
        return self._enter_library(0, 0, nonbasic=True)


    @simulate(evidence={'text': ('enter.trigger', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_library_mixed_nonbasic(self):
        return self._enter_library(1, 2, nonbasic=True)


    @simulate(evidence={'text': ('enter.trigger', 'land.effect'), 'fields': ('mana_cost',)})
    def simulate_enter_empty_library(self):
        return self._enter_library(0, only_lands=True)


