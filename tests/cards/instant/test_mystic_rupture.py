from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest


class TestMystic_Rupture(CardTestCaseBase):
    async def test_mystic_rupture_returns_nonland_permanents_to_hand(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Rupture/model.py", "Mystic_Rupture")
        env = self.make_env()
        card = card_cls(env.p1)

        self_c = env.put_creatures(env.p1, "Self C", 2, 2, 1)[0]
        opp_c = env.put_creatures(env.p2, "Opp C", 2, 2, 1)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertNotEqual(env.card_zone(self_c), "battlefield")
        self.assertNotEqual(env.card_zone(opp_c), "battlefield")

    async def test_mystic_rupture_leaves_lands_on_battlefield(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Rupture/model.py", "Mystic_Rupture")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_creatures(env.p1, "BF", 1, 1, 1)
        p1_land = Forest(env.p1)
        env.p1.land_area.append(p1_land)
        lands_before = len(env.p1.land_area)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.land_area), lands_before)
        self.assertTrue(any(getattr(x, "name", "") == "Forest" for x in env.p1.land_area))

    async def test_mystic_rupture_player_life_totals_unchanged(self):
        card_cls = load_card_class_from_path("pycards/Instant/Mystic_Rupture/model.py", "Mystic_Rupture")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p1, "X", 2, 2, 1)
        env.put_creatures(env.p2, "Y", 2, 2, 1)
        p1l, p2l = env.p1.life, env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, p1l)
        self.assertEqual(env.p2.life, p2l)
