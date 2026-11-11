from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.land.Mountain.model import Mountain
from pycards.Instant.Veiled_Concealment.model import Veiled_Concealment


@bind_card(Veiled_Concealment)
class Veiled_Concealment_Simulation(Card_Simulation):
    scenario_locks={
        '_effect_scene':('opponent.battlefield', 'opponent.graveyard', 'opponent.land_area', 'opponent.library', 'self.battlefield', 'self.graveyard', 'self.hand', 'self.land_area', 'self.library'),
    }

    text_parts = {
        "keyword.effect": [
            "Give a target creature you control the unblockable keyword until your end step.",
            "A target creature you control gains unblockable until your turn ends.",
            "Grant unblockable to one of your creatures until your end step.",
            "Until your end step, a target creature under your control has unblockable.",
            "The selected creature you control receives unblockable until your turn ends.",
            "Choose one of your creatures to gain the unblockable keyword until your end step.",
            "Give one targeted creature under your control unblockable through your turn.",
            "The creature you target on your battlefield gains unblockable until your end step.",
            "Until the end of your turn, grant the chosen creature you control unblockable.",
            "Apply the unblockable keyword to a target creature of yours until your end step.",
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

    def _effect_scene(self, own_count, enemy_count, protected=False, mountains=0, offset=0, role="enemy", hand_count=None, library_count=None, grave_count=0, tapped=False):
        hand_count=self.scenario_count("hand",hand_count)
        library_count=self.scenario_count("library",library_count)
        self.scenario_prepare()
        self.player.hand.clear()
        self.player.graveyard.clear()
        self.player.opponent.graveyard.clear()
        self.scenario_random_cards(self.player,"hand",hand_count)
        for _ in range(mountains):
            land = Mountain(self.player)
            self.scenario_tapped(land)
            self.stage_card(land, zone="land_area")
        for owner, count in ((self.player, own_count), (self.player.opponent, enemy_count)):
            for index in range(count):
                health = max(1, self.card.effect_params.get("damage", 3) + offset + index)
                creature = self.scenario_creature(owner, power=index + 1, health=health, flags={"tap": tapped, "Hexproof": False})
                if protected:
                    self.scenario_buff(creature, Indestructible(self.card, creature))
        for owner in (self.player, self.player.opponent):
            for _ in range(grave_count):
                creature = self.scenario_creature(owner, power=2, health=3, flags={}, zone="graveyard")
        if library_count is not None:
            owner = self.player
            self.scenario_replace_cards(owner,"library",instant=(library_count, library_count))
            owner.library = [card for card in owner.library if card.type == "Instant"][:library_count]
        self.player.mana.update(self.card.calculate_cost())
        subaction = 11 if role == "self" else 1 if role == "enemy" else 21
        return self.scenario_cast((subaction,), provide_mana=False)

    @simulate(evidence={'text': ('keyword.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_self_normal(self):
        return self._effect_scene(1, 0, role='self', offset=0)

    @simulate(evidence={'text': ('keyword.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_normal(self):
        return self._effect_scene(0, 1, role='enemy', offset=0)

    @simulate(evidence={'text': ('keyword.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_player_normal(self):
        return self._effect_scene(0, 0, role='player', offset=0)

    @simulate(evidence={'text': ('keyword.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_library_empty(self):
        return self._effect_scene(1, 1, role='self', library_count=0)

    @simulate(evidence={'text': ('keyword.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_library_short(self):
        return self._effect_scene(1, 1, role='self', library_count=max(0, self.card.effect_params["draw_count"] - 1))

    @simulate(evidence={'text': ('keyword.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_library_exact(self):
        return self._effect_scene(1, 1, role='self', library_count=self.card.effect_params["draw_count"])

