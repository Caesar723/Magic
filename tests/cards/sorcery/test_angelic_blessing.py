from unittest.mock import patch

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestAngelic_Blessing(CardTestCaseBase):
    async def test_angelic_blessing_plus_three_plus_three_and_vigilance(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Angelic_Blessing/model.py", "Angelic_Blessing")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p1, "Blessed", 2, 2, 1)[0]
        before = target.state

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(target.state, (before[0] + 3, before[1] + 3))
        self.assertTrue(target.get_flag("Vigilance"))
        self.assertEqual(env.p2.life, 20)

    async def test_angelic_blessing_buffs_expire_end_of_turn(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Angelic_Blessing/model.py", "Angelic_Blessing")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p1, "Blessed", 2, 2, 1)[0]
        before = target.state

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(target.state, (before[0] + 3, before[1] + 3))

        for buff in list(target.buffs):
            if buff.__class__.__name__ in {"StateBuff", "KeyBuff"}:
                buff.when_end_turn()
        self.assertEqual(target.state, before)
        self.assertFalse(target.get_flag("Vigilance"))

    async def test_angelic_blessing_does_not_buff_opponent_creature_when_ally_scripted(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Angelic_Blessing/model.py", "Angelic_Blessing")
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
        self.assertFalse(foe.get_flag("Vigilance"))
