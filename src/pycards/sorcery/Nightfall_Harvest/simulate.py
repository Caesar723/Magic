from game.card_simulation import bind_card, simulate, Card_Simulation
from game.buffs import Indestructible
from pycards.land.Plains.model import Plains
from pycards.sorcery.Nightfall_Harvest.model import Nightfall_Harvest


@bind_card(Nightfall_Harvest)
class Nightfall_Harvest_Simulation(Card_Simulation):
    text_parts = {
        "destroy.effect": [
            "Destroy all opposing creatures.",
            "Destroy each creature your opponent controls.",
            "Every creature on the opposing battlefield is destroyed.",
            "Destroy all creatures on your opponent's side.",
            "Destroy every opposing creature in play.",
            "Mark every creature your opponent controls for destruction.",
            "Destroy each creature on the opposing battlefield.",
            "All creatures your opponent controls are destroyed.",
            "Destroy the creatures on your opponent's battlefield.",
            "Apply destruction to every opposing creature.",
        ],
        "life.loss": [
            "Then you lose {life_loss} life.",
            "Afterward, lose {life_loss} life.",
            "You lose {life_loss} life next.",
            "Then reduce your life total by {life_loss}.",
            "After the destruction, you lose {life_loss} life.",
            "You then pay {life_loss} life.",
            "Next, your life total drops by {life_loss}.",
            "Afterward, your life decreases by {life_loss}.",
            "Lose a total of {life_loss} life afterward.",
            "The destruction is followed by you losing {life_loss} life.",
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

    @simulate(evidence={'text': ('destroy.effect', 'life.loss'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_0_normal(self):
        return self._board_scene(0, 0, offset=0)

    @simulate(evidence={'text': ('destroy.effect', 'life.loss'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_0_normal(self):
        return self._board_scene(1, 0, offset=0)

    @simulate(evidence={'text': ('destroy.effect', 'life.loss'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_1_normal(self):
        return self._board_scene(0, 1, offset=0)

    @simulate(evidence={'text': ('destroy.effect', 'life.loss'), 'fields': ('mana_cost',)})
    def simulate_self_1_enemy_1_normal(self):
        return self._board_scene(1, 1, offset=0)

    @simulate(evidence={'text': ('destroy.effect', 'life.loss'), 'fields': ('mana_cost',)})
    def simulate_self_3_enemy_3_normal(self):
        return self._board_scene(3, 3, offset=0)

    @simulate(evidence={'text': ('destroy.effect', 'life.loss'), 'fields': ('mana_cost',)})
    def simulate_self_0_enemy_5_normal(self):
        return self._board_scene(0, 5, offset=0)

    @simulate(evidence={'text': ('destroy.effect', 'life.loss'), 'fields': ('mana_cost',)})
    def simulate_self_5_enemy_0_normal(self):
        return self._board_scene(5, 0, offset=0)

    @simulate(evidence={'text': ('destroy.effect', 'life.loss'), 'fields': ('mana_cost',)})
    def simulate_protected_battlefields(self):
        return self._board_scene(3, 3, protected=True)

    @simulate(evidence={'text': ('destroy.effect', 'life.loss'), 'fields': ('mana_cost',)})
    def simulate_life_lethal_over(self):
        return self._board_scene(1, 2, life=self.card.effect_params["life_loss"] + -1)

    @simulate(evidence={'text': ('destroy.effect', 'life.loss'), 'fields': ('mana_cost',)})
    def simulate_life_lethal_equal(self):
        return self._board_scene(1, 2, life=self.card.effect_params["life_loss"] + 0)

    @simulate(evidence={'text': ('destroy.effect', 'life.loss'), 'fields': ('mana_cost',)})
    def simulate_life_survives(self):
        return self._board_scene(1, 2, life=self.card.effect_params["life_loss"] + 1)

