from unittest.mock import AsyncMock

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestMystic_Evocation(CardTestCaseBase):
    async def test_mystic_evocation_counters_noncreature_and_scry(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Evocation/model.py", "Mystic_Evocation")
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
        self.assertEqual(len(env.room.stack), 0)

    async def test_mystic_evocation_blocked_when_stack_top_is_creature_spell(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Evocation/model.py", "Mystic_Evocation")
        env = self.make_env()
        card = card_cls(env.p1)
        stack_creature = env.put_creatures(env.p2, "Stack C", 2, 2, 1)[0]

        async def _noop():
            return None

        env.room.stack.append((_noop, stack_creature))
        env.room.flag_dict["bullet_time"] = True
        result = await env.play_card(card, env.p1)
        self.assertFalse(result[0])

    async def test_mystic_evocation_invokes_scry_after_countering_spell(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Evocation/model.py", "Mystic_Evocation")
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)
        card.Scry = AsyncMock(return_value=None)

        async def _noop():
            return None

        env.room.stack.append((_noop, spell_cls(env.p2)))
        env.room.flag_dict["bullet_time"] = True
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        card.Scry.assert_awaited()
