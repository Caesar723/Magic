from pycards.land.Forest.model import Forest

from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestNature_s_Embrace(CardTestCaseBase):
    async def test_nature_s_embrace_puts_creature_from_library_tapped(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Nature_s_Embrace/model.py", "Nature_s_Embrace")
        creature_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)

        creature = creature_cls(env.p1)
        env.p1.library = [creature]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        found = env.find_card_by_name(env.p1, "Night Stalker", zones=("battlefield",))
        self.assertIsNotNone(found)
        self.assertTrue(found.get_flag("tap"))

    async def test_nature_s_embrace_no_creature_in_library_resolves_cleanly(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Nature_s_Embrace/model.py", "Nature_s_Embrace")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = [Forest(env.p1)]

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.battlefield), 0)
        self.assertEqual(len(env.p1.library), 1)

    async def test_nature_s_embrace_opponent_life_unchanged_on_creature_tutor(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Nature_s_Embrace/model.py", "Nature_s_Embrace")
        creature_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p1.library = [creature_cls(env.p1)]
        opp = env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp)
