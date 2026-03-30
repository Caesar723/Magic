from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from unittest.mock import patch


class TestCelestial_Convergence(CardTestCaseBase):
    async def test_celestial_convergence_exiles_and_gains_life_for_small_mv(self):
        card_cls = load_card_class_from_path("pycards/Instant/Celestial_Convergence/model.py", "Celestial_Convergence")
        ns_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)

        target = ns_cls(env.p2)
        env.put_on_battlefield(target, env.p2)
        mv = sum(target.cost.values())
        self.assertLessEqual(mv, 3)
        env.p1.life = 10
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(target), "exile_area")
        self.assertEqual(env.p1.life, 10 + mv)
        self.assertEqual(env.p2.life, 20)

    async def test_celestial_convergence_exiles_high_mv_without_life_gain(self):
        card_cls = load_card_class_from_path("pycards/Instant/Celestial_Convergence/model.py", "Celestial_Convergence")
        titan_cls = load_card_class_from_path("pycards/creature/Inferno_Titan/model.py", "Inferno_Titan")
        env = self.make_env()
        card = card_cls(env.p1)

        target = titan_cls(env.p2)
        env.put_on_battlefield(target, env.p2)
        mv = sum(target.cost.values())
        self.assertGreater(mv, 3)
        env.p1.life = 20
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(target), "exile_area")
        self.assertEqual(env.p1.life, 20)
        self.assertEqual(env.p2.life, 20)

    async def test_celestial_convergence_opponent_creature_small_mv_exile_no_opponent_life_change(self):
        card_cls = load_card_class_from_path("pycards/Instant/Celestial_Convergence/model.py", "Celestial_Convergence")
        ns_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)
        target = ns_cls(env.p2)
        env.put_on_battlefield(target, env.p2)
        mv = sum(target.cost.values())
        env.p1.life = 11
        env.p2.life = 7
        with patch("game.game_function_tool.random.choice", side_effect=lambda seq: seq[0]):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.card_zone(target), "exile_area")
        self.assertEqual(env.p1.life, 11 + mv)
        self.assertEqual(env.p2.life, 7)
