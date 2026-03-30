from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest


class TestCelestial_Intervention(CardTestCaseBase):
    async def test_celestial_intervention_grants_indestructible_and_draws(self):
        card_cls = load_card_class_from_path("pycards/Instant/Celestial_Intervention/model.py", "Celestial_Intervention")
        env = self.make_env()
        card = card_cls(env.p1)

        creature = env.put_creatures(env.p1, "Self C", 2, 2, 1)[0]
        env.p1.library = [Forest(env.p1)]
        hand_before = len(env.p1.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before + 1)
        self.assert_state(creature, {"buffs_contains": ["Indestructible"]})

    async def test_celestial_intervention_empty_battlefield_still_draws(self):
        card_cls = load_card_class_from_path("pycards/Instant/Celestial_Intervention/model.py", "Celestial_Intervention")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = [Forest(env.p1)]
        hand_before = len(env.p1.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before + 1)
        self.assertFalse(env.p1.battlefield)

    async def test_celestial_intervention_empty_library_still_grants_indestructible(self):
        card_cls = load_card_class_from_path("pycards/Instant/Celestial_Intervention/model.py", "Celestial_Intervention")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library.clear()

        creature = env.put_creatures(env.p1, "Protected", 2, 2, 1)[0]
        hand_before = len(env.p1.hand)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assert_state(creature, {"buffs_contains": ["Indestructible"]})
        self.assertEqual(len(env.p1.hand), hand_before)
