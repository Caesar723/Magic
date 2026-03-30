from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestVorinclex__Apex_of_Mutation(CardTestCaseBase):
    async def test_vorinclex_has_trample_and_infect_buff(self):
        card_cls = load_card_class_from_path("pycards/creature/Vorinclex__Apex_of_Mutation/model.py", "Vorinclex__Apex_of_Mutation")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        vorinclex = env.get_battlefield_creature(env.p1, "Vorinclex, Apex of Mutation")
        self.assert_state(vorinclex, {
            "zone": "battlefield",
            "state": (6, 6),
            "flags": {"Trample": True},
            "buffs_contains": ["Infect"],
        })

    async def test_vorinclex_infect_combat_kills_blocker(self):
        card_cls = load_card_class_from_path("pycards/creature/Vorinclex__Apex_of_Mutation/model.py", "Vorinclex__Apex_of_Mutation")
        env = self.make_env()
        card = card_cls(env.p1)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        vorinclex = env.get_battlefield_creature(env.p1, "Vorinclex, Apex of Mutation")
        blocker = env.put_creatures(env.p2, "Chump", 2, 2, 1)[0]
        await env.simulate_combat(vorinclex, blocker)
        self.assertNotEqual(env.card_zone(blocker), "battlefield")

    async def test_vorinclex_etb_does_not_damage_controller(self):
        card_cls = load_card_class_from_path("pycards/creature/Vorinclex__Apex_of_Mutation/model.py", "Vorinclex__Apex_of_Mutation")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.life = 4

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, 4)
