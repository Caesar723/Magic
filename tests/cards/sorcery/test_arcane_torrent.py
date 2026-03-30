from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.land.Forest.model import Forest


class TestArcane_Torrent(CardTestCaseBase):
    async def test_arcane_torrent_puts_sorcery_from_library_to_hand(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Arcane_Torrent/model.py", "Arcane_Torrent")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.library = [Forest(env.p1), card_cls(env.p1)]
        hand_before = len(env.p1.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before + 1)

    async def test_arcane_torrent_no_sorcery_in_library_does_not_add_hand(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Arcane_Torrent/model.py", "Arcane_Torrent")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.library = [Forest(env.p1), Forest(env.p1)]
        hand_before = len(env.p1.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before)

    async def test_arcane_torrent_does_not_add_cards_to_opponent_hand(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Arcane_Torrent/model.py", "Arcane_Torrent")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = [Forest(env.p1), card_cls(env.p1)]
        opp_hand_before = len(env.p2.hand)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p2.hand), opp_hand_before)
