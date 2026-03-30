from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestEmberheart_Dragonrider(CardTestCaseBase):
    async def test_emberheart_dragonrider_etb_can_grant_haste_when_paid(self):
        card_cls = load_card_class_from_path("pycards/creature/Emberheart_Dragonrider/model.py", "Emberheart_Dragonrider")
        env = self.make_env()
        card = card_cls(env.p1)

        ally = env.put_creatures(env.p1, "Ally", 2, 2, 1)[0]
        env.p1.mana["R"] = 1
        env.script_selection(env.p1, [0])

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        dragonrider = env.get_battlefield_creature(env.p1, "Emberheart Dragonrider")
        self.assert_state(dragonrider, {"zone": "battlefield", "state": (3, 3)})
        self.assertTrue(ally.get_flag("haste") or dragonrider.get_flag("haste"))

    async def test_emberheart_dragonrider_without_red_mana_does_not_grant_haste(self):
        card_cls = load_card_class_from_path("pycards/creature/Emberheart_Dragonrider/model.py", "Emberheart_Dragonrider")
        env = self.make_env()
        card = card_cls(env.p1)

        ally = env.put_creatures(env.p1, "Ally", 2, 2, 1)[0]
        env.p1.mana["R"] = 0

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertFalse(ally.get_flag("haste"))

    async def test_emberheart_dragonrider_paid_haste_buff_targets_selected_creature(self):
        card_cls = load_card_class_from_path("pycards/creature/Emberheart_Dragonrider/model.py", "Emberheart_Dragonrider")
        env = self.make_env()
        card = card_cls(env.p1)
        ally = env.put_creatures(env.p1, "Ally", 2, 2, 1)[0]
        env.p1.mana["R"] = 1
        env.script_selection(env.p1, [0])
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.mana["R"], 0)
        dragonrider = env.get_battlefield_creature(env.p1, "Emberheart Dragonrider")
        self.assertTrue(ally.get_flag("haste"))
        self.assertFalse(dragonrider.get_flag("haste"))
