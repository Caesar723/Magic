from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Mountain.model import Mountain
from unittest.mock import patch


class TestPyroblast_Surge(CardTestCaseBase):
    async def test_pyroblast_surge_bonus_damage_with_untapped_mountain(self):
        card_cls = load_card_class_from_path("pycards/Instant/Pyroblast_Surge/model.py", "Pyroblast_Surge")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.land_area.append(Mountain(env.p1))
        target = env.put_creatures(env.p2, "Pyro Target", 2, 4, 1)[0]
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertNotEqual(env.card_zone(target), "battlefield")

    async def test_pyroblast_surge_tapped_mountain_only_three_damage(self):
        card_cls = load_card_class_from_path("pycards/Instant/Pyroblast_Surge/model.py", "Pyroblast_Surge")
        env = self.make_env()
        card = card_cls(env.p1)
        m = Mountain(env.p1)
        m.flag_dict["tap"] = True
        env.p1.land_area.append(m)
        target = env.put_creatures(env.p2, "Tough", 2, 4, 1)[0]
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(target.state[1], 1)

    async def test_pyroblast_surge_controller_life_unchanged(self):
        card_cls = load_card_class_from_path("pycards/Instant/Pyroblast_Surge/model.py", "Pyroblast_Surge")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.land_area.append(Mountain(env.p1))
        env.put_creatures(env.p2, "T", 2, 4, 1)
        life = env.p1.life
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, life)
