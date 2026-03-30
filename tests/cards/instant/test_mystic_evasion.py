from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest


class TestMystic_Evasion(CardTestCaseBase):
    async def test_mystic_evasion_bounces_current_attacker_and_draws(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Evasion/model.py", "Mystic_Evasion")
        env = self.make_env()
        card = card_cls(env.p1)

        attacker = env.put_creatures(env.p2, "Attacker", 3, 3, 1)[0]
        env.room.attacker = attacker
        env.p1.library = [Forest(env.p1)]
        p2_hand_before = len(env.p2.hand)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.hand), p2_hand_before + 1)

    async def test_mystic_evasion_no_attacker_still_draws(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Evasion/model.py", "Mystic_Evasion")
        env = self.make_env()
        card = card_cls(env.p1)
        env.room.attacker = None
        env.p1.library = [Forest(env.p1)]
        hand_before = len(env.p1.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before + 1)

    async def test_mystic_evasion_empty_library_still_bounces_attacker(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Evasion/model.py", "Mystic_Evasion")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library.clear()

        attacker = env.put_creatures(env.p2, "Attacker", 3, 3, 1)[0]
        env.room.attacker = attacker
        p1_hand_before = len(env.p1.hand)
        p2_hand_before = len(env.p2.hand)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertGreater(len(env.p2.hand), p2_hand_before)
        self.assertEqual(len(env.p1.hand), p1_hand_before)
        self.assertIsNone(env.find_card_by_name(env.p2, "Attacker", zones=("battlefield",)))
