from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest


class TestAquatic_Evasion(CardTestCaseBase):
    async def test_aquatic_evasion_grants_hexproof_and_draws(self):
        card_cls = load_card_class_from_path("pycards/Instant/Aquatic_Evasion/model.py", "Aquatic_Evasion")
        env = self.make_env()
        card = card_cls(env.p1)

        creature = env.put_creatures(env.p1, "Self C", 2, 2, 1)[0]
        env.p1.library = [Forest(env.p1)]
        hand_before = len(env.p1.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before + 1)
        self.assertTrue(creature.get_flag("Hexproof"))

    async def test_aquatic_evasion_empty_library_still_grants_hexproof(self):
        card_cls = load_card_class_from_path("pycards/Instant/Aquatic_Evasion/model.py", "Aquatic_Evasion")
        env = self.make_env()
        card = card_cls(env.p1)

        creature = env.put_creatures(env.p1, "Solo", 1, 1, 1)[0]
        env.p1.library = []
        hand_before = len(env.p1.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before)
        self.assertTrue(creature.get_flag("Hexproof"))

    async def test_aquatic_evasion_does_not_grant_hexproof_to_opponent_creatures(self):
        card_cls = load_card_class_from_path("pycards/Instant/Aquatic_Evasion/model.py", "Aquatic_Evasion")
        env = self.make_env()
        card = card_cls(env.p1)
        ours = env.put_creatures(env.p1, "Ours", 2, 2, 1)[0]
        theirs = env.put_creatures(env.p2, "Theirs", 2, 2, 1)[0]
        env.p1.library = [Forest(env.p1)]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertTrue(ours.get_flag("Hexproof"))
        self.assertFalse(theirs.get_flag("Hexproof"))
