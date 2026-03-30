from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.creature.Night_Stalker__.model import Night_Stalker__
from pycards.land.Forest.model import Forest


class TestWild_Growth(CardTestCaseBase):
    async def test_wild_growth_fetches_tapped_land(self):
        card_cls = load_card_class_from_path("pycards/Instant/Wild_Growth/model.py", "Wild_Growth")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.library = [Forest(env.p1)]
        lands_before = len(env.p1.land_area)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.land_area), lands_before + 1)
        self.assertTrue(env.p1.land_area[-1].get_flag("tap"))

    async def test_wild_growth_no_land_in_library_does_nothing(self):
        card_cls = load_card_class_from_path("pycards/Instant/Wild_Growth/model.py", "Wild_Growth")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.library = [Night_Stalker__(env.p1)]
        lands_before = len(env.p1.land_area)
        lib_before = len(env.p1.library)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.land_area), lands_before)
        self.assertEqual(len(env.p1.library), lib_before)

    async def test_wild_growth_opponent_life_unchanged_when_fetching(self):
        card_cls = load_card_class_from_path("pycards/Instant/Wild_Growth/model.py", "Wild_Growth")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = [Forest(env.p1)]
        opp_before = env.p2.life

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp_before)
