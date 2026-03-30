from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest
from pycards.land.Plains.model import Plains


class TestMindful_Manipulation(CardTestCaseBase):
    async def test_mindful_manipulation_draw_two_put_one_back(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Mindful_Manipulation/model.py", "Mindful_Manipulation")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.library = [Forest(env.p1), Plains(env.p1)]
        hand_before = len(env.p1.hand)
        lib_before = len(env.p1.library)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before + 1)
        self.assertEqual(len(env.p1.library), lib_before - 1)
        self.assertEqual(env.p2.life, 20)

    async def test_mindful_manipulation_puts_one_card_back_on_library(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Mindful_Manipulation/model.py", "Mindful_Manipulation")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = [Forest(env.p1), Plains(env.p1), Forest(env.p1)]
        lib_before = len(env.p1.library)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.library), lib_before - 1)

    async def test_mindful_manipulation_does_not_draw_from_opponent_library(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Mindful_Manipulation/model.py", "Mindful_Manipulation")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = [Forest(env.p1), Plains(env.p1)]
        opp_lib_before = len(env.p2.library)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.library), opp_lib_before)
