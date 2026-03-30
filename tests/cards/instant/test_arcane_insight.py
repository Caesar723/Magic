from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest
from pycards.land.Island.model import Island
from pycards.land.Mountain.model import Mountain


class TestArcane_Insight(CardTestCaseBase):
    async def test_arcane_insight_discards_non_spell_choice(self):
        card_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)

        forced_land = Mountain(env.p1)
        env.p1.hand.append(forced_land)
        env.p1.library = [Forest(env.p1), Island(env.p1)]
        env.script_selection(env.p1, [forced_land])

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertGreaterEqual(len(env.p1.hand), 1)

    async def test_arcane_insight_keeps_hand_when_discarding_instant_choice(self):
        card_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        instant_cls = load_card_class_from_path("pycards/Instant/Aquatic_Evasion/model.py", "Aquatic_Evasion")
        env = self.make_env()
        card = card_cls(env.p1)

        keep = instant_cls(env.p1)
        env.p1.hand = [card, keep]
        env.p1.library = [Forest(env.p1), Island(env.p1)]
        env.script_selection(env.p1, [keep])

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertIn(keep, env.p1.hand)
        self.assertEqual(env.card_zone(keep), "hand")

    async def test_arcane_insight_opponent_life_unchanged_after_cast(self):
        card_cls = load_card_class_from_path("pycards/Instant/Arcane_Insight/model.py", "Arcane_Insight")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.hand = [card]
        env.p1.library = [Forest(env.p1), Island(env.p1)]
        opp_life = env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp_life)
