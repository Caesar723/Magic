from unittest.mock import AsyncMock
from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestMystic_Reversal(CardTestCaseBase):
    async def test_mystic_reversal_uses_undo_stack(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Reversal/model.py", "Mystic_Reversal")
        env = self.make_env()
        card = card_cls(env.p1)

        async def _noop():
            return None

        env.room.stack.append((_noop, env.create_creature(env.p2, "Stack", 2, 2)))
        env.room.flag_dict["bullet_time"] = True
        card.undo_stack = AsyncMock(return_value=(None, env.create_creature(env.p2, "Stack", 2, 2)))
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        card.undo_stack.assert_awaited_once()

    async def test_mystic_reversal_counters_creature_spell_on_stack(self):
        creature_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Reversal/model.py", "Mystic_Reversal")
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
        self.assertEqual(env.card_zone(stack_creature), "graveyard")

    async def test_mystic_reversal_controller_life_unchanged(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Reversal/model.py", "Mystic_Reversal")
        env = self.make_env()
        card = card_cls(env.p1)
        life_before = env.p1.life

        async def _noop():
            return None

        env.room.stack.append((_noop, env.create_creature(env.p2, "Stack", 2, 2)))
        env.room.flag_dict["bullet_time"] = True
        card.undo_stack = AsyncMock(return_value=(None, env.create_creature(env.p2, "Stack", 2, 2)))
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, life_before)
