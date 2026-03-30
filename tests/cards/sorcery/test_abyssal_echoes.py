from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestAbyssal_Echoes(CardTestCaseBase):
    async def test_abyssal_echoes_cheats_large_creature_from_library(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Abyssal_Echoes/model.py", "Abyssal_Echoes")
        big_cls = load_card_class_from_path("pycards/creature/Blightsteel_Colossus/model.py", "Blightsteel_Colossus")
        small_cls = load_card_class_from_path("pycards/creature/Tidal_Sprite/model.py", "Tidal_Sprite")
        env = self.make_env()
        card = card_cls(env.p1)

        small = small_cls(env.p1)
        big = big_cls(env.p1)
        env.p1.library = [small, big]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertTrue(any(c.name == "Blightsteel Colossus" for c in env.p1.battlefield))
        self.assertIn(small, env.p1.library)

    async def test_abyssal_echoes_no_seven_plus_creature_in_library_no_op(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Abyssal_Echoes/model.py", "Abyssal_Echoes")
        small_cls = load_card_class_from_path("pycards/creature/Tidal_Sprite/model.py", "Tidal_Sprite")
        env = self.make_env()
        card = card_cls(env.p1)
        only_small = small_cls(env.p1)
        env.p1.library = [only_small]
        bf_before = len(env.p1.battlefield)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.battlefield), bf_before)
        self.assertIn(only_small, env.p1.library)

    async def test_abyssal_echoes_opponent_library_unchanged(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Abyssal_Echoes/model.py", "Abyssal_Echoes")
        big_cls = load_card_class_from_path("pycards/creature/Blightsteel_Colossus/model.py", "Blightsteel_Colossus")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p2.library = [big_cls(env.p2)]
        lib_before = list(env.p2.library)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(env.p2.library, lib_before)
