from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest


class TestSylvan_Harmonist(CardTestCaseBase):
    async def test_sylvan_harmonist_etb_puts_land_to_battlefield_tapped(self):
        card_cls = load_card_class_from_path("pycards/creature/Sylvan_Harmonist/model.py", "Sylvan_Harmonist")
        env = self.make_env()
        card = card_cls(env.p1)

        land = Forest(env.p1)
        env.p1.library = [land]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        harmonist = env.get_battlefield_creature(env.p1, "Sylvan Harmonist")
        self.assert_state(harmonist, {"zone": "battlefield", "state": (2, 3)})
        self.assertEqual(len(env.p1.library), 0)
        self.assertEqual(len(env.p1.land_area), 1)
        self.assertTrue(env.p1.land_area[0].get_flag("tap"))

    async def test_sylvan_harmonist_empty_library_skips_land_search(self):
        env = self.make_env()
        card_cls = load_card_class_from_path("pycards/creature/Sylvan_Harmonist/model.py", "Sylvan_Harmonist")
        card = card_cls(env.p1)
        env.p1.library = []
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.land_area), 0)
        self.assertEqual(len(env.p1.library), 0)
        env.get_battlefield_creature(env.p1, "Sylvan Harmonist")

    async def test_sylvan_harmonist_opponent_life_unchanged_on_etb(self):
        card_cls = load_card_class_from_path("pycards/creature/Sylvan_Harmonist/model.py", "Sylvan_Harmonist")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = [Forest(env.p1)]
        opp = env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp)
