from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestTime_Reversal(CardTestCaseBase):
    async def test_time_reversal_replaces_opponent_stack_effects(self):
        card_cls = load_card_class_from_path("pycards/Instant/Time_Reversal/model.py", "Time_Reversal")
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)

        async def _orig():
            return "orig"

        original_spell = spell_cls(env.p2)
        env.room.stack.append((_orig, original_spell))
        env.room.flag_dict["bullet_time"] = True

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.room.stack), 0)
        self.assertEqual(env.p1.life, 20)
        self.assertEqual(env.p2.life, 20)

    async def test_time_reversal_blocked_when_stack_top_is_nonspell(self):
        """Instant_Undo check_can_use only inspects stack[-1]; a creature on top forbids cast even if a spell is below."""
        card_cls = load_card_class_from_path("pycards/Instant/Time_Reversal/model.py", "Time_Reversal")
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)

        async def _orig():
            return "orig"

        dummy_creature = env.create_creature(env.p2, "Stack Creature", 1, 1)
        opp_spell = spell_cls(env.p2)
        env.room.stack.append((_orig, opp_spell))
        env.room.stack.append((_orig, dummy_creature))
        env.room.flag_dict["bullet_time"] = True

        result = await env.play_card(card, env.p1)
        self.assertFalse(result[0])

    async def test_time_reversal_blocked_without_bullet_time(self):
        card_cls = load_card_class_from_path("pycards/Instant/Time_Reversal/model.py", "Time_Reversal")
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)

        async def _orig():
            return "orig"

        env.room.stack.append((_orig, spell_cls(env.p2)))
        env.room.flag_dict["bullet_time"] = False

        result = await env.play_card(card, env.p1)
        self.assertFalse(result[0])
        self.assertEqual(len(env.room.stack), 1)

    async def test_time_reversal_blocked_on_empty_stack(self):
        card_cls = load_card_class_from_path("pycards/Instant/Time_Reversal/model.py", "Time_Reversal")
        env = self.make_env()
        card = card_cls(env.p1)
        env.room.stack.clear()
        env.room.flag_dict["bullet_time"] = True

        result = await env.play_card(card, env.p1)
        self.assertFalse(result[0])

    async def test_time_reversal_works_when_top_is_opponent_sorcery(self):
        """undo_range includes Sorcery; stack top may be a Sorcery card object."""
        card_cls = load_card_class_from_path("pycards/Instant/Time_Reversal/model.py", "Time_Reversal")
        sorcery_cls = load_card_class_from_path("pycards/sorcery/Naturalize/model.py", "Naturalize")
        env = self.make_env()
        card = card_cls(env.p1)

        async def _orig():
            return "orig"

        env.room.stack.append((_orig, sorcery_cls(env.p2)))
        env.room.flag_dict["bullet_time"] = True

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.room.stack), 0)
