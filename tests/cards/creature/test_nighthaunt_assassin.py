from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestNighthaunt_Assassin(CardTestCaseBase):
    async def test_nighthaunt_assassin_etb_destroys_low_cost_enemy_creature(self):
        card_cls = load_card_class_from_path("pycards/creature/Nighthaunt_Assassin/model.py", "Nighthaunt_Assassin")
        env = self.make_env()
        card = card_cls(env.p1)

        low = env.put_creatures(env.p2, "Low CMC", 2, 2, 1)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        assassin = env.get_battlefield_creature(env.p1, "Nighthaunt Assassin")
        self.assert_state(assassin, {"zone": "battlefield", "state": (2, 1)})
        self.assertIn(env.card_zone(low), {"graveyard", "exile_area"})

    async def test_nighthaunt_assassin_etb_skips_when_only_high_cmc_enemies(self):
        card_cls = load_card_class_from_path("pycards/creature/Nighthaunt_Assassin/model.py", "Nighthaunt_Assassin")
        env = self.make_env()
        card = card_cls(env.p1)
        expensive = env.create_creature(env.p2, "High CMC", 4, 4)
        expensive.mana_cost = "6"
        env.put_on_battlefield(expensive, env.p2)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(expensive), "battlefield")
        self.assertEqual(expensive.state, (4, 4))

    async def test_nighthaunt_assassin_etb_no_op_when_opponent_board_empty(self):
        card_cls = load_card_class_from_path("pycards/creature/Nighthaunt_Assassin/model.py", "Nighthaunt_Assassin")
        env = self.make_env()
        card = card_cls(env.p1)
        self.assertFalse(env.p2.battlefield)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        assassin = env.get_battlefield_creature(env.p1, "Nighthaunt Assassin")
        self.assertEqual(env.card_zone(assassin), "battlefield")
