from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.land.Mountain.model import Mountain
from pycards.sorcery.Earthquake_Tremor.model import Earthquake_Tremor


@bind_card(Earthquake_Tremor)
class Earthquake_Tremor_Simulation(Card_Simulation):
    scenario_locks={
        '_effect_scene':('opponent.battlefield', 'opponent.graveyard', 'opponent.land_area', 'opponent.library', 'self.battlefield', 'self.graveyard', 'self.hand', 'self.land_area', 'self.library'),
    }

    text_parts = {
        "destroy.effect": [
            "Destroy {destroy_count} randomly chosen opposing creatures, or all if fewer exist.",
            "Randomly select up to {destroy_count} opposing creatures and destroy them, taking all if fewer.",
            "Destroy as many available opposing creatures as possible, up to {destroy_count}, choosing randomly.",
            "Choose {destroy_count} opposing creatures at random to destroy, or all available if fewer.",
            "Destroy up to {destroy_count} opposing creatures chosen randomly, taking all if fewer remain.",
            "Randomly pick opposing creatures without replacement and destroy up to {destroy_count} of them.",
            "Destroy a random set of up to {destroy_count} available opposing creatures.",
            "For {destroy_count} attempts, destroy a randomly chosen opposing creature not chosen earlier, if available.",
            "Choose and destroy opposing creatures randomly until {destroy_count} are chosen or none remain unchosen.",
            "Destroy {destroy_count} random opposing creatures if possible, or all available if fewer exist.",
        ],
        "token.effect": [
            "For each creature selected this way, create one {token_power}/{token_toughness} Elemental, even if destruction is prevented.",
            "Create a {token_power}/{token_toughness} Elemental for every attempted destruction, including protected creatures.",
            "Each creature chosen for destruction produces one {token_power}/{token_toughness} Elemental for you, whether it dies or survives protection.",
            "For each selected creature, put one {token_power}/{token_toughness} Elemental onto your battlefield even if it cannot be destroyed.",
            "You create one {token_power}/{token_toughness} Elemental per creature this effect tries to destroy.",
            "Every attempted destruction gives you one {token_power}/{token_toughness} Elemental token.",
            "Put a {token_power}/{token_toughness} Elemental into play for each creature selected for destruction, including protected targets.",
            "For every creature selected here, summon a {token_power}/{token_toughness} Elemental regardless of destruction success.",
            "Each selected opposing creature generates one {token_power}/{token_toughness} Elemental for you even when destruction is prevented.",
            "Create a {token_power}/{token_toughness} Elemental for each attempted creature destruction this way.",
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
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('destroy.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0(self):
        return self._effect_scene(0,0)

    @simulate(evidence={'text': ('destroy.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0(self):
        return self._effect_scene(1,0)

    @simulate(evidence={'text': ('destroy.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1(self):
        return self._effect_scene(0,1)

    @simulate(evidence={'text': ('destroy.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1(self):
        return self._effect_scene(1,1)

    @simulate(evidence={'text': ('destroy.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3(self):
        return self._effect_scene(3,3)

    @simulate(evidence={'text': ('destroy.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5(self):
        return self._effect_scene(0,5)

    @simulate(evidence={'text': ('destroy.effect', 'token.effect'), 'fields': ('mana_cost',)})
    def simulate_indestructible(self):
        return self._effect_scene(2,5,mountains=3,protected=True)

