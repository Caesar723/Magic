from game.card_simulation import bind_card, simulate, Card_Simulation
from game.type_cards.land import Land
from pycards.land.Plains.model import Plains
from pycards.land.Forest.model import Forest
from pycards.Instant.Wild_Growth_Rush.model import Wild_Growth_Rush


@bind_card(Wild_Growth_Rush)
class Wild_Growth_Rush_Simulation(Card_Simulation):
    text_parts = {
        "buff.stats": [
            "It gets +{power_bonus}/+{toughness_bonus} until that creature's controller's turn ends.",
            "Give it +{power_bonus}/+{toughness_bonus} until that creature's controller's turn ends.",
            "It gains +{power_bonus}/+{toughness_bonus} until that creature's controller's turn ends.",
            "Until that creature's controller's turn ends, it gets +{power_bonus}/+{toughness_bonus}.",
            "Increase its power by {power_bonus} and toughness by {toughness_bonus} until that creature's controller's turn ends.",
            "It receives +{power_bonus}/+{toughness_bonus} until that creature's controller's turn ends.",
            "Its power increases by {power_bonus} and its toughness by {toughness_bonus} until that creature's controller's turn ends.",
            "Grant it +{power_bonus}/+{toughness_bonus} until that creature's controller's turn ends.",
            "It gets an extra {power_bonus} power and {toughness_bonus} toughness until that creature's controller's turn ends.",
            "Until that creature's controller's turn ends, add {power_bonus} to its power and {toughness_bonus} to its toughness.",
        ],
        "buff.trample": [
            "It also gains trample until its controller's turn ends.",
            "It receives trample until its controller's turn ends.",
            "Give it trample until its controller's turn ends.",
            "It has trample until its controller's turn ends.",
            "Until its controller's turn ends, it also has trample.",
            "It gains the trample ability until its controller's turn ends.",
            "Grant it trample until its controller's turn ends.",
            "Until its controller's turn ends, it receives trample.",
            "Until its controller's turn ends, it also gains trample.",
            "It is granted trample until its controller's turn ends.",
        ],
        "land.condition": [
            "If you control a Forest,",
            "If a Forest is on your battlefield,",
            "When your lands include a Forest,",
            "If at least one Forest is under your control,",
            "If there is a Forest among your lands,",
            "When a Forest is in your land area,",
            "If you have a Forest in play,",
            "If one or more Forests are on your side,",
            "When your battlefield contains a Forest,",
            "If a Forest is present under your control,",
        ],
        "land.effect": [
            "Put a random basic land from your library onto your battlefield tapped, if one is available.",
            "If your library has a basic land, randomly choose one and put it onto your battlefield tapped.",
            "Choose a basic land from your library at random and put it into play tapped, if possible.",
            "If available, move one random basic land from your library onto your battlefield tapped.",
            "Randomly select a basic land in your library and put it onto your battlefield tapped, when available.",
            "When your library contains a basic land, put one selected at random into play tapped.",
            "Move a randomly chosen basic land from your library onto your battlefield tapped if any exist.",
            "Put one basic land chosen randomly from your library into play tapped, if you have one.",
            "From your library, take a random basic land if present and put it onto your battlefield tapped.",
            "If any basic lands remain in your library, randomly choose one to enter your battlefield tapped.",
        ],
        "library.shuffle": [
            "If a land was put into play this way, then shuffle your library.",
            "If a land was put into play this way, shuffle the remaining library afterward.",
            "If a land was put into play this way, next, shuffle your remaining library.",
            "If a land was put into play this way, afterward, shuffle the library.",
            "If a land was put into play this way, finish by shuffling your library.",
            "If a land was put into play this way, finally, randomize your library's order.",
            "If a land was put into play this way, shuffle your library after this.",
            "If a land was put into play this way, after moving the land, shuffle your library.",
            "If a land was put into play this way, then randomize the order of your remaining library.",
            "If a land was put into play this way, the remaining library is shuffled afterward.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _resource_scene(self, basics, other_cards=3, nonbasic=False, role="none", forest=False, tapped=0, missing=1, grave_count=0):
        self.scenario_prepare()
        self.player.life = max(1, self.player.ini_life - missing)
        self.player.graveyard.clear()
        self.room.env_initinal_library(self.player, {"instant_number": (other_cards, other_cards), "creature_number": (0, 0), "sorcery_number": (0, 0), "land_number": (0, 0)})
        self.player.library = [card for card in self.player.library if card.type == "Instant"][:other_cards]
        for _ in range(basics):
            self.player.library.append(Plains(self.player))
        if nonbasic:
            land = Land(self.player)
            land.name, land.type = "Review nonbasic land", "Land"
            self.player.library.insert(0, land)
        for index in range(tapped):
            land = Plains(self.player)
            land.tap()
            self.stage_card(land, zone="land_area")
        if forest:
            self.stage_card(Forest(self.player), zone="land_area")
        subaction = 0
        if role != "none":
            owner = self.player.opponent if role.startswith("enemy") else self.player
            flags = {"Hexproof": role.endswith("hexproof"), "Trample": role.endswith("trample")}
            self.scenario_creature(owner, power=2, health=3, flags=flags)
            subaction = 1 if owner is self.player.opponent else 11
        self.player.mana.update(self.card.calculate_cost())
        return self.scenario_cast((subaction,), provide_mana=False)

    @simulate(evidence={'text': ('buff.stats', 'buff.trample', 'land.condition', 'land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_basic_none(self):
        return self._resource_scene(0, role="self")

    @simulate(evidence={'text': ('buff.stats', 'buff.trample', 'land.condition', 'land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_basic_one(self):
        return self._resource_scene(1, role="self")

    @simulate(evidence={'text': ('buff.stats', 'buff.trample', 'land.condition', 'land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_basic_several(self):
        return self._resource_scene(4, role="self")

    @simulate(evidence={'text': ('buff.stats', 'buff.trample', 'land.condition', 'land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_nonbasic_first(self):
        return self._resource_scene(2, nonbasic=True, role="self")

    @simulate(evidence={'text': ('buff.stats', 'buff.trample', 'land.condition', 'land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_empty_library(self):
        return self._resource_scene(0, other_cards=0, role="self")

    @simulate(evidence={'text': ('buff.stats', 'buff.trample', 'land.condition', 'land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_only_basic_library(self):
        return self._resource_scene(1, other_cards=0, role="self")

    @simulate(evidence={'text': ('buff.stats', 'buff.trample', 'land.condition', 'land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_self_forest_False(self):
        return self._resource_scene(3, role='self', forest=False)

    @simulate(evidence={'text': ('buff.stats', 'buff.trample', 'land.condition', 'land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_enemy_forest_False(self):
        return self._resource_scene(3, role='enemy', forest=False)

    @simulate(evidence={'text': ('buff.stats', 'buff.trample', 'land.condition', 'land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_none_forest_False(self):
        return self._resource_scene(3, role='none', forest=False)

    @simulate(evidence={'text': ('buff.stats', 'buff.trample', 'land.condition', 'land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_self_trample_forest_False(self):
        return self._resource_scene(3, role='self_trample', forest=False)

    @simulate(evidence={'text': ('buff.stats', 'buff.trample', 'land.condition', 'land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_enemy_hexproof_forest_False(self):
        return self._resource_scene(3, role='enemy_hexproof', forest=False)

    @simulate(evidence={'text': ('buff.stats', 'buff.trample', 'land.condition', 'land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_self_forest_True(self):
        return self._resource_scene(3, role='self', forest=True)

    @simulate(evidence={'text': ('buff.stats', 'buff.trample', 'land.condition', 'land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_enemy_forest_True(self):
        return self._resource_scene(3, role='enemy', forest=True)

    @simulate(evidence={'text': ('buff.stats', 'buff.trample', 'land.condition', 'land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_none_forest_True(self):
        return self._resource_scene(3, role='none', forest=True)

    @simulate(evidence={'text': ('buff.stats', 'buff.trample', 'land.condition', 'land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_self_trample_forest_True(self):
        return self._resource_scene(3, role='self_trample', forest=True)

    @simulate(evidence={'text': ('buff.stats', 'buff.trample', 'land.condition', 'land.effect', 'library.shuffle'), 'fields': ('mana_cost',)})
    def simulate_enemy_hexproof_forest_True(self):
        return self._resource_scene(3, role='enemy_hexproof', forest=True)

