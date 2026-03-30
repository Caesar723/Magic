from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestTidal_Sprite(CardTestCaseBase):
    async def test_tidal_sprite_has_flying_and_connects_unblocked(self):
        card_cls = load_card_class_from_path("pycards/creature/Tidal_Sprite/model.py", "Tidal_Sprite")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        sprite = env.get_battlefield_creature(env.p1, "Tidal Sprite")
        self.assert_state(sprite, {
            "zone": "battlefield",
            "state": (1, 1),
            "flags": {"flying": True},
        })

        await env.simulate_combat(sprite)
        self.assertEqual(env.p2.life, 19)

    async def test_tidal_sprite_blocked_by_flying_creature_deals_no_player_damage(self):
        card_cls = load_card_class_from_path("pycards/creature/Tidal_Sprite/model.py", "Tidal_Sprite")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        sprite = env.get_battlefield_creature(env.p1, "Tidal Sprite")
        blocker = env.put_creatures(env.p2, "Sky Snare", 1, 2, 1, flying=True)[0]
        life_before = env.p2.life
        await env.simulate_combat(sprite, blocker)
        self.assertEqual(env.p2.life, life_before)

    async def test_tidal_sprite_blocked_by_reach_creature_does_not_damage_player(self):
        card_cls = load_card_class_from_path("pycards/creature/Tidal_Sprite/model.py", "Tidal_Sprite")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        sprite = env.get_battlefield_creature(env.p1, "Tidal Sprite")
        reach_wall = env.put_creatures(env.p2, "Reach Wall", 2, 3, 1, reach=True)[0]
        life_before = env.p2.life
        await env.simulate_combat(sprite, reach_wall)
        self.assertEqual(env.p2.life, life_before)
        self.assert_state(reach_wall, {"zone": "battlefield"})
