from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestTorrent_Elemental(CardTestCaseBase):
    async def test_torrent_elemental_has_flash_and_flying(self):
        card_cls = load_card_class_from_path("pycards/creature/Torrent_Elemental/model.py", "Torrent_Elemental")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        elemental = env.get_battlefield_creature(env.p1, "Torrent Elemental")
        self.assert_state(elemental, {
            "zone": "battlefield",
            "state": (2, 3),
            "flags": {"Flash": True, "flying": True},
        })

    async def test_torrent_elemental_unblocked_attack_deals_two(self):
        card_cls = load_card_class_from_path("pycards/creature/Torrent_Elemental/model.py", "Torrent_Elemental")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        elemental = env.get_battlefield_creature(env.p1, "Torrent Elemental")
        await env.simulate_combat(elemental)
        self.assertEqual(env.p2.life, 18)

    async def test_torrent_elemental_blocked_by_large_reach_no_player_damage(self):
        card_cls = load_card_class_from_path("pycards/creature/Torrent_Elemental/model.py", "Torrent_Elemental")
        env = self.make_env()
        card = card_cls(env.p1)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        elemental = env.get_battlefield_creature(env.p1, "Torrent Elemental")
        blocker = env.put_creatures(env.p2, "Wall", 5, 5, 1, reach=True)[0]
        life_before = env.p2.life
        await env.simulate_combat(elemental, blocker)
        self.assertEqual(env.p2.life, life_before)
