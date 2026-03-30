from unittest.mock import patch

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestShadow_Stalker(CardTestCaseBase):
    async def test_shadow_stalker_has_hexproof(self):
        card_cls = load_card_class_from_path("pycards/creature/Shadow_Stalker/model.py", "Shadow_Stalker")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        stalker = env.get_battlefield_creature(env.p1, "Shadow Stalker")
        self.assert_state(stalker, {"zone": "battlefield", "state": (3, 3), "flags": {"Hexproof": True}})

    async def test_shadow_stalker_attack_forces_discard(self):
        card_cls = load_card_class_from_path("pycards/creature/Shadow_Stalker/model.py", "Shadow_Stalker")
        env = self.make_env()
        card = card_cls(env.p1)

        hand_before = len(env.p2.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        stalker = env.get_battlefield_creature(env.p1, "Shadow Stalker")
        await env.simulate_combat(stalker)
        self.assertEqual(len(env.p2.hand), hand_before - 1)

    async def test_shadow_stalker_attack_skips_discard_when_opponent_hand_empty(self):
        card_cls = load_card_class_from_path("pycards/creature/Shadow_Stalker/model.py", "Shadow_Stalker")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p2.hand.clear()
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        stalker = env.get_battlefield_creature(env.p1, "Shadow Stalker")
        await env.simulate_combat(stalker)
        self.assertEqual(len(env.p2.hand), 0)

    async def test_shadow_stalker_blocked_attack_still_forces_discard(self):
        card_cls = load_card_class_from_path("pycards/creature/Shadow_Stalker/model.py", "Shadow_Stalker")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "Chunky Blocker", 1, 5, 1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        stalker = env.get_battlefield_creature(env.p1, "Shadow Stalker")
        blocker = env.p2.battlefield[0]
        hand_before = len(env.p2.hand)

        def _discard_first(seq):
            return seq[0]

        with patch("random.choice", side_effect=_discard_first):
            await env.simulate_combat(stalker, blocker)

        self.assertEqual(env.p2.life, 20)
        self.assertEqual(len(env.p2.hand), hand_before - 1)
