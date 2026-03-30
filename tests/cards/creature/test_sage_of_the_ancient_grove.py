from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.creature.Night_Stalker__.model import Night_Stalker__
from pycards.land.Forest.model import Forest
from pycards.land.Plains.model import Plains


class TestSage_of_the_Ancient_Grove(CardTestCaseBase):
    async def test_sage_of_the_ancient_grove_reach_and_land_tutor(self):
        card_cls = load_card_class_from_path("pycards/creature/Sage_of_the_Ancient_Grove/model.py", "Sage_of_the_Ancient_Grove")
        env = self.make_env()
        card = card_cls(env.p1)

        land = Forest(env.p1)
        env.p1.library = [land]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        sage = env.get_battlefield_creature(env.p1, "Sage of the Ancient Grove")
        self.assert_state(sage, {"zone": "battlefield", "state": (4, 4), "flags": {"reach": True}})
        self.assertEqual(len(env.p1.library), 0)
        self.assertEqual(len(env.p1.land_area), 1)
        self.assertTrue(env.p1.land_area[0].get_flag("tap"))

    async def test_sage_of_the_ancient_grove_no_land_in_library_skips_search(self):
        card_cls = load_card_class_from_path("pycards/creature/Sage_of_the_Ancient_Grove/model.py", "Sage_of_the_Ancient_Grove")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.library = [Night_Stalker__(env.p1)]
        lands_before = len(env.p1.land_area)
        lib_before = len(env.p1.library)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        sage = env.get_battlefield_creature(env.p1, "Sage of the Ancient Grove")
        self.assert_state(sage, {"zone": "battlefield", "flags": {"reach": True}})
        self.assertEqual(len(env.p1.land_area), lands_before)
        self.assertEqual(len(env.p1.library), lib_before)

    async def test_sage_of_the_ancient_grove_tutors_first_basic_in_library_order(self):
        card_cls = load_card_class_from_path("pycards/creature/Sage_of_the_Ancient_Grove/model.py", "Sage_of_the_Ancient_Grove")
        env = self.make_env()
        card = card_cls(env.p1)
        first = Forest(env.p1)
        second = Plains(env.p1)
        env.p1.library = [first, second]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertIn(first, env.p1.land_area)
        self.assertIn(second, env.p1.library)
        self.assertTrue(first.get_flag("tap"))
