from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestMistweaver_Drake(CardTestCaseBase):
    async def test_mistweaver_drake_has_flash(self):
        card_cls = load_card_class_from_path("pycards/creature/Mistweaver_Drake/model.py", "Mistweaver_Drake")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        drake = env.get_battlefield_creature(env.p1, "Mistweaver Drake")
        self.assert_state(drake, {"zone": "battlefield", "state": (2, 1), "flags": {"Flash": True}})

    async def test_mistweaver_drake_unblocked_attack_deals_two(self):
        card_cls = load_card_class_from_path("pycards/creature/Mistweaver_Drake/model.py", "Mistweaver_Drake")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        drake = env.get_battlefield_creature(env.p1, "Mistweaver Drake")
        await env.simulate_combat(drake)
        self.assertEqual(env.p2.life, 18)

    async def test_mistweaver_drake_blocked_deals_no_player_damage(self):
        card_cls = load_card_class_from_path("pycards/creature/Mistweaver_Drake/model.py", "Mistweaver_Drake")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        drake = env.get_battlefield_creature(env.p1, "Mistweaver Drake")
        blocker = env.put_creatures(env.p2, "Reach Wall", 1, 3, 1, reach=True)
        blocker = blocker[0]
        life_before = env.p2.life
        await env.simulate_combat(drake, blocker)
        self.assertEqual(env.p2.life, life_before)

    async def test_mistweaver_drake_trades_with_two_two_blocker(self):
        card_cls = load_card_class_from_path("pycards/creature/Mistweaver_Drake/model.py", "Mistweaver_Drake")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        drake = env.get_battlefield_creature(env.p1, "Mistweaver Drake")
        blocker = env.put_creatures(env.p2, "Two Two", 2, 2, 1)[0]
        await env.simulate_combat(drake, blocker)
        await env.room.check_death()

        self.assertEqual(env.card_zone(drake), "graveyard")
        self.assertEqual(env.card_zone(blocker), "graveyard")
