from unittest.mock import patch

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestVengeful_Retribution(CardTestCaseBase):
    async def test_vengeful_retribution_forces_multiple_sacrifices(self):
        card_cls = load_card_class_from_path("pycards/Instant/Vengeful_Retribution/model.py", "Vengeful_Retribution")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_creatures(env.p2, "Enemy A", 2, 2, 1)
        env.put_creatures(env.p2, "Enemy B", 3, 3, 1)
        env.put_creatures(env.p2, "Enemy C", 4, 4, 1)
        before = len(env.p2.battlefield)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertLessEqual(len(env.p2.battlefield), before - 2)

    async def test_vengeful_retribution_single_creature_no_followup_damage(self):
        """With one creature, only one sacrifice occurs and no random damage target remains."""
        card_cls = load_card_class_from_path("pycards/Instant/Vengeful_Retribution/model.py", "Vengeful_Retribution")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "Only One", 4, 4, 1)
        env.p2.life = 20
        life_before = env.p2.life

        with patch("random.sample", side_effect=lambda pop, k: pop[:k]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.battlefield), 0)
        self.assertEqual(env.p2.life, life_before)

    async def test_vengeful_retribution_empty_opponent_board_is_no_op(self):
        card_cls = load_card_class_from_path("pycards/Instant/Vengeful_Retribution/model.py", "Vengeful_Retribution")
        env = self.make_env()
        card = card_cls(env.p1)
        self.assertFalse(env.p2.battlefield)
        life = env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, life)
        self.assertFalse(env.p2.battlefield)
