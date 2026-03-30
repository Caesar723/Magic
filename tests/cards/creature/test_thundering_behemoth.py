from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestThundering_Behemoth(CardTestCaseBase):
    async def test_thundering_behemoth_etb_grants_team_trample(self):
        card_cls = load_card_class_from_path("pycards/creature/Thundering_Behemoth/model.py", "Thundering_Behemoth")
        env = self.make_env()
        card = card_cls(env.p1)

        ally = env.put_creatures(env.p1, "Ally", 2, 2, 1)[0]
        enemy = env.put_creatures(env.p2, "Enemy", 2, 2, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        behemoth = env.get_battlefield_creature(env.p1, "Thundering Behemoth")
        self.assert_state(behemoth, {"zone": "battlefield", "state": (6, 5), "flags": {"Trample": True}})
        self.assertTrue(ally.get_flag("Trample"))
        self.assertFalse(enemy.get_flag("Trample"))

    async def test_thundering_behemoth_team_trample_buff_ends_after_end_step_hooks(self):
        card_cls = load_card_class_from_path("pycards/creature/Thundering_Behemoth/model.py", "Thundering_Behemoth")
        env = self.make_env()
        card = card_cls(env.p1)
        ally = env.put_creatures(env.p1, "Ally EOT", 2, 2, 1)[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertTrue(ally.get_flag("Trample"))

        for buff in list(ally.buffs):
            if type(buff).__name__ == "KeyBuff" and getattr(buff, "key_name", None) == "Trample":
                buff.when_end_turn()
        self.assertFalse(ally.get_flag("Trample"))

    async def test_thundering_behemoth_etb_only_buffs_self_when_no_other_creatures(self):
        card_cls = load_card_class_from_path("pycards/creature/Thundering_Behemoth/model.py", "Thundering_Behemoth")
        env = self.make_env()
        card = card_cls(env.p1)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        behemoth = env.get_battlefield_creature(env.p1, "Thundering Behemoth")
        self.assertTrue(behemoth.get_flag("Trample"))
        self.assertFalse(env.p2.battlefield)
