from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestEssence_Channeler(CardTestCaseBase):
    async def test_essence_channeler_adds_green_on_creature_cast_trigger(self):
        card_cls = load_card_class_from_path("pycards/creature/Essence_Channeler/model.py", "Essence_Channeler")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_on_battlefield(card, env.p1)
        other = env.create_creature(env.p1, "Other Creature", 1, 1)
        green_before = env.p1.mana["G"]

        await env.trigger(card, "when_play_a_card", other, env.p1, env.p2)
        self.assertEqual(env.p1.mana["G"], green_before + 1)

    async def test_essence_channeler_does_not_trigger_on_non_creature_spell(self):
        card_cls = load_card_class_from_path("pycards/creature/Essence_Channeler/model.py", "Essence_Channeler")
        spell_cls = load_card_class_from_path("pycards/Instant/Swift_Ward/model.py", "Swift_Ward")
        env = self.make_env()
        card = card_cls(env.p1)

        env.put_on_battlefield(card, env.p1)
        green_before = env.p1.mana["G"]
        await env.trigger(card, "when_play_a_card", spell_cls(env.p1), env.p1, env.p2)
        self.assertEqual(env.p1.mana["G"], green_before)

    async def test_essence_channeler_does_not_add_mana_for_opponent_casts(self):
        card_cls = load_card_class_from_path("pycards/creature/Essence_Channeler/model.py", "Essence_Channeler")
        env = self.make_env()
        card = card_cls(env.p1)
        env.put_on_battlefield(card, env.p1)
        opp_creature = env.create_creature(env.p2, "Opp Creature", 1, 1)
        g_before = env.p1.mana["G"]
        await env.trigger(card, "when_play_a_card", opp_creature, env.p2, env.p1)
        self.assertEqual(env.p1.mana["G"], g_before)
