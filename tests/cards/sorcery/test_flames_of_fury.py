from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Mountain.model import Mountain
from unittest.mock import patch


class TestFlames_of_Fury(CardTestCaseBase):
    async def test_flames_of_fury_bonus_damage_with_mountain(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Flames_of_Fury/model.py", "Flames_of_Fury")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.land_area.append(Mountain(env.p1))
        target = env.put_creatures(env.p2, "Fury Target", 2, 4, 1)[0]
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertNotEqual(env.card_zone(target), "battlefield")

    async def test_flames_of_fury_without_mountain_deals_three(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Flames_of_Fury/model.py", "Flames_of_Fury")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.land_area.clear()
        target = env.put_creatures(env.p2, "Tough", 2, 4, 1)[0]
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(target), "battlefield")
        self.assertEqual(target.state, (2, 1))

    async def test_flames_of_fury_controller_life_unchanged_with_mountain_bonus(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Flames_of_Fury/model.py", "Flames_of_Fury")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.land_area.append(Mountain(env.p1))
        env.put_creatures(env.p2, "Fury Target", 2, 4, 1)
        ctrl_life = env.p1.life

        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, ctrl_life)
