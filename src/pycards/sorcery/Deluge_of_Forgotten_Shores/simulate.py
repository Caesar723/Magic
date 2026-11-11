from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.land.Plains.model import Plains
from pycards.sorcery.Deluge_of_Forgotten_Shores.model import Deluge_of_Forgotten_Shores


@bind_card(Deluge_of_Forgotten_Shores)
class Deluge_of_Forgotten_Shores_Simulation(Card_Simulation):
    text_parts = {
        "return.effect": [
            "Return every opposing creature to its owner's hand.",
            "Put all opposing creatures into their owners' hands.",
            "All opposing creatures return to the hands of their owners.",
            "Move every opposing creature from the battlefield to its owner's hand.",
            "Return all opposing creatures in play to their owners' hands.",
            "Put each opposing creature back into its owner's hand.",
            "Every opposing creature goes back to its owner's hand.",
            "Return all opposing creatures to their owners' hands.",
            "Take all opposing creatures off the battlefield and put them into their owners' hands.",
            "Move all opposing creatures on both battlefields back to their owners' hands.",
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

    def _board_scene(self, own_count, enemy_count, offset=0, protected=False, library_count=None, life=None, old_exile=False):
        self.scenario_prepare()
        if life is not None:
            if not 1 <= life <= self.player.ini_life:
                return self.scenario_skip()
            self.player.life = life
        for owner, count in ((self.player, own_count), (self.player.opponent, enemy_count)):
            for index in range(count):
                creature = self.scenario_creature(owner, power=2 + index, health=3 + index, flags={"Hexproof": index % 2 == 0, "tap": index % 2 == 1})
                if protected:
                    creature.gain_buff(Indestructible(self.card, creature), self.card)
            land = Plains(owner)
            land.tap()
            self.stage_card(land, owner, zone="land_area")
        if library_count is not None:
            self.room.env_initinal_library(self.player, {"instant_number": (library_count, library_count), "creature_number": (0, 0), "sorcery_number": (0, 0), "land_number": (0, 0)})
            self.player.library = [card for card in self.player.library if card.type == "Instant"][:library_count]
        self.player.mana.update(self.card.calculate_cost())
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_normal(self):
        return self._board_scene(0, 0, offset=0)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_normal(self):
        return self._board_scene(1, 0, offset=0)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_normal(self):
        return self._board_scene(0, 1, offset=0)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_normal(self):
        return self._board_scene(1, 1, offset=0)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_normal(self):
        return self._board_scene(3, 3, offset=0)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_normal(self):
        return self._board_scene(0, 5, offset=0)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_5_enemy_0_normal(self):
        return self._board_scene(5, 0, offset=0)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_protected_battlefields(self):
        return self._board_scene(3, 3, protected=True)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_library_empty(self):
        return self._board_scene(2, 3, library_count=0)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_library_short(self):
        return self._board_scene(2, 3, library_count=max(0, self.card.effect_params["draw_count"] - 1))

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_library_exact(self):
        return self._board_scene(2, 3, library_count=self.card.effect_params["draw_count"])

