from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestOblivion_Devourer(CardTestCaseBase):
    async def test_oblivion_devourer_attack_sacrifices_weakest_and_discards_two(self):
        card_cls = load_card_class_from_path("pycards/creature/Oblivion_Devourer/model.py", "Oblivion_Devourer")
        filler_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)

        weak = env.put_creatures(env.p1, "Weak Ally", 1, 1, 1)[0]
        env.put_creatures(env.p1, "Strong Ally", 4, 4, 1)
        env.p2.hand.append(filler_cls(env.p2))
        env.p2.hand.append(filler_cls(env.p2))
        env.p2.hand.append(filler_cls(env.p2))

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        devourer = env.get_battlefield_creature(env.p1, "Oblivion Devourer")
        hand_before = len(env.p2.hand)
        await env.trigger(devourer, "when_start_attcak", env.p2, env.p1, env.p2)
        await env.resolve_stack()

        self.assertNotEqual(env.card_zone(weak), "battlefield")
        self.assertEqual(len(env.p2.hand), hand_before - 2)
        self.assert_state(devourer, {"flags": {"Menace": True}})

    async def test_oblivion_devourer_attack_without_other_creatures_skips_sacrifice(self):
        card_cls = load_card_class_from_path("pycards/creature/Oblivion_Devourer/model.py", "Oblivion_Devourer")
        filler_cls = load_card_class_from_path("pycards/creature/Night_Stalker__/model.py", "Night_Stalker__")
        env = self.make_env()
        card = card_cls(env.p1)

        env.p2.hand.extend([filler_cls(env.p2), filler_cls(env.p2)])
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        devourer = env.get_battlefield_creature(env.p1, "Oblivion Devourer")
        hand_before = len(env.p2.hand)
        await env.trigger(devourer, "when_start_attcak", env.p2, env.p1, env.p2)
        await env.resolve_stack()

        self.assertEqual(len(env.p2.hand), hand_before)
        self.assertEqual(env.card_zone(devourer), "battlefield")

    async def test_oblivion_devourer_attack_with_empty_opponent_hand_skips_discard(self):
        card_cls = load_card_class_from_path("pycards/creature/Oblivion_Devourer/model.py", "Oblivion_Devourer")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p1, "Sac Fodder", 1, 1, 1)
        env.p2.hand.clear()

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        devourer = env.get_battlefield_creature(env.p1, "Oblivion Devourer")
        await env.trigger(devourer, "when_start_attcak", env.p2, env.p1, env.p2)
        await env.resolve_stack()

        self.assertEqual(len(env.p2.hand), 0)
