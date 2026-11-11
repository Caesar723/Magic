from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.land.Mountain.model import Mountain
from pycards.sorcery.Flamestrike_Surge__.model import Flamestrike_Surge__


@bind_card(Flamestrike_Surge__)
class Flamestrike_Surge___Simulation(Card_Simulation):
    text_parts = {
        "damage.effect": [
            "{card_name} deals {damage} damage to the target.",
            "Deal {damage} damage to the selected target.",
            "The target takes {damage} damage from {card_name}.",
            "{card_name} inflicts {damage} damage on that target.",
            "Deal the chosen target {damage} damage.",
            "Hit the target for {damage} damage.",
            "The selected target is dealt {damage} damage.",
            "Deal an amount of damage equal to {damage} to the target.",
            "{card_name} hits the chosen target for {damage} damage.",
            "Inflict {damage} points of damage on the target.",
        ],
        "hand.condition": [
            "If any cards remain in your hand after casting this spell,",
            "If your hand is not empty after this spell is cast,",
            "When at least one hand card remains after casting,",
            "If you have another card in your hand after casting,",
            "If your hand still contains a card after this spell is cast,",
            "When there are cards left in your hand after casting,",
            "If at least one card is left in your hand after casting this spell,",
            "If your hand remains nonempty after casting,",
            "When you still have a hand card after this spell is cast,",
            "If another hand card remains after casting this spell,",
        ],
        "hand.remove": [
            "remove {discard_count} random hand cards, or all available if fewer,",
            "randomly remove up to {discard_count} hand cards, taking all if fewer remain,",
            "take {discard_count} random cards out of your hand, limited by availability,",
            "remove hand cards at random {discard_count} times while any remain,",
            "randomly select and remove {discard_count} hand cards if available,",
            "remove up to {discard_count} randomly chosen cards from your hand, taking all if fewer,",
            "randomly take as many as {discard_count} available hand cards out of your hand,",
            "choose {discard_count} hand cards randomly to remove, stopping when the hand empties,",
            "take out {discard_count} cards chosen randomly from your hand, or all if fewer exist,",
            "remove {discard_count} randomly selected hand cards, stopping if none remain,",
        ],
        "hand.draw": [
            "draw {draw_count} card{draw_count_plural}.",
            "draw {draw_count_word} card{draw_count_plural}.",
            "take the top {draw_count} card{draw_count_plural} of your library into your hand.",
            "put the top {draw_count} card{draw_count_plural} from your library into your hand.",
            "add the top {draw_count} card{draw_count_plural} of your library to your hand.",
            "you draw {draw_count} card{draw_count_plural}.",
            "draw a total of {draw_count} card{draw_count_plural}.",
            "you draw a total of {draw_count_word} card{draw_count_plural}.",
            "take {draw_count} card{draw_count_plural} from the top of your library into your hand.",
            "put {draw_count} card{draw_count_plural} from the top of your library into your hand.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _effect_scene(self, own_count, enemy_count, protected=False, mountains=0, offset=0, role="enemy", hand_count=1, library_count=None, grave_count=0, tapped=False):
        self.scenario_prepare()
        self.player.hand.clear()
        self.player.graveyard.clear()
        self.player.opponent.graveyard.clear()
        for _ in range(hand_count):
            self.player.append_card(self.card.copy_for_player(self.player), "hand")
        for _ in range(mountains):
            land = Mountain(self.player)
            land.tap()
            self.stage_card(land, zone="land_area")
        for owner, count in ((self.player, own_count), (self.player.opponent, enemy_count)):
            for index in range(count):
                health = max(1, self.card.effect_params.get("damage", 3) + offset + index)
                creature = self.scenario_creature(owner, power=index + 1, health=health, flags={"tap": tapped, "Hexproof": False})
                if protected:
                    creature.gain_buff(Indestructible(self.card, creature), self.card)
        for owner in (self.player, self.player.opponent):
            for _ in range(grave_count):
                creature = self.scenario_creature(owner, power=2, health=3, flags={})
                owner.remove_card(creature, "battlefield")
                owner.append_card(creature, "graveyard")
        if library_count is not None:
            owner = self.player
            self.room.env_initinal_library(owner, {"instant_number": (library_count, library_count), "sorcery_number": (0, 0), "creature_number": (0, 0), "land_number": (0, 0)})
            owner.library = [card for card in owner.library if card.type == "Instant"][:library_count]
        self.player.mana.update(self.card.calculate_cost())
        if (own_count or enemy_count) and self.card.effect_params["damage"] + offset <= 0:
            return self.scenario_skip()
        if role == "player":
            life = self.card.effect_params["damage"] + offset
            if not 1 <= life <= self.player.opponent.ini_life:
                return self.scenario_skip()
            self.player.opponent.life = life
        subaction = 11 if role == "self" else 1 if role == "enemy" else 21
        return self.scenario_cast((subaction,), provide_mana=False)

    @simulate(evidence={'text': ('damage.effect', 'hand.condition', 'hand.remove', 'hand.draw'), 'fields': ('mana_cost',)})
    def simulate_self_overkill(self):
        return self._effect_scene(1, 0, role='self', offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'hand.condition', 'hand.remove', 'hand.draw'), 'fields': ('mana_cost',)})
    def simulate_self_exact(self):
        return self._effect_scene(1, 0, role='self', offset=0)

    @simulate(evidence={'text': ('damage.effect', 'hand.condition', 'hand.remove', 'hand.draw'), 'fields': ('mana_cost',)})
    def simulate_self_survives(self):
        return self._effect_scene(1, 0, role='self', offset=1)

    @simulate(evidence={'text': ('damage.effect', 'hand.condition', 'hand.remove', 'hand.draw'), 'fields': ('mana_cost',)})
    def simulate_enemy_overkill(self):
        return self._effect_scene(0, 1, role='enemy', offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'hand.condition', 'hand.remove', 'hand.draw'), 'fields': ('mana_cost',)})
    def simulate_enemy_exact(self):
        return self._effect_scene(0, 1, role='enemy', offset=0)

    @simulate(evidence={'text': ('damage.effect', 'hand.condition', 'hand.remove', 'hand.draw'), 'fields': ('mana_cost',)})
    def simulate_enemy_survives(self):
        return self._effect_scene(0, 1, role='enemy', offset=1)

    @simulate(evidence={'text': ('damage.effect', 'hand.condition', 'hand.remove', 'hand.draw'), 'fields': ('mana_cost',)})
    def simulate_player_overkill(self):
        return self._effect_scene(0, 0, role='player', offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'hand.condition', 'hand.remove', 'hand.draw'), 'fields': ('mana_cost',)})
    def simulate_player_exact(self):
        return self._effect_scene(0, 0, role='player', offset=0)

    @simulate(evidence={'text': ('damage.effect', 'hand.condition', 'hand.remove', 'hand.draw'), 'fields': ('mana_cost',)})
    def simulate_player_survives(self):
        return self._effect_scene(0, 0, role='player', offset=1)

    @simulate(evidence={'text': ('damage.effect', 'hand.condition', 'hand.remove', 'hand.draw'), 'fields': ('mana_cost',)})
    def simulate_library_empty(self):
        return self._effect_scene(1, 1, role='enemy', library_count=0)

    @simulate(evidence={'text': ('damage.effect', 'hand.condition', 'hand.remove', 'hand.draw'), 'fields': ('mana_cost',)})
    def simulate_library_short(self):
        return self._effect_scene(1, 1, role='enemy', library_count=max(0, self.card.effect_params["draw_count"] - 1))

    @simulate(evidence={'text': ('damage.effect', 'hand.condition', 'hand.remove', 'hand.draw'), 'fields': ('mana_cost',)})
    def simulate_library_exact(self):
        return self._effect_scene(1, 1, role='enemy', library_count=self.card.effect_params["draw_count"])

    @simulate(evidence={'text': ('damage.effect', 'hand.condition', 'hand.remove', 'hand.draw'), 'fields': ('mana_cost',)})
    def simulate_hand_0(self):
        return self._effect_scene(0, 0, role="player", hand_count=0)

    @simulate(evidence={'text': ('damage.effect', 'hand.condition', 'hand.remove', 'hand.draw'), 'fields': ('mana_cost',)})
    def simulate_hand_1(self):
        return self._effect_scene(0, 0, role="player", hand_count=1)

    @simulate(evidence={'text': ('damage.effect', 'hand.condition', 'hand.remove', 'hand.draw'), 'fields': ('mana_cost',)})
    def simulate_hand_3(self):
        return self._effect_scene(0, 0, role="player", hand_count=3)

