from unittest.mock import patch
from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest
from pycards.land.Mountain.model import Mountain


class TestArcane_Intervention(CardTestCaseBase):
    async def test_arcane_intervention_bounces_permanent_and_draws(self):
        card_cls = load_card_class_from_path("pycards/Instant/Arcane_Intervention/model.py", "Arcane_Intervention")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Bounce Target", 2, 2, 1)[0]
        env.p1.library = [Forest(env.p1)]
        p2_hand_before = len(env.p2.hand)
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.hand), p2_hand_before + 1)
        self.assertIsNot(env.p2.hand[-1], target)
        self.assertEqual(env.p1.life, 20)

    async def test_arcane_intervention_targeting_land_only_draws(self):
        card_cls = load_card_class_from_path("pycards/Instant/Arcane_Intervention/model.py", "Arcane_Intervention")
        env = self.make_env()
        card = card_cls(env.p1)

        opp_land = Mountain(env.p2)
        env.p2.land_area.append(opp_land)
        env.p1.library = [Forest(env.p1)]
        p2_hand_before = len(env.p2.hand)
        lands_before = len(env.p2.land_area)
        env.script_selection(env.p1, [opp_land])

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.land_area), lands_before)
        self.assertEqual(len(env.p2.hand), p2_hand_before)
        self.assertTrue(any(c.name == "Forest" for c in env.p1.hand))

    async def test_arcane_intervention_creature_bounce_does_not_change_opponent_life(self):
        card_cls = load_card_class_from_path("pycards/Instant/Arcane_Intervention/model.py", "Arcane_Intervention")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p2, "Punching Bag", 3, 3, 1)
        env.p1.library = [Forest(env.p1)]
        life_before = env.p2.life
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, life_before)
