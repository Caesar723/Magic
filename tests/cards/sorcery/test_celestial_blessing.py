from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestCelestial_Blessing(CardTestCaseBase):
    async def test_celestial_blessing_gives_lifelink_to_two_creatures(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Celestial_Blessing/model.py", "Celestial_Blessing")
        env = self.make_env()
        card = card_cls(env.p1)

        c1 = env.put_creatures(env.p1, "Bless One", 2, 2, 1)[0]
        c2 = env.put_creatures(env.p1, "Bless Two", 3, 3, 1)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertTrue(c1.get_flag("lifelink"))
        self.assertTrue(c2.get_flag("lifelink"))
        self.assertEqual(env.p2.life, 20)

    async def test_celestial_blessing_single_creature_only_one_gets_lifelink(self):
        """Selection fills up to two targets; with one creature on board only it is buffed."""
        card_cls = load_card_class_from_path("pycards/sorcery/Celestial_Blessing/model.py", "Celestial_Blessing")
        env = self.make_env()
        card = card_cls(env.p1)

        solo = env.put_creatures(env.p1, "Only Friend", 4, 4, 1)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertTrue(solo.get_flag("lifelink"))
        self.assertEqual(len(env.p1.battlefield), 1)

    async def test_celestial_blessing_does_not_grant_lifelink_to_opponent_creatures(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Celestial_Blessing/model.py", "Celestial_Blessing")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_creatures(env.p1, "Bless One", 2, 2, 1)
        foe = env.put_creatures(env.p2, "Enemy", 3, 3, 1)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertFalse(foe.get_flag("lifelink"))
