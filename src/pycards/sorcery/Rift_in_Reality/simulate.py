from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.land.Mountain.model import Mountain
from pycards.sorcery.Rift_in_Reality.model import Rift_in_Reality


@bind_card(Rift_in_Reality)
class Rift_in_Reality_Simulation(Card_Simulation):
    scenario_locks={
        '_effect_scene':('opponent.battlefield', 'opponent.graveyard', 'opponent.land_area', 'opponent.library', 'self.battlefield', 'self.graveyard', 'self.hand', 'self.land_area', 'self.library'),
    }

    text_parts = {
        "exile.effect": [
            "Exile a target opposing creature.",
            "Put a target creature your opponent controls into exile.",
            "Exile one creature you target on the opposing battlefield.",
            "Choose an opposing creature to exile.",
            "Send a targeted opposing creature into exile.",
            "The selected opposing creature is exiled.",
            "Move one target creature your opponent controls into exile.",
            "Exile a creature of your choice controlled by your opponent.",
            "Put the chosen opposing creature into exile.",
            "Target one opposing creature and exile it.",
        ],
        "return.effect": [
            "At your next upkeep, create a fresh copy on its owner's battlefield while retaining the exiled original, then that owner draws {draw_count} cards.",
            "When your next turn begins, its owner gets a fresh battlefield copy without removing the exiled card and draws {draw_count} cards.",
            "At your next turn start, copy that creature onto its owner's battlefield, leave the original in exile, and have its owner draw {draw_count} cards.",
            "During your next upkeep, put a fresh copy onto its owner's battlefield while keeping the original exiled, then its owner draws {draw_count} cards.",
            "On your next upkeep, that creature's owner creates a fresh battlefield copy, retains the exiled original, and draws {draw_count} cards.",
            "At the beginning of your next turn, put its fresh copy onto its owner's battlefield without moving the original from exile, then its owner draws {draw_count} cards.",
            "Your next upkeep creates a fresh battlefield copy for the creature's owner, leaves the original in exile, and makes that owner draw {draw_count} cards.",
            "When your following turn starts, give its owner a fresh battlefield copy while the original stays exiled, then that owner draws {draw_count} cards.",
            "Create a fresh copy for its owner at your next upkeep, retaining the original in exile, and have that owner draw {draw_count} cards.",
            "At your next turn's beginning, its owner gets a fresh battlefield copy plus {draw_count} drawn cards, while the original remains in exile.",
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
            owner = self.player.opponent
            self.scenario_replace_cards(owner,"library",instant=(library_count, library_count))
            owner.library = [card for card in owner.library if card.type == "Instant"][:library_count]
        self.player.mana.update(self.card.calculate_cost())
        subaction = 11 if role == "self" else 1 if role == "enemy" else 21
        return self.scenario_cast((subaction,), provide_mana=False)

    @simulate(evidence={'text': ('exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_self_normal(self):
        return self._effect_scene(1, 0, role='self', offset=0)

    @simulate(evidence={'text': ('exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_enemy_normal(self):
        return self._effect_scene(0, 1, role='enemy', offset=0)

    @simulate(evidence={'text': ('exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_player_normal(self):
        return self._effect_scene(0, 0, role='player', offset=0)

    @simulate(evidence={'text': ('exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_library_empty(self):
        return self._effect_scene(1, 1, role='enemy', library_count=0)

    @simulate(evidence={'text': ('exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_library_short(self):
        return self._effect_scene(1, 1, role='enemy', library_count=max(0, self.card.effect_params["draw_count"] - 1))

    @simulate(evidence={'text': ('exile.effect', 'return.effect'), 'fields': ('mana_cost',)})
    def simulate_library_exact(self):
        return self._effect_scene(1, 1, role='enemy', library_count=self.card.effect_params["draw_count"])

