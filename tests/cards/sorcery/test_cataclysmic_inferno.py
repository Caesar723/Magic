from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Mountain.model import Mountain


class TestCataclysmic_Inferno(CardTestCaseBase):
    async def test_cataclysmic_inferno_scales_with_mountains_and_makes_tokens(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Cataclysmic_Inferno/model.py", "Cataclysmic_Inferno")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.land_area.extend([Mountain(env.p1), Mountain(env.p1)])
        env.put_creatures(env.p2, "Enemy A", 2, 2, 1)
        env.put_creatures(env.p2, "Enemy B", 2, 2, 1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertTrue(any(c.name == "Elemental Creature" for c in env.p1.battlefield))

    async def test_cataclysmic_inferno_zero_mountains_deals_no_damage_and_no_tokens(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Cataclysmic_Inferno/model.py", "Cataclysmic_Inferno")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.land_area.clear()
        env.put_creatures(env.p2, "Enemy", 2, 2, 1)
        enemy = env.p2.battlefield[0]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(enemy.state, (2, 2))
        self.assertFalse(any(c.name == "Elemental Creature" for c in env.p1.battlefield))

    async def test_cataclysmic_inferno_controller_life_unchanged_with_zero_mountains(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Cataclysmic_Inferno/model.py", "Cataclysmic_Inferno")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.land_area.clear()
        life = env.p1.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p1.life, life)
