from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.land.Plains.model import Plains
from pycards.Instant.Mystic_Evasion.model import Mystic_Evasion


@bind_card(Mystic_Evasion)
class Mystic_Evasion_Simulation(Card_Simulation):
    text_parts = {
        "return.effect": [
            "Return the current attacker to its owner's hand if it is still on a battlefield.",
            "If the current attacking creature is still in play, put it into its owner's hand.",
            "Put the room's current attacker into its owner's hand if that creature is still in play.",
            "Return the attacking creature to its owner's hand when it is still on either battlefield.",
            "If the current attacker remains on a battlefield, return it to its owner's hand.",
            "Move the current attacking creature back to its owner's hand, provided it is still in play.",
            "The current attacker goes back to its owner's hand if it remains on either battlefield.",
            "When the current attacking creature is in play, return it to the hand of its owner.",
            "Take the current attacker off its battlefield and put it into its owner's hand, if present.",
            "Send the creature currently attacking back to its owner's hand if it is still on a battlefield.",
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

    def _return_scene(self, role, tapped=0, library_count=None, flags=None):
        self.scenario_prepare()
        for index in range(tapped + 1):
            land = Plains(self.player)
            if index < tapped:
                land.tap()
            self.stage_card(land, zone="land_area")
        if library_count is not None:
            self.room.env_initinal_library(self.player, {"instant_number": (library_count, library_count), "creature_number": (0, 0), "sorcery_number": (0, 0), "land_number": (0, 0)})
            self.player.library = [card for card in self.player.library if card.type == "Instant"][:library_count]
        subaction = 0
        if role in ("self", "enemy"):
            owner = self.player if role == "self" else self.player.opponent
            target = self.scenario_creature(owner, power=2, health=4, flags=flags or {})
            target.actual_live = 2
            subaction = 11 if role == "self" else 1
        elif role == "player":
            subaction = 21
        if role in ("self", "enemy"):
            self.room.attacker = target
            target.set_counter_dict("attack_counter", 1)
        self.player.mana.update(self.card.calculate_cost())
        record = self.scenario_cast(in_stack=role != "none", provide_mana=False)
        if role != "none":
            self.room.flag_dict["attacker_defenders"] = True
            self.room.non_active_player = self.player if role == "enemy" else self.player.opponent
        return record

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_return_self(self):
        return self._return_scene('self')

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_return_enemy(self):
        return self._return_scene('enemy')

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_return_none(self):
        return self._return_scene('none')

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_hexproof(self):
        return self._return_scene('self', flags={'Hexproof': True})

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_tap(self):
        return self._return_scene('self', flags={'tap': True})

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_hexproof(self):
        return self._return_scene('enemy', flags={'Hexproof': True})

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_tap(self):
        return self._return_scene('enemy', flags={'tap': True})

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_library_empty(self):
        return self._return_scene("enemy", library_count=0)

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_library_short(self):
        return self._return_scene("enemy", library_count=max(0, self.card.effect_params["draw_count"] - 1))

    @simulate(evidence={'text': ('return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_library_exact(self):
        return self._return_scene("enemy", library_count=self.card.effect_params["draw_count"])

