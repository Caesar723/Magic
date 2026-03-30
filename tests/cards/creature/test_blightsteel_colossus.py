from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestBlightsteel_Colossus(CardTestCaseBase):
    async def test_blightsteel_colossus_keywords_and_buffs(self):
        card_cls = load_card_class_from_path("pycards/creature/Blightsteel_Colossus/model.py", "Blightsteel_Colossus")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        colossus = env.get_battlefield_creature(env.p1, "Blightsteel Colossus")
        self.assert_state(colossus, {
            "zone": "battlefield",
            "state": (11, 11),
            "flags": {"Trample": True},
            "buffs_contains": ["Infect", "Indestructible"],
        })

    async def test_blightsteel_infect_kills_small_blocker_via_state_buff(self):
        card_cls = load_card_class_from_path("pycards/creature/Blightsteel_Colossus/model.py", "Blightsteel_Colossus")
        env = self.make_env()
        colossus = card_cls(env.p1)
        blocker = env.put_creatures(env.p2, "Chump", 2, 2, 1)[0]

        result = await env.play_card(colossus, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        colossus_bf = env.get_battlefield_creature(env.p1, "Blightsteel Colossus")
        env.ready_attacker(colossus_bf)
        await env.simulate_combat(colossus_bf, blocker)
        await env.room.check_death()

        self.assertEqual(env.card_zone(blocker), "graveyard")
        self.assert_state(colossus_bf, {"zone": "battlefield"})

    async def test_blightsteel_unblocked_combat_drops_opponent_life_by_power(self):
        card_cls = load_card_class_from_path("pycards/creature/Blightsteel_Colossus/model.py", "Blightsteel_Colossus")
        env = self.make_env()
        colossus = card_cls(env.p1)
        p2_before = env.p2.life

        result = await env.play_card(colossus, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        colossus_bf = env.get_battlefield_creature(env.p1, "Blightsteel Colossus")
        env.ready_attacker(colossus_bf)
        await env.simulate_combat(colossus_bf)
        await env.room.check_death()

        self.assertEqual(env.p2.life, p2_before - 11)
        self.assert_state(colossus_bf, {"zone": "battlefield"})
