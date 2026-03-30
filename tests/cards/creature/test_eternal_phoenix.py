from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestEternal_Phoenix(CardTestCaseBase):
    async def test_eternal_phoenix_revives_once_with_feather_counter(self):
        card_cls = load_card_class_from_path("pycards/creature/Eternal_Phoenix/model.py", "Eternal_Phoenix")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        phoenix = env.get_battlefield_creature(env.p1, "Eternal Phoenix")
        await env.move_to_graveyard(phoenix)
        await env.resolve_stack()

        revived = env.get_battlefield_creature(env.p1, "Eternal Phoenix")
        self.assertIsNotNone(revived)
        self.assertTrue(revived.get_flag("feather_Eternal_Phoenix"))
        self.assert_state(revived, {"zone": "battlefield", "state": (3, 3), "flags": {"flying": True}})

    async def test_eternal_phoenix_with_feather_does_not_revive_again(self):
        card_cls = load_card_class_from_path("pycards/creature/Eternal_Phoenix/model.py", "Eternal_Phoenix")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        phoenix = env.get_battlefield_creature(env.p1, "Eternal Phoenix")
        await env.move_to_graveyard(phoenix)
        await env.resolve_stack()
        revived = env.get_battlefield_creature(env.p1, "Eternal Phoenix")
        self.assertTrue(revived.get_flag("feather_Eternal_Phoenix"))

        await env.move_to_graveyard(revived)
        await env.resolve_stack()

        names_in_gy = [c.name for c in env.p1.graveyard]
        self.assertGreaterEqual(names_in_gy.count("Eternal Phoenix"), 1)
        with self.assertRaises(ValueError):
            env.get_battlefield_creature(env.p1, "Eternal Phoenix")

    async def test_eternal_phoenix_revive_does_not_change_opponent_life(self):
        card_cls = load_card_class_from_path("pycards/creature/Eternal_Phoenix/model.py", "Eternal_Phoenix")
        env = self.make_env()
        card = card_cls(env.p1)
        opp_life = env.p2.life

        await env.play_card(card, env.p1)
        await env.resolve_stack()
        phoenix = env.get_battlefield_creature(env.p1, "Eternal Phoenix")
        await env.move_to_graveyard(phoenix)
        await env.resolve_stack()

        self.assertIsNotNone(env.get_battlefield_creature(env.p1, "Eternal Phoenix"))
        self.assertEqual(env.p2.life, opp_life)
