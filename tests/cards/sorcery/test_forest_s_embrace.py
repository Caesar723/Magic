from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest
from pycards.land.Island.model import Island
from pycards.land.Mountain.model import Mountain


class TestForest_s_Embrace(CardTestCaseBase):
    async def test_forest_s_embrace_puts_up_to_three_lands_tapped(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Forest_s_Embrace/model.py", "Forest_s_Embrace")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.library = [Forest(env.p1), Island(env.p1), Mountain(env.p1)]
        land_before = len(env.p1.land_area)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertGreaterEqual(len(env.p1.land_area), land_before + 3)
        self.assertTrue(all(l.get_flag("tap") for l in env.p1.land_area[-3:]))

    async def test_forest_s_embrace_puts_only_available_lands(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Forest_s_Embrace/model.py", "Forest_s_Embrace")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.library = [Forest(env.p1)]
        land_before = len(env.p1.land_area)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.land_area), land_before + 1)
        self.assertEqual(len(env.p1.library), 0)

    async def test_forest_s_embrace_does_not_move_opponent_lands(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Forest_s_Embrace/model.py", "Forest_s_Embrace")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = [Forest(env.p1)]
        opp_land = Island(env.p2)
        env.p2.land_area.append(opp_land)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertIn(opp_land, env.p2.land_area)
