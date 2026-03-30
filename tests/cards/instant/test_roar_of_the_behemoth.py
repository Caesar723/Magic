from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestRoar_of_the_Behemoth(CardTestCaseBase):
    async def test_roar_of_the_behemoth_sets_enemy_power_to_zero(self):
        card_cls = load_card_class_from_path("pycards/Instant/Roar_of_the_Behemoth/model.py", "Roar_of_the_Behemoth")
        env = self.make_env()
        card = card_cls(env.p1)

        enemy = env.put_creatures(env.p2, "Enemy", 5, 5, 1)[0]
        enemy_two = env.put_creatures(env.p2, "Enemy Two", 2, 4, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(enemy.state[0], 0)
        self.assertEqual(enemy_two.state[0], 0)

        buffs = [b for b in enemy.buffs if b.__class__.__name__ == "Roar_of_the_Behemoth_Buff"]
        self.assertEqual(len(buffs), 1)
        buffs[0].when_end_turn()
        self.assertEqual(enemy.state[0], 5)

    async def test_roar_of_the_behemoth_does_not_change_friendly_power(self):
        card_cls = load_card_class_from_path("pycards/Instant/Roar_of_the_Behemoth/model.py", "Roar_of_the_Behemoth")
        env = self.make_env()
        card = card_cls(env.p1)

        friendly = env.put_creatures(env.p1, "Friendly", 4, 4, 1)[0]
        env.put_creatures(env.p2, "Enemy", 3, 3, 1)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(friendly.state[0], 4)

    async def test_roar_of_the_behemoth_empty_enemy_board_still_resolves(self):
        card_cls = load_card_class_from_path("pycards/Instant/Roar_of_the_Behemoth/model.py", "Roar_of_the_Behemoth")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p2.battlefield.clear()
        life_before = env.p1.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, life_before)
        self.assertIsNotNone(env.find_card_by_name(env.p1, "Roar of the Behemoth", zones=("graveyard",)))
