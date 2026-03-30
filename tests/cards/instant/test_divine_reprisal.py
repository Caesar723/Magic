from unittest.mock import patch

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestDivine_Reprisal(CardTestCaseBase):
    async def test_divine_reprisal_destroys_target_creature(self):
        card_cls = load_card_class_from_path("pycards/Instant/Divine_Reprisal/model.py", "Divine_Reprisal")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Reprisal Target", 2, 2, 1)[0]
        env.room.attacker = target
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(target), "graveyard")

    async def test_divine_reprisal_does_not_destroy_non_attacker(self):
        card_cls = load_card_class_from_path("pycards/Instant/Divine_Reprisal/model.py", "Divine_Reprisal")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Safe Target", 2, 2, 1)[0]
        env.room.attacker = None
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(target), "battlefield")

    async def test_divine_reprisal_does_not_destroy_selected_non_attacker(self):
        card_cls = load_card_class_from_path("pycards/Instant/Divine_Reprisal/model.py", "Divine_Reprisal")
        env = self.make_env()
        card = card_cls(env.p1)

        not_attacker = env.put_creatures(env.p2, "Not Attacking", 2, 2, 1)[0]
        real_attacker = env.put_creatures(env.p2, "Actual Attacker", 3, 3, 1)[0]
        env.room.attacker = real_attacker

        def _pick_first(seq):
            return seq[0]

        with patch("random.choice", side_effect=_pick_first):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(not_attacker), "battlefield")
        self.assertEqual(env.card_zone(real_attacker), "battlefield")
