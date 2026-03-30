from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from unittest.mock import AsyncMock


class TestMindshaper_Sphinx(CardTestCaseBase):
    async def test_mindshaper_sphinx_flying_and_etb_draw(self):
        card_cls = load_card_class_from_path("pycards/creature/Mindshaper_Sphinx/model.py", "Mindshaper_Sphinx")
        env = self.make_env()
        card = card_cls(env.p1)

        hand_before = len(env.p1.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        sphinx = env.get_battlefield_creature(env.p1, "Mindshaper Sphinx")
        self.assert_state(sphinx, {"zone": "battlefield", "state": (4, 4), "flags": {"flying": True}})
        self.assertEqual(len(env.p1.hand), hand_before)

    async def test_mindshaper_sphinx_calls_scry_three_on_etb(self):
        card_cls = load_card_class_from_path("pycards/creature/Mindshaper_Sphinx/model.py", "Mindshaper_Sphinx")
        env = self.make_env()
        card = card_cls(env.p1)
        card.Scry = AsyncMock(return_value=None)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        card.Scry.assert_awaited_once_with(env.p1, env.p2, 3)

    async def test_mindshaper_sphinx_etb_does_not_change_opponent_hand_size(self):
        card_cls = load_card_class_from_path("pycards/creature/Mindshaper_Sphinx/model.py", "Mindshaper_Sphinx")
        env = self.make_env()
        card = card_cls(env.p1)
        opp_hand_before = len(env.p2.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.hand), opp_hand_before)
