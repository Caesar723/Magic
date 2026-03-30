from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestNature_s_Reprisal(CardTestCaseBase):
    async def test_nature_s_reprisal_destroys_flying_and_gains_life(self):
        card_cls = load_card_class_from_path("pycards/Instant/Nature_s_Reprisal/model.py", "Nature_s_Reprisal")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Flying Enemy", 2, 2, 1, flying=True)[0]
        env.p1.life = 10

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(target), "graveyard")
        self.assertEqual(env.p1.life, 12)

    async def test_nature_s_reprisal_does_not_destroy_non_flying(self):
        card_cls = load_card_class_from_path("pycards/Instant/Nature_s_Reprisal/model.py", "Nature_s_Reprisal")
        env = self.make_env()
        card = card_cls(env.p1)

        ground = env.put_creatures(env.p2, "Walker", 2, 2, 1)[0]
        env.p1.life = 10
        env.script_selection(env.p1, [0])

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(ground), "battlefield")
        self.assertEqual(env.p1.life, 10)

    async def test_nature_s_reprisal_opponent_life_unchanged_when_destroying_flyer(self):
        card_cls = load_card_class_from_path("pycards/Instant/Nature_s_Reprisal/model.py", "Nature_s_Reprisal")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "Flyer", 2, 2, 1, flying=True)
        opp_life = env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp_life)
