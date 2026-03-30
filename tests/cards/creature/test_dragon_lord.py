from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestDragon_Lord(CardTestCaseBase):
    async def test_dragon_lord_has_flying_and_creates_two_tokens_on_player_damage(self):
        card_cls = load_card_class_from_path("pycards/creature/Dragon_Lord/model.py", "Dragon_Lord")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        dragon = env.get_battlefield_creature(env.p1, "Dragon Lord")
        self.assert_state(dragon, {"zone": "battlefield", "state": (6, 6), "flags": {"flying": True}})

        before_count = len(env.p1.battlefield)
        await env.trigger(dragon, "when_harm_is_done", env.p2, 2, env.p1, env.p2)
        self.assertEqual(len(env.p1.battlefield), before_count + 2)

        tokens = env.p1.battlefield[-2:]
        for token in tokens:
            self.assertEqual(token.state, (4, 4))
            self.assertEqual(token.name, "Dragon Lord")

    async def test_dragon_lord_damage_to_enemy_creature_still_summons_tokens(self):
        card_cls = load_card_class_from_path("pycards/creature/Dragon_Lord/model.py", "Dragon_Lord")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        dragon = env.get_battlefield_creature(env.p1, "Dragon Lord")
        blocker = env.put_creatures(env.p2, "Blocker", 1, 10, 1)[0]
        before = len(env.p1.battlefield)
        await env.trigger(dragon, "when_harm_is_done", blocker, 3, env.p1, env.p2)
        self.assertEqual(len(env.p1.battlefield), before + 2)

    async def test_dragon_lord_damage_to_controller_creature_does_not_create_tokens(self):
        card_cls = load_card_class_from_path("pycards/creature/Dragon_Lord/model.py", "Dragon_Lord")
        env = self.make_env()
        card = card_cls(env.p1)
        ally = env.put_creatures(env.p1, "Friendly Pawn", 1, 1, 1)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        dragon = env.get_battlefield_creature(env.p1, "Dragon Lord")
        before = len(env.p1.battlefield)
        await env.trigger(dragon, "when_harm_is_done", ally, 2, env.p1, env.p2)
        self.assertEqual(len(env.p1.battlefield), before)
