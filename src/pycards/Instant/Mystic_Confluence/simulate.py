from game.card_simulation import bind_card, simulate, Card_Simulation
from pycards.Instant.Mystic_Confluence.model import Mystic_Confluence


@bind_card(Mystic_Confluence)
class Mystic_Confluence_Simulation(Card_Simulation):
    scenario_locks={
        '_stack_scene':('opponent.battlefield', 'self.battlefield', 'self.library'),
    }

    text_parts = {
        "counter.effect": [
            "Counter the top spell.",
            "Counter the spell on top of the stack.",
            "Undo the current topmost spell.",
            "Cancel the spell at the top of the stack.",
            "The current top spell is countered.",
            "Counter whichever spell is on top of the stack.",
            "The topmost pending spell is countered.",
            "Counter the stack's current top spell.",
            "Remove the top spell's pending effect.",
            "Counter the currently pending top spell.",
        ],
        "return.effect": [
            "Return the selected creature to its owner's hand.",
            "Put the target creature into its owner's hand.",
            "The chosen creature returns to its owner's hand.",
            "Move that creature from the battlefield to its owner's hand.",
            "Return the creature you targeted to the hand of its owner.",
            "Put that creature back into its owner's hand.",
            "The targeted creature goes back to its owner's hand.",
            "Return your chosen creature from play to its owner's hand.",
            "Take that creature off the battlefield and put it into its owner's hand.",
            "Move the targeted creature back to its owner's hand.",
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

    def _stack_scene(self, kind="instant", own_stack=False, lower_count=0, role="enemy", target_top=False, library_count=None):
        library_count=self.scenario_count("library",library_count)
        self.scenario_prepare()
        target = self.scenario_stack(kind, own_target=own_stack, lower_count=lower_count)
        for index, item in enumerate(self.room.stack[:-1]):
            if index % 2 == 0:
                old = item["card"]
                owner = old.player.opponent
                zone = "battlefield" if old.type == "Creature" else "graveyard"
                self.unstage_card(old, old.player)
                new = old.copy_for_player(owner)
                self.stage_card(new, owner, zone=zone)
                item["card"] = new
        if target_top and kind == "creature":
            owner = target.player
        else:
            owner = self.player if role == "self" else self.player.opponent
            target = self.scenario_creature(owner, power=2, health=4, flags={})
        subaction = (11 if owner is self.player else 1) + owner.battlefield.index(target)
        if library_count is not None:
            self.scenario_replace_cards(self.player,"library",instant=(library_count, library_count))
            self.player.library = [card for card in self.player.library if card.type == "Instant"][:library_count]
        return self.scenario_cast((subaction,), in_stack=True)

    @simulate(evidence={'text': ('counter.effect', 'return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_stack_instant_own_False_lower_0(self):
        return self._stack_scene('instant', False, 0)

    @simulate(evidence={'text': ('counter.effect', 'return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_stack_instant_own_False_lower_3(self):
        return self._stack_scene('instant', False, 3)

    @simulate(evidence={'text': ('counter.effect', 'return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_stack_instant_own_True_lower_0(self):
        return self._stack_scene('instant', True, 0)

    @simulate(evidence={'text': ('counter.effect', 'return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_stack_instant_own_True_lower_3(self):
        return self._stack_scene('instant', True, 3)

    @simulate(evidence={'text': ('counter.effect', 'return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_stack_sorcery_own_False_lower_0(self):
        return self._stack_scene('sorcery', False, 0)

    @simulate(evidence={'text': ('counter.effect', 'return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_stack_sorcery_own_False_lower_3(self):
        return self._stack_scene('sorcery', False, 3)

    @simulate(evidence={'text': ('counter.effect', 'return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_stack_sorcery_own_True_lower_0(self):
        return self._stack_scene('sorcery', True, 0)

    @simulate(evidence={'text': ('counter.effect', 'return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_stack_sorcery_own_True_lower_3(self):
        return self._stack_scene('sorcery', True, 3)

    @simulate(evidence={'text': ('counter.effect', 'return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_stack_creature_own_False_lower_0(self):
        return self._stack_scene('creature', False, 0)

    @simulate(evidence={'text': ('counter.effect', 'return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_stack_creature_own_False_lower_3(self):
        return self._stack_scene('creature', False, 3)

    @simulate(evidence={'text': ('counter.effect', 'return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_stack_creature_own_True_lower_0(self):
        return self._stack_scene('creature', True, 0)

    @simulate(evidence={'text': ('counter.effect', 'return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_stack_creature_own_True_lower_3(self):
        return self._stack_scene('creature', True, 3)

    @simulate(evidence={'text': ('counter.effect', 'return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_bounce_countered_creature(self):
        return self._stack_scene("creature", target_top=True)

    @simulate(evidence={'text': ('counter.effect', 'return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_bounce_self(self):
        return self._stack_scene(role="self")

    @simulate(evidence={'text': ('counter.effect', 'return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_library_empty(self):
        return self._stack_scene(library_count=0)

    @simulate(evidence={'text': ('counter.effect', 'return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_library_short(self):
        return self._stack_scene(library_count=max(0, self.card.effect_params["draw_count"] - 1))

    @simulate(evidence={'text': ('counter.effect', 'return.effect', 'draw.effect'), 'fields': ('mana_cost',)})
    def simulate_library_exact(self):
        return self._stack_scene(library_count=self.card.effect_params["draw_count"])

