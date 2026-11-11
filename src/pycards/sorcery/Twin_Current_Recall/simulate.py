from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.land.Plains.model import Plains
from pycards.sorcery.Twin_Current_Recall.model import Twin_Current_Recall


@bind_card(Twin_Current_Recall)
class Twin_Current_Recall_Simulation(Card_Simulation):
    scenario_locks={
        '_board_scene':('opponent.battlefield', 'opponent.land_area', 'self.battlefield', 'self.land_area', 'self.library'),
    }

    text_parts = {
        "return.effect": [
            "Return each opposing creature with current power at most {power_threshold} to its owner's hand.",
            "Put all opposing creatures whose current power is {power_threshold} or less into their owners' hands.",
            "Every opposing creature with current power no greater than {power_threshold} returns to its owner's hand.",
            "Return opposing creatures to their owners' hands if their current power does not exceed {power_threshold}.",
            "Move all opposing creatures with current power of at most {power_threshold} into their owners' hands.",
            "Each creature your opponent controls with {power_threshold} or less current power goes back to its owner's hand.",
            "Return every opposing creature whose current power is equal to or below {power_threshold} to its owner's hand.",
            "Put opposing creatures back into their owners' hands when their current power is no higher than {power_threshold}.",
            "Return your opponent's creatures with current power of {power_threshold} or less to their owners' hands.",
            "Move every opposing creature with current power no more than {power_threshold} back to its owner's hand.",
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

    def _board_scene(self,own_count,enemy_count,offset=0,protected=False,library_count=None,life=None):
        library_count=self.scenario_count("library",library_count)
        self.scenario_prepare()
        if life is not None:
            if not 1 <= life <= self.player.ini_life:
                return self.scenario_skip()
            self.player.life = life
        for owner, count in ((self.player, own_count), (self.player.opponent, enemy_count)):
            for index in range(count):
                creature = self.scenario_creature(owner, power=2 + index, health=3 + index, flags={"Hexproof": index % 2 == 0, "tap": index % 2 == 1})
                creature.power = max(0, self.card.effect_params["power_threshold"] + offset + index)
                creature.actual_power = max(0, self.card.effect_params["power_threshold"] + offset + index)
                if protected:
                    self.scenario_buff(creature, Indestructible(self.card, creature))
            land = Plains(owner)
            self.scenario_tapped(land)
            self.stage_card(land, owner, zone="land_area")
        if library_count is not None:
            self.scenario_replace_cards(self.player,"library",instant=(library_count, library_count))
            self.player.library = [card for card in self.player.library if card.type == "Instant"][:library_count]
        self.player.mana.update(self.card.calculate_cost())
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_below(self):
        return self._board_scene(0,0,offset=-1)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_equal(self):
        return self._board_scene(0,0,offset=0)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_above(self):
        return self._board_scene(0,0,offset=1)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_below(self):
        return self._board_scene(1,0,offset=-1)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_equal(self):
        return self._board_scene(1,0,offset=0)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_above(self):
        return self._board_scene(1,0,offset=1)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_below(self):
        return self._board_scene(0,1,offset=-1)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_equal(self):
        return self._board_scene(0,1,offset=0)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_above(self):
        return self._board_scene(0,1,offset=1)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_below(self):
        return self._board_scene(1,1,offset=-1)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_equal(self):
        return self._board_scene(1,1,offset=0)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_above(self):
        return self._board_scene(1,1,offset=1)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_below(self):
        return self._board_scene(3,3,offset=-1)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_equal(self):
        return self._board_scene(3,3,offset=0)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_above(self):
        return self._board_scene(3,3,offset=1)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_below(self):
        return self._board_scene(0,5,offset=-1)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_equal(self):
        return self._board_scene(0,5,offset=0)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_above(self):
        return self._board_scene(0,5,offset=1)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_5_enemy_0_below(self):
        return self._board_scene(5,0,offset=-1)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_5_enemy_0_equal(self):
        return self._board_scene(5,0,offset=0)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_5_enemy_0_above(self):
        return self._board_scene(5,0,offset=1)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_protected_battlefields(self):
        return self._board_scene(3,3,protected=True)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_library_empty(self):
        return self._board_scene(2,3,library_count=0)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_library_short(self):
        return self._board_scene(2,3,library_count=max(0, self.card.effect_params["draw_count"] - 1))

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_library_exact(self):
        return self._board_scene(2,3,library_count=self.card.effect_params["draw_count"])

