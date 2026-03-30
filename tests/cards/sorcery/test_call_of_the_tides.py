from unittest.mock import AsyncMock

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestCall_of_the_Tides(CardTestCaseBase):
    async def test_call_of_the_tides_draw_two_discard_one(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Call_of_the_Tides/model.py", "Call_of_the_Tides")
        forest_cls = load_card_class_from_path("pycards/land/Forest/model.py", "Forest")
        swamp_cls = load_card_class_from_path("pycards/land/Swamp/model.py", "Swamp")
        mountain_cls = load_card_class_from_path("pycards/land/Mountain/model.py", "Mountain")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.library = [forest_cls(env.p1), swamp_cls(env.p1), mountain_cls(env.p1)]
        hand_before = len(env.p1.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before + 1)
        self.assertTrue(any(c.name == "Call of the Tides" for c in env.p1.graveyard))

    async def test_call_of_the_tides_invokes_scry_one(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Call_of_the_Tides/model.py", "Call_of_the_Tides")
        forest_cls = load_card_class_from_path("pycards/land/Forest/model.py", "Forest")
        env = self.make_env()
        card = card_cls(env.p1)
        card.Scry = AsyncMock(return_value=None)
        env.p1.library = [forest_cls(env.p1), forest_cls(env.p1), forest_cls(env.p1)]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        card.Scry.assert_awaited_once_with(env.p1, env.p2, 1)

    async def test_call_of_the_tides_opponent_life_unchanged(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Call_of_the_Tides/model.py", "Call_of_the_Tides")
        forest_cls = load_card_class_from_path("pycards/land/Forest/model.py", "Forest")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = [forest_cls(env.p1), forest_cls(env.p1), forest_cls(env.p1)]
        opp = env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp)
