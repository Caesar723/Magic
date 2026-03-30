from unittest.mock import AsyncMock
from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest


class TestMindweave(CardTestCaseBase):
    async def test_mindweave_counters_and_draws(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mindweave/model.py", "Mindweave")
        env = self.make_env()
        card = card_cls(env.p1)

        async def _noop():
            return None

        env.room.stack.append((_noop, env.create_creature(env.p2, "Stack", 2, 2)))
        env.room.flag_dict["bullet_time"] = True
        card.undo_stack = AsyncMock(return_value=(None, env.create_creature(env.p2, "Stack", 2, 2)))
        env.p1.library = [Forest(env.p1)]
        hand_before = len(env.p1.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before + 1)

    async def test_mindweave_counters_noncreature_spell_on_stack_still_draws(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mindweave/model.py", "Mindweave")
        spell_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)

        async def _noop():
            return None

        env.room.stack.append((_noop, spell_cls(env.p2)))
        env.room.flag_dict["bullet_time"] = True
        card.undo_stack = AsyncMock(return_value=(None, spell_cls(env.p2)))
        env.p1.library = [Forest(env.p1)]
        hand_before = len(env.p1.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before + 1)

    async def test_mindweave_opponent_hand_unchanged_after_counter(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mindweave/model.py", "Mindweave")
        env = self.make_env()
        card = card_cls(env.p1)
        opp_hand_before = len(env.p2.hand)

        async def _noop():
            return None

        env.room.stack.append((_noop, env.create_creature(env.p2, "Stack", 2, 2)))
        env.room.flag_dict["bullet_time"] = True
        card.undo_stack = AsyncMock(return_value=(None, env.create_creature(env.p2, "Stack", 2, 2)))
        env.p1.library = [Forest(env.p1)]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.hand), opp_hand_before)
