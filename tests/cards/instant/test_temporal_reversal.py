from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest
from unittest.mock import patch


class TestTemporal_Reversal(CardTestCaseBase):
    async def test_temporal_reversal_bounces_and_untaps_two_lands(self):
        card_cls = load_card_class_from_path("pycards/Instant/Temporal_Reversal/model.py", "Temporal_Reversal")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Return Me", 2, 2, 1)[0]
        l1, l2 = Forest(env.p1), Forest(env.p1)
        env.p1.land_area.extend([l1, l2])
        l1.flag_dict["tap"] = True
        l2.flag_dict["tap"] = True

        with patch(
            "game.game_function_tool.random.choice",
            side_effect=lambda seq: target if target in seq else seq[0],
        ):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertNotEqual(env.card_zone(target), "battlefield")
        self.assertFalse(l1.get_flag("tap"))
        self.assertFalse(l2.get_flag("tap"))

    async def test_temporal_reversal_untaps_at_most_one_tapped_land(self):
        card_cls = load_card_class_from_path("pycards/Instant/Temporal_Reversal/model.py", "Temporal_Reversal")
        env = self.make_env()
        card = card_cls(env.p1)
        target = env.put_creatures(env.p2, "Return Me", 2, 2, 1)[0]
        l1, l2 = Forest(env.p1), Forest(env.p1)
        env.p1.land_area.extend([l1, l2])
        l1.flag_dict["tap"] = True
        l2.flag_dict["tap"] = False
        with patch(
            "game.game_function_tool.random.choice",
            side_effect=lambda seq: target if target in seq else seq[0],
        ):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertFalse(l1.get_flag("tap"))
        self.assertFalse(l2.get_flag("tap"))

    async def test_temporal_reversal_controller_life_unchanged(self):
        card_cls = load_card_class_from_path("pycards/Instant/Temporal_Reversal/model.py", "Temporal_Reversal")
        env = self.make_env()
        card = card_cls(env.p1)
        target = env.put_creatures(env.p2, "Return Me", 2, 2, 1)[0]
        l1 = Forest(env.p1)
        env.p1.land_area.append(l1)
        l1.flag_dict["tap"] = True
        life = env.p1.life
        with patch(
            "game.game_function_tool.random.choice",
            side_effect=lambda seq: target if target in seq else seq[0],
        ):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, life)
