from unittest.mock import AsyncMock, patch

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestVoidwisp_Harbinger(CardTestCaseBase):
    async def test_voidwisp_harbinger_keywords_and_scry(self):
        card_cls = load_card_class_from_path("pycards/creature/Voidwisp_Harbinger/model.py", "Voidwisp_Harbinger")
        env = self.make_env()
        card = card_cls(env.p1)

        library_before = len(env.p1.library)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        harbinger = env.get_battlefield_creature(env.p1, "Voidwisp Harbinger")
        self.assert_state(harbinger, {
            "zone": "battlefield",
            "state": (2, 4),
            "flags": {"Flash": True, "flying": True},
        })
        self.assertEqual(len(env.p1.library), library_before)
        self.assertEqual(env.p2.life, 20)

    async def test_voidwisp_harbinger_etb_invokes_scry_two(self):
        card_cls = load_card_class_from_path("pycards/creature/Voidwisp_Harbinger/model.py", "Voidwisp_Harbinger")
        env = self.make_env()
        card = card_cls(env.p1)
        with patch.object(card, "Scry", new_callable=AsyncMock) as mock_scry:
            result = await env.play_card(card, env.p1)
            await env.resolve_stack()
        self.assertTrue(result[0])
        mock_scry.assert_awaited_once()
        args = mock_scry.await_args[0]
        self.assertEqual(args[2], 2)

    async def test_voidwisp_harbinger_etb_does_not_change_opponent_hand(self):
        card_cls = load_card_class_from_path("pycards/creature/Voidwisp_Harbinger/model.py", "Voidwisp_Harbinger")
        env = self.make_env()
        card = card_cls(env.p1)
        opp_hand_before = len(env.p2.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.hand), opp_hand_before)
