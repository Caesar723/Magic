from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestAncient_Stonewood(CardTestCaseBase):
    async def test_ancient_stonewood_indestructible_and_reflect_damage(self):
        stonewood_cls = load_card_class_from_path("pycards/creature/Ancient_Stonewood/model.py", "Ancient_Stonewood")
        env = self.make_env()
        card = stonewood_cls(env.p1)

        attacker = env.put_creatures(env.p2, "Enemy Attacker", 3, 3, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        stonewood = env.get_battlefield_creature(env.p1, "Ancient Stonewood")
        await env.simulate_combat(attacker, stonewood)
        await env.room.check_death()

        self.assert_state(stonewood, {"zone": "battlefield"})
        self.assertIn(env.card_zone(attacker), {"graveyard", "exile_area", "battlefield"})

    async def test_ancient_stonewood_hurt_reflect_skipped_without_opponent_creatures(self):
        stonewood_cls = load_card_class_from_path("pycards/creature/Ancient_Stonewood/model.py", "Ancient_Stonewood")
        env = self.make_env()
        card = stonewood_cls(env.p1)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        stonewood = env.get_battlefield_creature(env.p1, "Ancient Stonewood")

        source = env.create_creature(env.p1, "Damage Source", 1, 1)
        env.p2.battlefield.clear()
        before_life = env.p2.life
        await env.trigger(stonewood, "when_hurt", source, 2, env.p1, env.p2)
        self.assertEqual(env.p2.life, before_life)
        self.assertEqual(len(env.p2.battlefield), 0)

    async def test_ancient_stonewood_reflect_damage_kills_one_toughness_creature(self):
        stonewood_cls = load_card_class_from_path("pycards/creature/Ancient_Stonewood/model.py", "Ancient_Stonewood")
        env = self.make_env()
        card = stonewood_cls(env.p1)
        chump = env.put_creatures(env.p2, "Chump", 1, 1, 1)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        stonewood = env.get_battlefield_creature(env.p1, "Ancient Stonewood")

        source = env.create_creature(env.p1, "Ping Source", 1, 1)
        await env.trigger(stonewood, "when_hurt", source, 1, env.p1, env.p2)
        await env.room.check_death()

        self.assertEqual(env.card_zone(chump), "graveyard")
        self.assert_state(stonewood, {"zone": "battlefield"})
