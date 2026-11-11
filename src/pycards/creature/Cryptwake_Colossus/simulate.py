from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.creature.Cryptwake_Colossus.model import Cryptwake_Colossus


@bind_card(Cryptwake_Colossus)
class Cryptwake_Colossus_Simulation(Card_Simulation):
    text_parts = {
        "keyword.lifelink": [
            "Lifelink.",
            "This creature has lifelink.",
            "{card_name} has lifelink.",
            "This creature has the lifelink ability.",
            "{card_name} has the lifelink ability.",
            "Lifelink (Damage dealt by this creature also causes you to gain that much life).",
            "Damage dealt by this creature also causes you to gain that much life.",
            "Damage dealt by {card_name} also causes you to gain that much life.",
            "This creature has lifelink, so its damage also causes you to gain that much life.",
            "{card_name} has lifelink, so its damage also causes you to gain that much life.",
        ],
        "enter.trigger": [
            "When {card_name} enters the battlefield,",
            "Whenever {card_name} enters the battlefield,",
            "When this creature enters the battlefield,",
            "Whenever this creature enters the battlefield,",
            "When {card_name} enters play,",
            "Whenever {card_name} enters play,",
            "When this creature enters play,",
            "Whenever this creature enters play,",
            "When {card_name} comes into play,",
            "Whenever {card_name} comes into play,",
        ],
        "enter.life_loss": [
            "your opponent loses {life_loss} life",
            "the opposing player loses {life_loss} life",
            "your opponent loses a total of {life_loss} life",
            "the opposing player loses a total of {life_loss} life",
            "your opponent loses an amount of life equal to {life_loss}",
            "the opposing player loses an amount of life equal to {life_loss}",
            "reduce your opponent's life total by {life_loss}",
            "reduce the opposing player's life total by {life_loss}",
            "{card_name} causes your opponent to lose {life_loss} life",
            "this creature causes your opponent to lose {life_loss} life",
        ],
        "enter.heal": [
            "and you gain {heal} life.",
            "and gain {heal} life.",
            "and you gain a total of {heal} life.",
            "and gain a total of {heal} life.",
            "and increase your life total by {heal}.",
            "and you increase your life total by {heal}.",
            "and restore {heal} life.",
            "and you restore {heal} life.",
            "and gain an amount of life equal to {heal}.",
            "and you gain an amount of life equal to {heal}.",
        ],
    }

    def _simulate_drain(self, life, opponent_life):
        self.scenario_prepare()
        if not (1 <= life <= self.player.ini_life and 1 <= opponent_life <= self.player.opponent.ini_life):
            return self.scenario_skip()
        self.player.life = life
        self.player.opponent.life = opponent_life
        return self.scenario_cast()

    @simulate(evidence={'text': ('enter.trigger', 'enter.life_loss', 'enter.heal'), 'fields': ('mana_cost',)})
    def simulate_enter_injured_below_lethal(self):
        return self._simulate_drain(1, self.card.effect_params["life_loss"] - 1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.life_loss', 'enter.heal'), 'fields': ('mana_cost',)})
    def simulate_enter_injured_exact_lethal(self):
        return self._simulate_drain(1, self.card.effect_params["life_loss"])

    @simulate(evidence={'text': ('enter.trigger', 'enter.life_loss', 'enter.heal'), 'fields': ('mana_cost',)})
    def simulate_enter_injured_survives(self):
        return self._simulate_drain(1, self.card.effect_params["life_loss"] + 1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.life_loss', 'enter.heal'), 'fields': ('mana_cost',)})
    def simulate_enter_near_full_below_lethal(self):
        return self._simulate_drain(self.player.ini_life - 1, self.card.effect_params["life_loss"] - 1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.life_loss', 'enter.heal'), 'fields': ('mana_cost',)})
    def simulate_enter_near_full_exact_lethal(self):
        return self._simulate_drain(self.player.ini_life - 1, self.card.effect_params["life_loss"])

    @simulate(evidence={'text': ('enter.trigger', 'enter.life_loss', 'enter.heal'), 'fields': ('mana_cost',)})
    def simulate_enter_near_full_survives(self):
        return self._simulate_drain(self.player.ini_life - 1, self.card.effect_params["life_loss"] + 1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.life_loss', 'enter.heal'), 'fields': ('mana_cost',)})
    def simulate_enter_full_below_lethal(self):
        return self._simulate_drain(self.player.ini_life, self.card.effect_params["life_loss"] - 1)

    @simulate(evidence={'text': ('enter.trigger', 'enter.life_loss', 'enter.heal'), 'fields': ('mana_cost',)})
    def simulate_enter_full_exact_lethal(self):
        return self._simulate_drain(self.player.ini_life, self.card.effect_params["life_loss"])

    @simulate(evidence={'text': ('enter.trigger', 'enter.life_loss', 'enter.heal'), 'fields': ('mana_cost',)})
    def simulate_enter_full_survives(self):
        return self._simulate_drain(self.player.ini_life, self.card.effect_params["life_loss"] + 1)

    @simulate(evidence={'fields': ('mana_cost',)})
    def simulate_cast_without_mana(self):
        self.scenario_prepare()
        return self.scenario_cast(provide_mana=False)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives(self):
        return self.scenario_combat(False, True, False, margin=0)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(False, True, False, margin=1)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive(self):
        return self.scenario_combat(False, False, False, margin=0)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_survive_beyond_boundary(self):
        return self.scenario_combat(False, False, False, margin=1)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies(self):
        return self.scenario_combat(False, False, True, margin=0)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(False, False, True, margin=1)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die(self):
        return self.scenario_combat(False, True, True, margin=0)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_attack_both_die_beyond_boundary(self):
        return self.scenario_combat(False, True, True, margin=1)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_dies_self_survives(self):
        return self.scenario_combat(True, True, False, margin=0)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_dies_self_survives_beyond_boundary(self):
        return self.scenario_combat(True, True, False, margin=1)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_survive(self):
        return self.scenario_combat(True, False, False, margin=0)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_survive_beyond_boundary(self):
        return self.scenario_combat(True, False, False, margin=1)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_survives_self_dies(self):
        return self.scenario_combat(True, False, True, margin=0)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_opponent_survives_self_dies_beyond_boundary(self):
        return self.scenario_combat(True, False, True, margin=1)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_die(self):
        return self.scenario_combat(True, True, True, margin=0)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'defend', 'special_type')})
    def simulate_defend_both_die_beyond_boundary(self):
        return self.scenario_combat(True, True, True, margin=1)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'special_type')})
    def simulate_attack_empty_board(self):
        return self.scenario_unblocked(False)

    @simulate(evidence={'text': ('keyword.lifelink',), 'fields': ('attack', 'special_type')})
    def simulate_attack_opponent_passes(self):
        return self.scenario_unblocked(True)

