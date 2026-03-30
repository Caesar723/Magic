from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest
from unittest.mock import AsyncMock


class TestEphemeral_Vision(CardTestCaseBase):
    async def test_ephemeral_vision_draw_then_scry(self):
        card_cls = load_card_class_from_path("pycards/Instant/Ephemeral_Vision/model.py", "Ephemeral_Vision")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.library = [Forest(env.p1)]
        hand_before = len(env.p1.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before + 1)

    async def test_ephemeral_vision_calls_scry_two(self):
        card_cls = load_card_class_from_path("pycards/Instant/Ephemeral_Vision/model.py", "Ephemeral_Vision")
        env = self.make_env()
        card = card_cls(env.p1)
        card.Scry = AsyncMock(return_value=None)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        card.Scry.assert_awaited_once_with(env.p1, env.p2, 2)

    async def test_ephemeral_vision_preserves_opponent_library_size(self):
        card_cls = load_card_class_from_path("pycards/Instant/Ephemeral_Vision/model.py", "Ephemeral_Vision")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = [Forest(env.p1)]
        opp_lib_before = len(env.p2.library)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.library), opp_lib_before)
