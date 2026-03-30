from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.creature.Elite_Squire.model import Elite_Squire
from pycards.land.Forest.model import Forest
from pycards.land.Plains.model import Plains


class TestVerdant_Harvest(CardTestCaseBase):
    async def test_verdant_harvest_puts_tapped_land_and_draws(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Verdant_Harvest/model.py", "Verdant_Harvest")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.library = [Forest(env.p1), Plains(env.p1)]
        hand_before = len(env.p1.hand)
        lands_before = len(env.p1.land_area)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.land_area), lands_before + 1)
        self.assertTrue(env.p1.land_area[0].get_flag("tap"))
        self.assertEqual(len(env.p1.hand), hand_before + 1)

    async def test_verdant_harvest_no_basic_in_library_no_land_no_draw(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Verdant_Harvest/model.py", "Verdant_Harvest")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.hand.clear()
        env.put_in_hand(card, env.p1)
        env.p1.library = [Elite_Squire(env.p1)]
        lands_before = len(env.p1.land_area)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.land_area), lands_before)
        self.assertEqual(len(env.p1.hand), 0)

    async def test_verdant_harvest_opponent_life_unchanged(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Verdant_Harvest/model.py", "Verdant_Harvest")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = [Forest(env.p1), Plains(env.p1)]
        opp = env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp)
