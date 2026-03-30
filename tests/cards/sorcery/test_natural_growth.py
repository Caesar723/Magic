from unittest.mock import patch

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestNatural_Growth(CardTestCaseBase):
    async def test_natural_growth_gives_plus_two_plus_two_until_end_turn(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Natural_Growth/model.py", "Natural_Growth")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p1, "Growth Target", 2, 2, 1)[0]
        before = target.state

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(target.state, (before[0] + 2, before[1] + 2))

    async def test_natural_growth_bonus_expires_end_turn(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Natural_Growth/model.py", "Natural_Growth")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p1, "Growth Target", 2, 2, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(target.state, (4, 4))

        state_buffs = [b for b in target.buffs if b.__class__.__name__ == "StateBuff"]
        self.assertEqual(len(state_buffs), 1)
        state_buffs[0].when_end_turn()
        self.assertEqual(target.state, (2, 2))

    async def test_natural_growth_does_not_buff_unselected_creature(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Natural_Growth/model.py", "Natural_Growth")
        env = self.make_env()
        card = card_cls(env.p1)
        ally = env.put_creatures(env.p1, "Ally", 2, 2, 1)[0]
        foe = env.put_creatures(env.p2, "Foe", 2, 2, 1)[0]

        def _pick_ally(seq):
            return ally if ally in seq else seq[0]

        with patch("game.game_function_tool.random.choice", side_effect=_pick_ally):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(ally.state, (4, 4))
        self.assertEqual(foe.state, (2, 2))
