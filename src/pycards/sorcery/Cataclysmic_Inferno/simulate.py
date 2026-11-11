from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.land.Mountain.model import Mountain
from pycards.sorcery.Cataclysmic_Inferno.model import Cataclysmic_Inferno


@bind_card(Cataclysmic_Inferno)
class Cataclysmic_Inferno_Simulation(Card_Simulation):
    scenario_locks={
        '_effect_scene':('opponent.battlefield', 'opponent.graveyard', 'opponent.land_area', 'opponent.library', 'self.battlefield', 'self.graveyard', 'self.hand', 'self.land_area', 'self.library'),
    }

    text_parts = {
        "damage.effect": [
            "Deal damage to every opposing creature equal to the number of lands you control named Mountain.",
            "Each opposing creature takes damage equal to your count of lands named Mountain.",
            "Count your lands named Mountain and deal that much damage to each opposing creature.",
            "Deal one damage per land you control named Mountain to every opposing creature.",
            "All opposing creatures are dealt damage equal to the number of your Mountains by name.",
            "For each of your lands named Mountain, deal one damage to every opposing creature.",
            "Damage each creature on the opposing battlefield by your number of lands named Mountain.",
            "Your count of lands with the name Mountain is the damage dealt to every opposing creature.",
            "Deal your Mountain-name land count as damage to all opposing creatures.",
            "Each creature your opponent controls is hit for the number of lands you have named Mountain.",
        ],
        "token.effect": [
            "For each creature that immediately dies from this damage, create {tokens_per_destroyed} {token_power}/{token_toughness} Elemental tokens with haste.",
            "Create {tokens_per_destroyed} hasty {token_power}/{token_toughness} Elementals per immediate creature death from this damage.",
            "Every creature immediately killed by the damage gives you {tokens_per_destroyed} {token_power}/{token_toughness} Elementals with haste.",
            "Put {tokens_per_destroyed} {token_power}/{token_toughness} Elemental tokens with haste onto your battlefield for each immediate victim.",
            "For each opposing creature that dies immediately from the hit, summon {tokens_per_destroyed} hasty {token_power}/{token_toughness} Elementals.",
            "You receive {tokens_per_destroyed} {token_power}/{token_toughness} Elemental tokens with haste for each creature immediately killed.",
            "Each immediate death caused by this damage produces {tokens_per_destroyed} {token_power}/{token_toughness} hasty Elementals for you.",
            "Summon {tokens_per_destroyed} hasty Elementals of size {token_power}/{token_toughness} for every creature immediately killed here.",
            "Create {tokens_per_destroyed} {token_power}/{token_toughness} haste Elementals per opposing creature that dies directly from this damage.",
            "For every immediate creature death following this hit, create {tokens_per_destroyed} hasty {token_power}/{token_toughness} Elemental tokens.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _effect_scene(self,own_count,enemy_count,protected=False,mountains=0,offset=0,hand_count=None,library_count=None,grave_count=0,tapped=False):
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
                health = max(1, mountains + offset + index)
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
        if (own_count or enemy_count) and mountains + offset <= 0:
            return self.scenario_skip()
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_mountains_0_below(self):
        return self._effect_scene(0,0,mountains=0,offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_mountains_0_equal(self):
        return self._effect_scene(0,0,mountains=0,offset=0)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_mountains_0_above(self):
        return self._effect_scene(0,0,mountains=0,offset=1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_mountains_1_below(self):
        return self._effect_scene(0,0,mountains=1,offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_mountains_1_equal(self):
        return self._effect_scene(0,0,mountains=1,offset=0)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_mountains_1_above(self):
        return self._effect_scene(0,0,mountains=1,offset=1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_mountains_3_below(self):
        return self._effect_scene(0,0,mountains=3,offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_mountains_3_equal(self):
        return self._effect_scene(0,0,mountains=3,offset=0)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_mountains_3_above(self):
        return self._effect_scene(0,0,mountains=3,offset=1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_mountains_0_below(self):
        return self._effect_scene(1,0,mountains=0,offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_mountains_0_equal(self):
        return self._effect_scene(1,0,mountains=0,offset=0)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_mountains_0_above(self):
        return self._effect_scene(1,0,mountains=0,offset=1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_mountains_1_below(self):
        return self._effect_scene(1,0,mountains=1,offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_mountains_1_equal(self):
        return self._effect_scene(1,0,mountains=1,offset=0)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_mountains_1_above(self):
        return self._effect_scene(1,0,mountains=1,offset=1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_mountains_3_below(self):
        return self._effect_scene(1,0,mountains=3,offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_mountains_3_equal(self):
        return self._effect_scene(1,0,mountains=3,offset=0)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_mountains_3_above(self):
        return self._effect_scene(1,0,mountains=3,offset=1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_mountains_0_below(self):
        return self._effect_scene(0,1,mountains=0,offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_mountains_0_equal(self):
        return self._effect_scene(0,1,mountains=0,offset=0)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_mountains_0_above(self):
        return self._effect_scene(0,1,mountains=0,offset=1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_mountains_1_below(self):
        return self._effect_scene(0,1,mountains=1,offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_mountains_1_equal(self):
        return self._effect_scene(0,1,mountains=1,offset=0)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_mountains_1_above(self):
        return self._effect_scene(0,1,mountains=1,offset=1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_mountains_3_below(self):
        return self._effect_scene(0,1,mountains=3,offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_mountains_3_equal(self):
        return self._effect_scene(0,1,mountains=3,offset=0)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_mountains_3_above(self):
        return self._effect_scene(0,1,mountains=3,offset=1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_mountains_0_below(self):
        return self._effect_scene(1,1,mountains=0,offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_mountains_0_equal(self):
        return self._effect_scene(1,1,mountains=0,offset=0)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_mountains_0_above(self):
        return self._effect_scene(1,1,mountains=0,offset=1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_mountains_1_below(self):
        return self._effect_scene(1,1,mountains=1,offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_mountains_1_equal(self):
        return self._effect_scene(1,1,mountains=1,offset=0)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_mountains_1_above(self):
        return self._effect_scene(1,1,mountains=1,offset=1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_mountains_3_below(self):
        return self._effect_scene(1,1,mountains=3,offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_mountains_3_equal(self):
        return self._effect_scene(1,1,mountains=3,offset=0)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_mountains_3_above(self):
        return self._effect_scene(1,1,mountains=3,offset=1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_mountains_0_below(self):
        return self._effect_scene(3,3,mountains=0,offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_mountains_0_equal(self):
        return self._effect_scene(3,3,mountains=0,offset=0)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_mountains_0_above(self):
        return self._effect_scene(3,3,mountains=0,offset=1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_mountains_1_below(self):
        return self._effect_scene(3,3,mountains=1,offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_mountains_1_equal(self):
        return self._effect_scene(3,3,mountains=1,offset=0)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_mountains_1_above(self):
        return self._effect_scene(3,3,mountains=1,offset=1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_mountains_3_below(self):
        return self._effect_scene(3,3,mountains=3,offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_mountains_3_equal(self):
        return self._effect_scene(3,3,mountains=3,offset=0)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_mountains_3_above(self):
        return self._effect_scene(3,3,mountains=3,offset=1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_mountains_0_below(self):
        return self._effect_scene(0,5,mountains=0,offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_mountains_0_equal(self):
        return self._effect_scene(0,5,mountains=0,offset=0)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_mountains_0_above(self):
        return self._effect_scene(0,5,mountains=0,offset=1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_mountains_1_below(self):
        return self._effect_scene(0,5,mountains=1,offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_mountains_1_equal(self):
        return self._effect_scene(0,5,mountains=1,offset=0)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_mountains_1_above(self):
        return self._effect_scene(0,5,mountains=1,offset=1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_mountains_3_below(self):
        return self._effect_scene(0,5,mountains=3,offset=-1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_mountains_3_equal(self):
        return self._effect_scene(0,5,mountains=3,offset=0)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_mountains_3_above(self):
        return self._effect_scene(0,5,mountains=3,offset=1)

    @simulate(evidence={'text': ('damage.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_indestructible(self):
        return self._effect_scene(2,5,mountains=3,protected=True)

