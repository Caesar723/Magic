from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestFalling_Stars(CardTestCaseBase):
    async def test_falling_stars_damages_all_and_creates_star_beast(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Falling_Stars/model.py", "Falling_Stars")
        env = self.make_env()
        card = card_cls(env.p1)

        weak_enemy = env.put_creatures(env.p2, "Enemy C", 2, 2, 1)[0]
        strong_enemy = env.put_creatures(env.p2, "Enemy Boss", 8, 10, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertNotEqual(env.card_zone(weak_enemy), "battlefield")
        self.assertLess(strong_enemy.state[1], 10)
        star_beasts = [c for c in env.p1.battlefield if c.name == "Star Beast"]
        self.assertEqual(len(star_beasts), 1)
        self.assert_state(star_beasts[0], {"state": (7, 7)})

    async def test_falling_stars_no_enemy_creatures_still_summons_star_beast(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Falling_Stars/model.py", "Falling_Stars")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p1, "Ally", 1, 1, 1)
        self.assertFalse(env.p2.battlefield)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        star_beasts = [c for c in env.p1.battlefield if c.name == "Star Beast"]
        self.assertEqual(len(star_beasts), 1)

    async def test_falling_stars_player_life_totals_unchanged(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Falling_Stars/model.py", "Falling_Stars")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "Enemy", 2, 2, 1)
        env.put_creatures(env.p1, "Ally", 1, 1, 1)
        p1_life = env.p1.life
        p2_life = env.p2.life

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, p1_life)
        self.assertEqual(env.p2.life, p2_life)
