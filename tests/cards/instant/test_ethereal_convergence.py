from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestEthereal_Convergence(CardTestCaseBase):
    async def test_ethereal_convergence_returns_all_creatures_to_hands(self):
        card_cls = load_card_class_from_path("pycards/Instant/Ethereal_Convergence/model.py", "Ethereal_Convergence")
        env = self.make_env()
        card = card_cls(env.p1)

        c1 = env.put_creatures(env.p1, "Self C", 2, 2, 1)[0]
        c2 = env.put_creatures(env.p2, "Enemy C", 2, 2, 1)[0]
        p1_hand_before = len(env.p1.hand)
        p2_hand_before = len(env.p2.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(c1), "unknown")
        self.assertEqual(env.card_zone(c2), "unknown")
        self.assertEqual(len(env.p1.hand), p1_hand_before + 1)
        self.assertEqual(len(env.p2.hand), p2_hand_before + 1)

    async def test_ethereal_convergence_empty_battlefields_still_resolves(self):
        card_cls = load_card_class_from_path("pycards/Instant/Ethereal_Convergence/model.py", "Ethereal_Convergence")
        env = self.make_env()
        card = card_cls(env.p1)
        hand_before = len(env.p1.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertFalse(env.p1.battlefield)
        self.assertFalse(env.p2.battlefield)
        self.assertEqual(len(env.p1.hand), hand_before)

    async def test_ethereal_convergence_player_life_totals_unchanged(self):
        card_cls = load_card_class_from_path("pycards/Instant/Ethereal_Convergence/model.py", "Ethereal_Convergence")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p1, "A", 2, 2, 1)
        env.put_creatures(env.p2, "B", 2, 2, 1)
        p1l, p2l = env.p1.life, env.p2.life

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, p1l)
        self.assertEqual(env.p2.life, p2l)
