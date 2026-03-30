from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest


class TestVerdant_Wyrm(CardTestCaseBase):
    async def test_verdant_wyrm_has_trample_and_fetches_land(self):
        card_cls = load_card_class_from_path("pycards/creature/Verdant_Wyrm/model.py", "Verdant_Wyrm")
        env = self.make_env()
        card = card_cls(env.p1)

        land = Forest(env.p1)
        env.p1.library = [land]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        wyrm = env.get_battlefield_creature(env.p1, "Verdant Wyrm")
        self.assert_state(wyrm, {"zone": "battlefield", "state": (4, 4), "flags": {"Trample": True}})
        self.assertEqual(len(env.p1.library), 0)
        self.assertEqual(len(env.p1.land_area), 1)
        self.assertTrue(env.p1.land_area[0].get_flag("tap"))

    async def test_verdant_wyrm_empty_library_no_land(self):
        card_cls = load_card_class_from_path("pycards/creature/Verdant_Wyrm/model.py", "Verdant_Wyrm")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = []
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.land_area), 0)
        env.get_battlefield_creature(env.p1, "Verdant Wyrm")

    async def test_verdant_wyrm_opponent_life_unchanged_when_fetching_land(self):
        card_cls = load_card_class_from_path("pycards/creature/Verdant_Wyrm/model.py", "Verdant_Wyrm")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = [Forest(env.p1)]
        opp = env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp)
