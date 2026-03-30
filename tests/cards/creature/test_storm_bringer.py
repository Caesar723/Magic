from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestStorm_Bringer(CardTestCaseBase):
    async def test_storm_bringer_etb_damages_opponent_and_heals_owner(self):
        card_cls = load_card_class_from_path("pycards/creature/Storm_Bringer/model.py", "Storm_Bringer")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.life = 10

        weak = env.put_creatures(env.p2, "Weak Target", 2, 2, 1)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        bringer = env.get_battlefield_creature(env.p1, "Storm Bringer")
        self.assert_state(bringer, {"zone": "battlefield", "state": (5, 5), "flags": {"flying": True}})
        self.assertEqual(env.p1.life, 13)
        self.assertEqual(env.p2.life, 17)
        self.assertIn(env.card_zone(weak), {"graveyard", "exile_area"})

    async def test_storm_bringer_etb_hits_player_when_opponent_has_no_creatures(self):
        card_cls = load_card_class_from_path("pycards/creature/Storm_Bringer/model.py", "Storm_Bringer")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.life = 8
        p2_before = env.p2.life

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, p2_before - 3)
        self.assertEqual(env.p1.life, 11)

    async def test_storm_bringer_etb_splashes_three_to_each_enemy_creature(self):
        card_cls = load_card_class_from_path("pycards/creature/Storm_Bringer/model.py", "Storm_Bringer")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "Weak Target", 2, 2, 1)
        tough = env.put_creatures(env.p2, "Tough", 4, 10, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(tough.state, (4, 7))
        self.assertEqual(env.card_zone(tough), "battlefield")
