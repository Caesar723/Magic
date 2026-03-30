from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestElite_Squire(CardTestCaseBase):
    async def test_elite_squire_enters_with_vigilance(self):
        card_cls = load_card_class_from_path("pycards/creature/Elite_Squire/model.py", "Elite_Squire")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        squire = env.get_battlefield_creature(env.p1, "Elite Squire")
        self.assert_state(squire, {
            "zone": "battlefield",
            "state": (2, 2),
            "flags": {"Vigilance": True},
        })

    async def test_elite_squire_vigilance_keeps_it_untapped_after_attack(self):
        card_cls = load_card_class_from_path("pycards/creature/Elite_Squire/model.py", "Elite_Squire")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        squire = env.get_battlefield_creature(env.p1, "Elite Squire")
        await env.simulate_combat(squire)
        self.assertFalse(squire.get_flag("tap"))
        self.assertEqual(env.p2.life, 18)

    async def test_elite_squire_blocked_does_not_reduce_opponent_life(self):
        card_cls = load_card_class_from_path("pycards/creature/Elite_Squire/model.py", "Elite_Squire")
        env = self.make_env()
        card = card_cls(env.p1)
        defender = env.put_creatures(env.p2, "Wall", 1, 4, 1)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        squire = env.get_battlefield_creature(env.p1, "Elite Squire")
        life_before = env.p2.life
        await env.simulate_combat(squire, defender)
        self.assertEqual(env.p2.life, life_before)
        self.assertFalse(squire.get_flag("tap"))

    async def test_elite_squire_blocks_opponent_attacker_preserves_controller_life(self):
        card_cls = load_card_class_from_path("pycards/creature/Elite_Squire/model.py", "Elite_Squire")
        env = self.make_env()
        raider = env.put_creatures(env.p2, "Raider", 1, 1, 1)[0]
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        squire = env.get_battlefield_creature(env.p1, "Elite Squire")
        life_before = env.p1.life
        await env.simulate_combat(raider, squire)
        await env.room.check_death()

        self.assertEqual(env.p1.life, life_before)
        self.assertEqual(env.card_zone(raider), "graveyard")
        self.assert_state(squire, {"zone": "battlefield", "state": (2, 1)})
