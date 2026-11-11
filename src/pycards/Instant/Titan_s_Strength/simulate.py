from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Titan_s_Strength.model import Titan_s_Strength


@bind_card(Titan_s_Strength)
class Titan_s_Strength_Simulation(Card_Simulation):
    text_parts = {
        "target.scope": [
            "This affects all creatures you control.",
            "Apply the following effects to each creature you control.",
            "Each creature on your battlefield receives the following effects.",
            "The following effects apply to all your creatures.",
            "Apply this to every creature under your control.",
            "Every creature on your side receives the following effects.",
            "Affect each of the creatures under your control.",
            "Apply these effects to all creatures on your battlefield.",
            "All creatures you control are affected.",
            "Give every creature you control the following effects.",
        ],
        "state.effect": [
            "Each gets +{power_bonus}/+{toughness_bonus} until your turn ends.",
            "Give each +{power_bonus}/+{toughness_bonus} until your turn ends.",
            "Each gains +{power_bonus}/+{toughness_bonus} until your turn ends.",
            "Until your turn ends, each gets +{power_bonus}/+{toughness_bonus}.",
            "Increase each creature's power by {power_bonus} and toughness by {toughness_bonus} until your turn ends.",
            "Each receives +{power_bonus}/+{toughness_bonus} until your turn ends.",
            "Its power increases by {power_bonus} and each creature's toughness by {toughness_bonus} until your turn ends.",
            "Grant each +{power_bonus}/+{toughness_bonus} until your turn ends.",
            "Each gets an extra {power_bonus} power and {toughness_bonus} toughness until your turn ends.",
            "Until your turn ends, add {power_bonus} to each creature's power and {toughness_bonus} to each creature's toughness.",
        ],
        "keyword.effect": [
            "Each also gains trample until your turn ends.",
            "Each receives trample until your turn ends.",
            "Give each trample until your turn ends.",
            "Each has trample until your turn ends.",
            "Until your turn ends, each also has trample.",
            "Each gains the trample ability until your turn ends.",
            "Grant each trample until your turn ends.",
            "Until your turn ends, each receives trample.",
            "Until your turn ends, each also gains trample.",
            "Each is granted trample until your turn ends.",
        ],
    }

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    def _group_scene(self, own_count, enemy_count, existing_keyword=False):
        self.scenario_prepare()
        for owner, count in ((self.player, own_count), (self.player.opponent, enemy_count)):
            for _ in range(count):
                self.scenario_creature(owner, power=2, health=3, flags={'Trample': True} if existing_keyword else {})
        return self.scenario_cast()

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_group_self_0_enemy_0(self):
        return self._group_scene(0, 0)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_group_self_0_enemy_3(self):
        return self._group_scene(0, 3)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_group_self_1_enemy_0(self):
        return self._group_scene(1, 0)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_group_self_1_enemy_1(self):
        return self._group_scene(1, 1)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_group_self_3_enemy_3(self):
        return self._group_scene(3, 3)

    @simulate(evidence={'text': ('target.scope', 'state.effect', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_group_existing_keyword(self):
        return self._group_scene(3, 1, True)

