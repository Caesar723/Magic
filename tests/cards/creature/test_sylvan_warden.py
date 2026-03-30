from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest


class TestSylvan_Warden(CardTestCaseBase):
    async def test_sylvan_warden_etb_fetches_land_to_land_area(self):
        card_cls = load_card_class_from_path("pycards/creature/Sylvan_Warden/model.py", "Sylvan_Warden")
        env = self.make_env()
        card = card_cls(env.p1)

        land = Forest(env.p1)
        env.p1.library = [land]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        warden = env.get_battlefield_creature(env.p1, "Sylvan Warden")
        self.assert_state(warden, {"zone": "battlefield", "state": (2, 4)})
        self.assertEqual(len(env.p1.library), 0)
        self.assertEqual(len(env.p1.land_area), 1)

    async def test_sylvan_warden_attack_puts_plus_one_plus_one_counter_like_buff(self):
        card_cls = load_card_class_from_path("pycards/creature/Sylvan_Warden/model.py", "Sylvan_Warden")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        warden = env.get_battlefield_creature(env.p1, "Sylvan Warden")
        before = warden.state
        await env.simulate_combat(warden)
        self.assertGreaterEqual(warden.state[0], before[0] + 1)
        self.assertGreaterEqual(warden.state[1], before[1] + 1)

    async def test_sylvan_warden_empty_library_no_land_fetched(self):
        card_cls = load_card_class_from_path("pycards/creature/Sylvan_Warden/model.py", "Sylvan_Warden")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = []
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.land_area), 0)
        env.get_battlefield_creature(env.p1, "Sylvan Warden")
