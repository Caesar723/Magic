from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestThornwood_Ranger(CardTestCaseBase):
    async def test_thornwood_ranger_has_reach(self):
        card_cls = load_card_class_from_path("pycards/creature/Thornwood_Ranger/model.py", "Thornwood_Ranger")
        env = self.make_env()
        card = card_cls(env.p1)

        ally = env.put_creatures(env.p1, "Ally", 2, 2, 1)[0]
        env.script_selection(env.p1, [0])

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        ranger = env.get_battlefield_creature(env.p1, "Thornwood Ranger")
        self.assert_state(ranger, {"flags": {"reach": True}, "state": (2, 1)})
        self.assertEqual(ally.state[0], 3)
        self.assertEqual(ally.state[1], 2)
        self.assertEqual(env.p2.life, 20)

    async def test_thornwood_ranger_reach_can_block_flying(self):
        card_cls = load_card_class_from_path("pycards/creature/Thornwood_Ranger/model.py", "Thornwood_Ranger")
        env = self.make_env()
        card = card_cls(env.p1)

        ally = env.put_creatures(env.p1, "Ally", 2, 2, 1)[0]
        env.script_selection(env.p1, [0])

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(ally.state[0], 3)

        ranger = env.get_battlefield_creature(env.p1, "Thornwood Ranger")
        flyer = env.put_creatures(env.p2, "Enemy Flyer", 2, 2, 1, flying=True)[0]
        life_before = env.p1.life
        await env.simulate_combat(flyer, ranger)
        self.assertEqual(env.p1.life, life_before)

    async def test_thornwood_ranger_etb_buff_expires_after_end_turn_hook(self):
        card_cls = load_card_class_from_path("pycards/creature/Thornwood_Ranger/model.py", "Thornwood_Ranger")
        env = self.make_env()
        card = card_cls(env.p1)
        ally = env.put_creatures(env.p1, "Ally", 2, 2, 1)[0]
        env.script_selection(env.p1, [0])
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(ally.state, (3, 2))
        for b in list(ally.buffs):
            b.when_end_turn()
        self.assertEqual(ally.state, (2, 2))
