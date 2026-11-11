from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.sorcery.Unyielding_Resolve.model import Unyielding_Resolve


@bind_card(Unyielding_Resolve)
class Unyielding_Resolve_Simulation(Card_Simulation):
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
        "indestructible.effect": [
            "Each also gains indestructible until your turn ends.",
            "Each receives indestructible until your turn ends.",
            "Give each indestructible until your turn ends.",
            "Each has indestructible until your turn ends.",
            "Until your turn ends, each also has indestructible.",
            "Each gains the indestructible ability until your turn ends.",
            "Grant each indestructible until your turn ends.",
            "Until your turn ends, each receives indestructible.",
            "Until your turn ends, each also gains indestructible.",
            "Each is granted indestructible until your turn ends.",
        ],
        "keyword.effect": [
            "Each also gains lifelink until your turn ends.",
            "Each receives lifelink until your turn ends.",
            "Give each lifelink until your turn ends.",
            "Each has lifelink until your turn ends.",
            "Until your turn ends, each also has lifelink.",
            "Each gains the lifelink ability until your turn ends.",
            "Grant each lifelink until your turn ends.",
            "Until your turn ends, each receives lifelink.",
            "Until your turn ends, each also gains lifelink.",
            "Each is granted lifelink until your turn ends.",
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
                self.scenario_creature(owner, power=2, health=3, flags={'lifelink': True} if existing_keyword else {})
        return self.scenario_cast()

    @simulate(evidence={'text': ('target.scope', 'indestructible.effect', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_group_self_0_enemy_0(self):
        return self._group_scene(0, 0)

    @simulate(evidence={'text': ('target.scope', 'indestructible.effect', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_group_self_0_enemy_3(self):
        return self._group_scene(0, 3)

    @simulate(evidence={'text': ('target.scope', 'indestructible.effect', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_group_self_1_enemy_0(self):
        return self._group_scene(1, 0)

    @simulate(evidence={'text': ('target.scope', 'indestructible.effect', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_group_self_1_enemy_1(self):
        return self._group_scene(1, 1)

    @simulate(evidence={'text': ('target.scope', 'indestructible.effect', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_group_self_3_enemy_3(self):
        return self._group_scene(3, 3)

    @simulate(evidence={'text': ('target.scope', 'indestructible.effect', 'keyword.effect'), 'fields': ('mana_cost',)})
    def simulate_group_existing_keyword(self):
        return self._group_scene(3, 1, True)

