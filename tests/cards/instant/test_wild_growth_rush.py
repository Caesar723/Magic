from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest
from pycards.land.Plains.model import Plains


class TestWild_Growth_Rush(CardTestCaseBase):
    async def test_wild_growth_rush_buffs_and_fetches_land_if_forest(self):
        card_cls = load_card_class_from_path("pycards/Instant/Wild_Growth_Rush/model.py", "Wild_Growth_Rush")
        env = self.make_env()
        card = card_cls(env.p1)

        creature = env.put_creatures(env.p1, "Rush Target", 2, 2, 1)[0]
        env.p1.land_area.append(Forest(env.p1))
        env.p1.library = [Forest(env.p1)]
        lands_before = len(env.p1.land_area)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertGreaterEqual(creature.state[0], 4)
        self.assertGreaterEqual(len(env.p1.land_area), lands_before + 1)

    async def test_wild_growth_rush_no_forest_skips_library_search(self):
        card_cls = load_card_class_from_path("pycards/Instant/Wild_Growth_Rush/model.py", "Wild_Growth_Rush")
        env = self.make_env()
        card = card_cls(env.p1)
        creature = env.put_creatures(env.p1, "Rush Target", 2, 2, 1)[0]
        env.p1.land_area.clear()
        env.p1.land_area.append(Plains(env.p1))
        env.p1.library = [Forest(env.p1)]
        lib_before = len(env.p1.library)
        lands_before = len(env.p1.land_area)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertGreaterEqual(creature.state[0], 4)
        self.assertTrue(creature.get_flag("Trample"))
        self.assertEqual(len(env.p1.land_area), lands_before)
        self.assertEqual(len(env.p1.library), lib_before)

    async def test_wild_growth_rush_opponent_life_unchanged(self):
        card_cls = load_card_class_from_path("pycards/Instant/Wild_Growth_Rush/model.py", "Wild_Growth_Rush")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p1, "Rush Target", 2, 2, 1)
        env.p1.land_area.append(Forest(env.p1))
        env.p1.library = [Forest(env.p1)]
        opp = env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp)
