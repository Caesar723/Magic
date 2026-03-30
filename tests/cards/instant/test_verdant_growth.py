from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from unittest.mock import patch


class TestVerdant_Growth(CardTestCaseBase):
    async def test_verdant_growth_gives_plus_four_plus_four(self):
        card_cls = load_card_class_from_path("pycards/Instant/Verdant_Growth/model.py", "Verdant_Growth")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p1, "Buff Target", 2, 2, 1)[0]
        env.script_selection(env.p1, [0])
        before = target.state

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(target.state, (before[0] + 4, before[1] + 4))

    async def test_verdant_growth_treefolk_also_gets_trample(self):
        card_cls = load_card_class_from_path("pycards/Instant/Verdant_Growth/model.py", "Verdant_Growth")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.create_creature(env.p1, "Treefolk Target", 2, 2)
        target.type_card = "Treefolk Creature"
        env.put_on_battlefield(target, env.p1)
        env.script_selection(env.p1, [0])

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertTrue(target.get_flag("Trample"))

    async def test_verdant_growth_does_not_buff_opponent_creature(self):
        card_cls = load_card_class_from_path("pycards/Instant/Verdant_Growth/model.py", "Verdant_Growth")
        env = self.make_env()
        card = card_cls(env.p1)
        ally = env.put_creatures(env.p1, "Ally", 1, 1, 1)[0]
        foe = env.put_creatures(env.p2, "Foe", 1, 1, 1)[0]
        with patch(
            "game.game_function_tool.random.choice",
            side_effect=lambda seq: ally if ally in seq else seq[0],
        ):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(ally.state, (5, 5))
        self.assertEqual(foe.state, (1, 1))
