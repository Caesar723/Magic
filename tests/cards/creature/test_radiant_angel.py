from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestRadiant_Angel(CardTestCaseBase):
    async def test_radiant_angel_enters_with_flying_lifelink(self):
        card_cls = load_card_class_from_path("pycards/creature/Radiant_Angel/model.py", "Radiant_Angel")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        angel = env.get_battlefield_creature(env.p1, "Radiant Angel")
        self.assert_state(angel, {
            "zone": "battlefield",
            "state": (4, 4),
            "flags": {"flying": True, "lifelink": True},
        })

    async def test_radiant_angel_damage_taps_black_creatures_and_lifelinks(self):
        card_cls = load_card_class_from_path("pycards/creature/Radiant_Angel/model.py", "Radiant_Angel")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.life = 10

        black_creature = env.put_creatures(env.p2, "Black Unit", 2, 2, 1)[0]
        black_creature.color = "black"

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        angel = env.get_battlefield_creature(env.p1, "Radiant Angel")
        await env.simulate_combat(angel)

        self.assertEqual(env.p1.life, 14)
        self.assertTrue(black_creature.get_flag("tap"))

    async def test_radiant_angel_damage_does_not_tap_non_black_creatures(self):
        card_cls = load_card_class_from_path("pycards/creature/Radiant_Angel/model.py", "Radiant_Angel")
        env = self.make_env()
        card = card_cls(env.p1)

        black_creature = env.put_creatures(env.p2, "Black Unit", 2, 2, 1)[0]
        black_creature.color = "black"
        green_creature = env.put_creatures(env.p2, "Green Unit", 3, 3, 1)[0]
        green_creature.color = "green"

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        angel = env.get_battlefield_creature(env.p1, "Radiant Angel")
        await env.simulate_combat(angel)

        self.assertTrue(black_creature.get_flag("tap"))
        self.assertFalse(green_creature.get_flag("tap"))
