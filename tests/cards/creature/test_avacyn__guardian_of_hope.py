from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestAvacyn__Guardian_of_Hope(CardTestCaseBase):
    async def test_avacyn_keywords(self):
        card_cls = load_card_class_from_path("pycards/creature/Avacyn__Guardian_of_Hope/model.py", "Avacyn__Guardian_of_Hope")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        avacyn = env.get_battlefield_creature(env.p1, "Avacyn, Guardian of Hope")
        self.assert_state(avacyn, {
            "zone": "battlefield",
            "state": (5, 4),
            "flags": {"flying": True, "Vigilance": True, "lifelink": True},
        })

    async def test_avacyn_etb_grants_indestructible_to_team(self):
        card_cls = load_card_class_from_path("pycards/creature/Avacyn__Guardian_of_Hope/model.py", "Avacyn__Guardian_of_Hope")
        env = self.make_env()
        ally = env.put_creatures(env.p1, "Ally", 2, 2, 1)[0]
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        avacyn = env.get_battlefield_creature(env.p1, "Avacyn, Guardian of Hope")
        self.assert_state(avacyn, {"buffs_contains": ["Indestructible"]})
        self.assert_state(ally, {"buffs_contains": ["Indestructible"]})

    async def test_avacyn_etb_does_not_grant_indestructible_to_opponent_creatures(self):
        card_cls = load_card_class_from_path("pycards/creature/Avacyn__Guardian_of_Hope/model.py", "Avacyn__Guardian_of_Hope")
        env = self.make_env()
        foe = env.put_creatures(env.p2, "Enemy Ally", 2, 2, 1)[0]
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        buff_names = [type(b).__name__ for b in foe.buffs]
        self.assertNotIn("Indestructible", buff_names)

    async def test_avacyn_unblocked_combat_lifelink_gains_life(self):
        card_cls = load_card_class_from_path("pycards/creature/Avacyn__Guardian_of_Hope/model.py", "Avacyn__Guardian_of_Hope")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.life = 12
        p2_before = env.p2.life

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        avacyn = env.get_battlefield_creature(env.p1, "Avacyn, Guardian of Hope")
        await env.simulate_combat(avacyn)
        self.assertEqual(env.p2.life, p2_before - 5)
        self.assertEqual(env.p1.life, 12 + 5)
