from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestMist_Djinn(CardTestCaseBase):
    async def test_mist_djinn_base_state_and_defend_hook_callable(self):
        card_cls = load_card_class_from_path("pycards/creature/Mist_Djinn/model.py", "Mist_Djinn")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        djinn = env.get_battlefield_creature(env.p1, "Mist Djinn")
        self.assert_state(djinn, {"zone": "battlefield", "state": (4, 6)})

        attacker = env.put_creatures(env.p2, "Attacker", 2, 2, 1)[0]
        hook_result = await env.trigger(djinn, "when_finish_defend", attacker, env.p1, env.p2)
        self.assertIsNone(hook_result)

    async def test_mist_djinn_second_defend_hook_still_noop(self):
        card_cls = load_card_class_from_path("pycards/creature/Mist_Djinn/model.py", "Mist_Djinn")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        djinn = env.get_battlefield_creature(env.p1, "Mist Djinn")
        a1 = env.put_creatures(env.p2, "Attacker One", 1, 1, 1)[0]
        a2 = env.put_creatures(env.p2, "Attacker Two", 1, 1, 1)[0]
        r1 = await env.trigger(djinn, "when_finish_defend", a1, env.p1, env.p2)
        r2 = await env.trigger(djinn, "when_finish_defend", a2, env.p1, env.p2)
        self.assertIsNone(r1)
        self.assertIsNone(r2)

    async def test_mist_djinn_unblocked_combat_deals_four_damage(self):
        card_cls = load_card_class_from_path("pycards/creature/Mist_Djinn/model.py", "Mist_Djinn")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        djinn = env.get_battlefield_creature(env.p1, "Mist Djinn")
        before = env.p2.life
        await env.simulate_combat(djinn)
        self.assertEqual(env.p2.life, before - 4)
