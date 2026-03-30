from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from unittest.mock import AsyncMock


class TestMerfolk_Wayfinder(CardTestCaseBase):
    async def test_merfolk_wayfinder_etb_scry_does_not_change_library_count(self):
        card_cls = load_card_class_from_path("pycards/creature/Merfolk_Wayfinder/model.py", "Merfolk_Wayfinder")
        env = self.make_env()
        card = card_cls(env.p1)

        before = len(env.p1.library)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        wayfinder = env.get_battlefield_creature(env.p1, "Merfolk Wayfinder")
        self.assert_state(wayfinder, {"zone": "battlefield", "state": (1, 1)})
        self.assertEqual(len(env.p1.library), before)

    async def test_merfolk_wayfinder_calls_scry_with_current_value(self):
        card_cls = load_card_class_from_path("pycards/creature/Merfolk_Wayfinder/model.py", "Merfolk_Wayfinder")
        env = self.make_env()
        card = card_cls(env.p1)
        card.Scry = AsyncMock(return_value=None)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        card.Scry.assert_awaited_once_with(env.p1, env.p2, 5)

    async def test_merfolk_wayfinder_etb_does_not_touch_opponent_library(self):
        card_cls = load_card_class_from_path("pycards/creature/Merfolk_Wayfinder/model.py", "Merfolk_Wayfinder")
        env = self.make_env()
        card = card_cls(env.p1)
        opp_lib_before = len(env.p2.library)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.library), opp_lib_before)
