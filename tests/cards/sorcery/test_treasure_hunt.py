from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path
from pycards.creature.Elite_Squire.model import Elite_Squire
from pycards.land.Forest.model import Forest


class TestTreasure_Hunt(CardTestCaseBase):
    async def test_treasure_hunt_moves_revealed_lands_to_hand(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Treasure_Hunt/model.py", "Treasure_Hunt")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p1.library = [Forest(env.p1)]
        hand_before = len(env.p1.hand)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.hand), hand_before + 1)

    async def test_treasure_hunt_nonland_top_card_goes_to_graveyard(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Treasure_Hunt/model.py", "Treasure_Hunt")
        env = self.make_env()
        card = card_cls(env.p1)
        creature = Elite_Squire(env.p1)
        env.p1.library = [creature]
        lib_before = len(env.p1.library)
        gy_before = len(env.p1.graveyard)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.library), lib_before - 1)
        self.assertIn(creature, env.p1.graveyard)
        self.assertGreaterEqual(len(env.p1.graveyard), gy_before + 1)

    async def test_treasure_hunt_reveals_at_most_five_from_six_card_library(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Treasure_Hunt/model.py", "Treasure_Hunt")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.hand.clear()
        env.put_in_hand(card, env.p1)
        env.p1.library = [Forest(env.p1) for _ in range(6)]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.library), 1)
        self.assertEqual(sum(1 for c in env.p1.hand if c.name == "Forest"), 5)
