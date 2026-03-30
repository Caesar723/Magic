from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestNatural_Harmony(CardTestCaseBase):
    async def test_natural_harmony_fetches_land_and_gain_two_life(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Natural_Harmony/model.py", "Natural_Harmony")
        forest_cls = load_card_class_from_path("pycards/land/Forest/model.py", "Forest")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.library = [forest_cls(env.p1)]
        env.p1.life = 10

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.land_area), 1)
        self.assertTrue(env.p1.land_area[0].get_flag("tap"))
        self.assertEqual(env.p1.life, 12)

    async def test_natural_harmony_still_gains_life_without_land_in_library(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Natural_Harmony/model.py", "Natural_Harmony")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.library = []
        env.p1.life = 10
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.land_area), 0)
        self.assertEqual(env.p1.life, 12)

    async def test_natural_harmony_opponent_life_unchanged(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Natural_Harmony/model.py", "Natural_Harmony")
        forest_cls = load_card_class_from_path("pycards/land/Forest/model.py", "Forest")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = [forest_cls(env.p1)]
        opp_before = env.p2.life

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp_before)
