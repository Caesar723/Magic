from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestDemonic_Ascendance(CardTestCaseBase):
    async def test_demonic_ascendance_steals_creature_from_opponent_hand(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Demonic_Ascendance/model.py", "Demonic_Ascendance")
        creature_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p2.hand.append(creature_cls(env.p2))
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertTrue(any(c.name == "Night Stalker" for c in env.p1.battlefield))
        self.assertFalse(any(c.name == "Night Stalker" for c in env.p2.hand))

    async def test_demonic_ascendance_no_creature_in_hand_no_steal(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Demonic_Ascendance/model.py", "Demonic_Ascendance")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p2.hand = [c for c in env.p2.hand if getattr(c, "type", "") != "Creature"]
        before = len(env.p1.battlefield)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()

        self.assertTrue(result[0])
        self.assertEqual(len(env.p1.battlefield), before)

    async def test_demonic_ascendance_does_not_change_opponent_life(self):
        card_cls = load_card_class_from_path("pycards/sorcery/Demonic_Ascendance/model.py", "Demonic_Ascendance")
        creature_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)
        env.p2.hand.append(creature_cls(env.p2))
        opp_life = env.p2.life
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        self.assertEqual(env.p2.life, opp_life)
