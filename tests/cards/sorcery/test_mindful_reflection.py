from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest
from pycards.land.Plains.model import Plains


class TestMindful_Reflection(CardTestCaseBase):
    async def test_mindful_reflection_draw_two_discard_one(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Mindful_Reflection/model.py", "Mindful_Reflection")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.library = [Forest(env.p1), Plains(env.p1)]
        hand_before = len(env.p1.hand)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before + 1)

    async def test_mindful_reflection_discard_reduces_net_hand_gain(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Mindful_Reflection/model.py", "Mindful_Reflection")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = [Forest(env.p1), Plains(env.p1)]
        env.p1.hand.clear()
        env.put_in_hand(Forest(env.p1), env.p1)
        env.put_in_hand(card, env.p1)
        hand_before = len(env.p1.hand)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before)
        self.assertEqual(len(env.p1.library), 0)
        self.assertTrue(any(c.name == "Mindful Reflection" for c in env.p1.graveyard))

    async def test_mindful_reflection_opponent_life_unchanged(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Mindful_Reflection/model.py", "Mindful_Reflection")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = [Forest(env.p1), Plains(env.p1)]
        opp = env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp)
