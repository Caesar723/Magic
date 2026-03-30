from unittest.mock import patch

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestDivine_Blessing(CardTestCaseBase):
    async def test_divine_blessing_plus_two_plus_two_and_lifelink(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Divine_Blessing/model.py", "Divine_Blessing")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p1, "Blessed", 2, 2, 1)[0]
        before = target.state

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(target.state, (before[0] + 2, before[1] + 2))
        self.assertTrue(target.get_flag("lifelink"))

    async def test_divine_blessing_expires_end_turn(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Divine_Blessing/model.py", "Divine_Blessing")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p1, "Blessed", 2, 2, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(target.state, (4, 4))

        for buff in list(target.buffs):
            if buff.__class__.__name__ in {"StateBuff", "KeyBuff"}:
                buff.when_end_turn()
        self.assertEqual(target.state, (2, 2))
        self.assertFalse(target.get_flag("lifelink"))

    async def test_divine_blessing_does_not_buff_enemy_creatures(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Divine_Blessing/model.py", "Divine_Blessing")
        env = self.make_env()
        card = card_cls(env.p1)
        ally = env.put_creatures(env.p1, "Ally", 2, 2, 1)[0]
        foe = env.put_creatures(env.p2, "Foe", 2, 2, 1)[0]
        before = foe.state

        def _pick_ally(seq):
            return ally if ally in seq else seq[0]

        with patch("game.game_function_tool.random.choice", side_effect=_pick_ally):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(foe.state, before)
        self.assertFalse(foe.get_flag("lifelink"))
