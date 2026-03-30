from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from unittest.mock import AsyncMock


class TestMystic_Reversal(CardTestCaseBase):
    async def test_mystic_reversal_casts_without_crash(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Mystic_Reversal/model.py", "Mystic_Reversal")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])

    async def test_mystic_reversal_calls_undo_stack_when_available(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Mystic_Reversal/model.py", "Mystic_Reversal")
        env = self.make_env()
        card = card_cls(env.p1)
        card.undo_stack = AsyncMock(return_value=(None, None))

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        card.undo_stack.assert_awaited()

    async def test_mystic_reversal_resolves_to_graveyard(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Mystic_Reversal/model.py", "Mystic_Reversal")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(card), "graveyard")
