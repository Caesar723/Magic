from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from unittest.mock import patch


class TestInferno_Titan(CardTestCaseBase):
    async def test_inferno_titan_etb_deals_four_when_no_enemy_creatures(self):
        card_cls = load_card_class_from_path("pycards/creature/Inferno_Titan/model.py", "Inferno_Titan")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        titan = env.get_battlefield_creature(env.p1, "Inferno Titan")
        self.assert_state(titan, {"zone": "battlefield", "state": (6, 6)})
        self.assertEqual(env.p2.life, 16)

    async def test_inferno_titan_can_ping_enemy_creature(self):
        card_cls = load_card_class_from_path("pycards/creature/Inferno_Titan/model.py", "Inferno_Titan")
        env = self.make_env()
        card = card_cls(env.p1)

        target = env.put_creatures(env.p2, "Titan Target", 2, 2, 1)[0]
        before_life = target.state[1]
        with patch(
            "pycards.creature.Inferno_Titan.model.random.choice",
            side_effect=lambda seq: target if target in seq else seq[0],
        ):
            result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertTrue(target.state[1] < before_life or env.p2.life < 20)

    async def test_inferno_titan_controller_life_unchanged_on_etb(self):
        card_cls = load_card_class_from_path("pycards/creature/Inferno_Titan/model.py", "Inferno_Titan")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.life = 7

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, 7)
