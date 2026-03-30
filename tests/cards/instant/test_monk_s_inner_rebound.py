from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestMonk_s_Inner_Rebound(CardTestCaseBase):
    async def test_monk_s_inner_rebound_counters_and_recasts(self):
        card_cls = load_card_class_from_path("pycards/Instant/Monk_s_Inner_Rebound/model.py", "Monk_s_Inner_Rebound")
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)

        async def _noop():
            return None

        env.room.stack.append((_noop, spell_cls(env.p2)))
        env.room.flag_dict["bullet_time"] = True

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])

    async def test_monk_s_inner_rebound_creature_counter_does_not_recast_spell(self):
        """Only Instants (non-undo) and Sorceries are pushed back onto the stack."""
        card_cls = load_card_class_from_path("pycards/Instant/Monk_s_Inner_Rebound/model.py", "Monk_s_Inner_Rebound")
        creature_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)

        stack_creature = creature_cls(env.p2)
        env.p2.battlefield.append(stack_creature)

        async def _noop():
            return None

        env.room.stack.append((_noop, stack_creature))
        env.room.flag_dict["bullet_time"] = True

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.room.stack), 0)
        self.assertEqual(env.card_zone(stack_creature), "graveyard")

    async def test_monk_s_inner_rebound_controller_life_unchanged_after_counter(self):
        card_cls = load_card_class_from_path("pycards/Instant/Monk_s_Inner_Rebound/model.py", "Monk_s_Inner_Rebound")
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)
        async def _noop():
            return None
        env.room.stack.append((_noop, spell_cls(env.p2)))
        env.room.flag_dict["bullet_time"] = True
        life = env.p1.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, life)
