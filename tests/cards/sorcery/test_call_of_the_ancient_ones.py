from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestCall_of_the_Ancient_Ones(CardTestCaseBase):
    async def test_call_of_the_ancient_ones_reanimates_from_graveyard(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Call_of_the_Ancient_Ones/model.py", "Call_of_the_Ancient_Ones")
        creature_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)

        target = creature_cls(env.p2)
        env.p2.graveyard.append(target)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertIn(target, env.p1.battlefield)
        self.assertNotIn(target, env.p2.graveyard)

    async def test_call_of_the_ancient_ones_empty_graveyards_resolves(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Call_of_the_Ancient_Ones/model.py", "Call_of_the_Ancient_Ones")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.graveyard.clear()
        env.p2.graveyard.clear()
        bf_before = len(env.p1.battlefield)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.battlefield), bf_before)

    async def test_call_of_the_ancient_ones_reanimates_from_controller_graveyard(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Call_of_the_Ancient_Ones/model.py", "Call_of_the_Ancient_Ones")
        creature_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)

        target = creature_cls(env.p1)
        env.p1.graveyard.append(target)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertIn(target, env.p1.battlefield)
        self.assertNotIn(target, env.p1.graveyard)
