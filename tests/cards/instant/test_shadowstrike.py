from unittest.mock import patch

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest


class TestShadowstrike(CardTestCaseBase):
    async def test_shadowstrike_destroys_tapped_creature_and_draws(self):
        card_cls = load_card_class_from_path("pycards/Instant/Shadowstrike/model.py", "Shadowstrike")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Tapped Enemy", 2, 2, 1)[0]
        target.flag_dict["tap"] = True
        hand_before = len(env.p1.hand)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(target), "graveyard")
        self.assertEqual(len(env.p1.hand), hand_before)
        self.assertEqual(env.p1.life, 20)
        self.assertEqual(env.p2.life, 20)

    async def test_shadowstrike_untapped_creature_not_destroyed_but_still_draws(self):
        card_cls = load_card_class_from_path("pycards/Instant/Shadowstrike/model.py", "Shadowstrike")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = [Forest(env.p1)]
        env.p1.hand.clear()
        env.put_in_hand(card, env.p1)

        target = env.put_creatures(env.p2, "Untapped Enemy", 2, 2, 1)[0]
        target.flag_dict["tap"] = False
        env.script_selection(env.p1, [0])
        hand_before = len(env.p1.hand)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(target), "battlefield")
        self.assertEqual(len(env.p1.hand), hand_before)

    async def test_shadowstrike_destroy_draws_from_library(self):
        """Implementation draws after any valid target selection; verify library/hand when a tapped creature dies."""
        card_cls = load_card_class_from_path("pycards/Instant/Shadowstrike/model.py", "Shadowstrike")
        env = self.make_env()
        card = card_cls(env.p1)
        top = Forest(env.p1)
        env.p1.library = [top]
        env.p1.hand.clear()
        env.put_in_hand(card, env.p1)

        target = env.put_creatures(env.p2, "Tapped Victim", 2, 2, 1)[0]
        target.flag_dict["tap"] = True
        env.script_selection(env.p1, [0])

        lib_before = len(env.p1.library)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(target), "graveyard")
        self.assertEqual(len(env.p1.library), lib_before - 1)
        self.assertIn(top, env.p1.hand)
        self.assertEqual(env.p2.life, 20)

    async def test_shadowstrike_two_enemies_only_chosen_tapped_dies(self):
        """Auto-targeting uses random.choice over all_creatures; patch forces the tapped foe."""
        card_cls = load_card_class_from_path("pycards/Instant/Shadowstrike/model.py", "Shadowstrike")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = [Forest(env.p1)]
        env.p1.hand.clear()
        env.put_in_hand(card, env.p1)

        loose = env.put_creatures(env.p2, "Loose", 3, 3, 1)[0]
        loose.flag_dict["tap"] = False
        tapped = env.put_creatures(env.p2, "Marked", 2, 2, 1)[0]
        tapped.flag_dict["tap"] = True

        def _pick_tapped(seq):
            for c in seq:
                if c.get_flag("tap"):
                    return c
            return seq[0]

        with patch("game.game_function_tool.random.choice", side_effect=_pick_tapped):
            result = await env.play_card(card, env.p1)
            await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(loose), "battlefield")
        self.assertEqual(env.card_zone(tapped), "graveyard")
