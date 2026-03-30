from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestFlame_Tinkerer(CardTestCaseBase):
    async def test_flame_tinkerer_etb_allows_optional_trigger(self):
        card_cls = load_card_class_from_path("pycards/creature/Flame_Tinkerer/model.py", "Flame_Tinkerer")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Burn Target", 2, 2, 1)[0]
        original_life = target.state[1]

        async def _no_trigger_selection(player=None, opponent=None, selection_random=False):
            return [card.create_selection("Do nothing", 2)]

        card.selection_step = _no_trigger_selection

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        tinkerer = env.get_battlefield_creature(env.p1, "Flame Tinkerer")
        self.assert_state(tinkerer, {"zone": "battlefield", "state": (2, 1)})
        self.assertEqual(target.state[1], original_life)

    async def test_flame_tinkerer_etb_pay_r_deals_one_damage(self):
        card_cls = load_card_class_from_path("pycards/creature/Flame_Tinkerer/model.py", "Flame_Tinkerer")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Burn Target", 2, 2, 1)[0]
        env.p1.mana["R"] = 1

        async def _pick_target(player=None, opponent=None, selection_random=False):
            return [target]

        card.selection_step = _pick_target

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(target.state[1], 1)

    async def test_flame_tinkerer_pay_r_without_mana_skips_damage(self):
        card_cls = load_card_class_from_path("pycards/creature/Flame_Tinkerer/model.py", "Flame_Tinkerer")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Burn Target", 2, 2, 1)[0]
        env.p1.mana["R"] = 0

        async def _pay_and_target(player=None, opponent=None, selection_random=False):
            return [target]

        card.selection_step = _pay_and_target

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(target.state[1], 2)

    async def test_flame_tinkerer_pay_r_kills_one_toughness_creature(self):
        card_cls = load_card_class_from_path("pycards/creature/Flame_Tinkerer/model.py", "Flame_Tinkerer")
        env = self.make_env()
        card = card_cls(env.p1)
        victim = env.put_creatures(env.p2, "One Toughness", 1, 1, 1)[0]
        env.p1.mana["R"] = 1

        async def _pick_victim(player=None, opponent=None, selection_random=False):
            return [victim]

        card.selection_step = _pick_victim

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        await env.room.check_death()
        self.assertEqual(env.card_zone(victim), "graveyard")
