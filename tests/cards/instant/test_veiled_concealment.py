from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest


class TestVeiled_Concealment(CardTestCaseBase):
    async def test_veiled_concealment_unblockable_and_draw(self):
        card_cls = load_card_class_from_path("pycards/Instant/Veiled_Concealment/model.py", "Veiled_Concealment")
        env = self.make_env()
        card = card_cls(env.p1)

        creature = env.put_creatures(env.p1, "Sneak", 2, 2, 1)[0]
        env.p1.library = [Forest(env.p1)]
        hand_before = len(env.p1.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before + 1)
        self.assertTrue(creature.get_flag("unblockable"))

    async def test_veiled_concealment_empty_library_still_marks_unblockable(self):
        card_cls = load_card_class_from_path("pycards/Instant/Veiled_Concealment/model.py", "Veiled_Concealment")
        env = self.make_env()
        card = card_cls(env.p1)
        creature = env.put_creatures(env.p1, "Sneak", 2, 2, 1)[0]
        env.p1.library.clear()
        hand_before = len(env.p1.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertTrue(creature.get_flag("unblockable"))
        self.assertEqual(len(env.p1.hand), hand_before)
        self.assertTrue(env.p1.get_flag("die"))

    async def test_veiled_concealment_opponent_life_unchanged(self):
        card_cls = load_card_class_from_path("pycards/Instant/Veiled_Concealment/model.py", "Veiled_Concealment")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p1, "Sneak", 2, 2, 1)
        env.p1.library = [Forest(env.p1)]
        opp_before = env.p2.life

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp_before)
