from unittest.mock import AsyncMock, patch

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.creature.Elite_Squire.model import Elite_Squire
from pycards.land.Forest.model import Forest


class TestWild_Growth(CardTestCaseBase):
    async def test_wild_growth_fetches_one_tapped_land(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Wild_Growth/model.py", "Wild_Growth")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.library = [Forest(env.p1)]
        lands_before = len(env.p1.land_area)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.land_area), lands_before + 1)
        self.assertTrue(env.p1.land_area[-1].get_flag("tap"))

    async def test_wild_growth_no_land_still_invokes_scry(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Wild_Growth/model.py", "Wild_Growth")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = [Elite_Squire(env.p1)]
        lands_before = len(env.p1.land_area)
        with patch.object(card_cls, "Scry", new_callable=AsyncMock) as mock_scry:
            result = await env.play_card(card, env.p1)
            await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.land_area), lands_before)
        mock_scry.assert_awaited_once()

    async def test_wild_growth_opponent_hand_unchanged(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Wild_Growth/model.py", "Wild_Growth")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = [Forest(env.p1)]
        opp_hand_before = len(env.p2.hand)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.hand), opp_hand_before)
