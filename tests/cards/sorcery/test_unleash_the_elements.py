from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestUnleash_the_Elements(CardTestCaseBase):
    async def test_unleash_the_elements_deals_three_to_all_creatures(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Unleash_the_Elements/model.py", "Unleash_the_Elements")
        env = self.make_env()
        card = card_cls(env.p1)

        c1 = env.put_creatures(env.p1, "Self C", 2, 4, 1)[0]
        c2 = env.put_creatures(env.p2, "Enemy C", 2, 4, 1)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(c1.state[1], 1)
        self.assertEqual(c2.state[1], 1)

    async def test_unleash_the_elements_lethal_creature_exiled(self):
        """Lethal damage from the spell is followed by `exile_object` (not graveyard)."""
        card_cls = load_card_class_from_path("pycards/sorcery/Unleash_the_Elements/model.py", "Unleash_the_Elements")
        env = self.make_env()
        card = card_cls(env.p1)
        frail = env.put_creatures(env.p2, "Frail", 1, 1, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(frail), "exile_area")
        self.assertNotIn(frail, env.p2.graveyard)

    async def test_unleash_the_elements_lethal_own_creature_exiled(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Unleash_the_Elements/model.py", "Unleash_the_Elements")
        env = self.make_env()
        card = card_cls(env.p1)
        frail_self = env.put_creatures(env.p1, "Frail Ally", 1, 1, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(frail_self), "exile_area")

    async def test_unleash_the_elements_tough_creature_survives_with_damage(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Unleash_the_Elements/model.py", "Unleash_the_Elements")
        env = self.make_env()
        card = card_cls(env.p1)
        tough = env.put_creatures(env.p2, "Tough", 4, 5, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(tough), "battlefield")
        self.assertEqual(tough.state, (4, 2))

    async def test_unleash_the_elements_player_life_totals_unchanged(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Unleash_the_Elements/model.py", "Unleash_the_Elements")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p1, "X", 2, 4, 1)
        env.put_creatures(env.p2, "Y", 2, 4, 1)
        p1l, p2l = env.p1.life, env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, p1l)
        self.assertEqual(env.p2.life, p2l)
