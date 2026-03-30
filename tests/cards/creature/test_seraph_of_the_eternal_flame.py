from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestSeraph_of_the_Eternal_Flame(CardTestCaseBase):
    async def test_seraph_attack_grants_indestructible_to_friendly_creatures(self):
        card_cls = load_card_class_from_path("pycards/creature/Seraph_of_the_Eternal_Flame/model.py", "Seraph_of_the_Eternal_Flame")
        env = self.make_env()
        card = card_cls(env.p1)

        ally = env.put_creatures(env.p1, "Ally", 2, 2, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        seraph = env.get_battlefield_creature(env.p1, "Seraph of the Eternal Flame")
        self.assertNotIn("Indestructible", [type(b).__name__ for b in ally.buffs])
        self.assertNotIn("Indestructible", [type(b).__name__ for b in seraph.buffs])

        await env.trigger(seraph, "when_start_attcak", env.p2, env.p1, env.p2)
        self.assert_state(seraph, {"buffs_contains": ["Indestructible"]})
        self.assert_state(ally, {"buffs_contains": ["Indestructible"]})

    async def test_seraph_attack_does_not_grant_indestructible_to_opponent_creatures(self):
        card_cls = load_card_class_from_path("pycards/creature/Seraph_of_the_Eternal_Flame/model.py", "Seraph_of_the_Eternal_Flame")
        env = self.make_env()
        card = card_cls(env.p1)
        foe = env.put_creatures(env.p2, "Foe", 2, 2, 1)[0]
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        seraph = env.get_battlefield_creature(env.p1, "Seraph of the Eternal Flame")
        await env.trigger(seraph, "when_start_attcak", env.p2, env.p1, env.p2)
        self.assertNotIn("Indestructible", [type(b).__name__ for b in foe.buffs])

    async def test_seraph_attack_trigger_does_not_change_controller_life(self):
        card_cls = load_card_class_from_path("pycards/creature/Seraph_of_the_Eternal_Flame/model.py", "Seraph_of_the_Eternal_Flame")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_creatures(env.p1, "Ally", 2, 2, 1)
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        seraph = env.get_battlefield_creature(env.p1, "Seraph of the Eternal Flame")
        life = env.p1.life
        await env.trigger(seraph, "when_start_attcak", env.p2, env.p1, env.p2)
        self.assertEqual(env.p1.life, life)
