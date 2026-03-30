from unittest.mock import patch

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestEmberheart_Salamander(CardTestCaseBase):
    async def test_emberheart_salamander_has_trample(self):
        card_cls = load_card_class_from_path("pycards/creature/Emberheart_Salamander/model.py", "Emberheart_Salamander")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        salamander = env.get_battlefield_creature(env.p1, "Emberheart Salamander")
        self.assert_state(salamander, {"state": (4, 2), "flags": {"Trample": True}})

    async def test_emberheart_salamander_etb_deals_two_damage(self):
        card_cls = load_card_class_from_path("pycards/creature/Emberheart_Salamander/model.py", "Emberheart_Salamander")
        env = self.make_env()
        card = card_cls(env.p1)
        target = env.put_creatures(env.p2, "Burn Target", 2, 2, 1)[0]

        def _pick_burn_target(seq):
            for item in seq:
                if getattr(item, "name", None) == "Burn Target":
                    return item
            return seq[0]

        with patch("game.game_function_tool.random.choice", side_effect=_pick_burn_target):
            result = await env.play_card(card, env.p1)
            await env.resolve_stack()

        self.assertTrue(result[0])
        env.get_battlefield_creature(env.p1, "Emberheart Salamander")
        await env.room.check_death()
        self.assertTrue(
            target.actual_live < 2 or env.card_zone(target) == "graveyard",
            msg="ETB should deal 2 damage to the scripted target creature",
        )

    async def test_emberheart_salamander_etb_two_damage_to_opponent_player_when_patched(self):
        card_cls = load_card_class_from_path("pycards/creature/Emberheart_Salamander/model.py", "Emberheart_Salamander")
        env = self.make_env()
        card = card_cls(env.p1)

        def _force_opponent(seq):
            for item in seq:
                if item is env.p2:
                    return item
            return seq[0]

        with patch("game.game_function_tool.random.choice", side_effect=_force_opponent):
            before = env.p2.life
            result = await env.play_card(card, env.p1)
            await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, before - 2)
        env.get_battlefield_creature(env.p1, "Emberheart Salamander")

    async def test_emberheart_salamander_trample_deals_excess_to_opponent(self):
        card_cls = load_card_class_from_path("pycards/creature/Emberheart_Salamander/model.py", "Emberheart_Salamander")
        env = self.make_env()
        card = card_cls(env.p1)
        chump = env.put_creatures(env.p2, "Chump", 1, 1, 1)[0]

        def _etb_hits_player(seq):
            for item in seq:
                if item is env.p2:
                    return item
            return seq[0]

        with patch("game.game_function_tool.random.choice", side_effect=_etb_hits_player):
            result = await env.play_card(card, env.p1)
            await env.resolve_stack()
        self.assertTrue(result[0])

        salamander = env.get_battlefield_creature(env.p1, "Emberheart Salamander")
        env.ready_attacker(salamander)
        p2_before = env.p2.life
        await env.simulate_combat(salamander, chump)
        await env.room.check_death()

        self.assertEqual(env.card_zone(chump), "graveyard")
        self.assertEqual(env.p2.life, p2_before - 3)
