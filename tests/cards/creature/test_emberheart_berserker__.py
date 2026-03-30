from tests.cards.base_env import CardTestCaseBase, load_card_class_from_path


class TestEmberheart_Berserker__(CardTestCaseBase):
    async def test_emberheart_berserker_defend_gets_toughness_from_mountains(self):
        card_cls = load_card_class_from_path("pycards/creature/Emberheart_Berserker__/model.py", "Emberheart_Berserker__")
        env = self.make_env()
        card = card_cls(env.p1)

        mountain_cls = card.when_start_defend.__globals__["Mountain"]
        env.p1.land_area.append(mountain_cls(env.p1))
        env.p1.land_area.append(mountain_cls(env.p1))

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        berserker = env.get_battlefield_creature(env.p1, "Emberheart Berserker")
        before = berserker.state
        await env.trigger(berserker, "when_start_defend", env.p2, env.p1, env.p2)
        self.assertEqual(berserker.state[0], before[0])
        self.assertEqual(berserker.state[1], before[1] + 2)

    async def test_emberheart_berserker_defend_without_mountains_no_toughness_buff(self):
        card_cls = load_card_class_from_path("pycards/creature/Emberheart_Berserker__/model.py", "Emberheart_Berserker__")
        env = self.make_env()
        card = card_cls(env.p1)

        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])

        berserker = env.get_battlefield_creature(env.p1, "Emberheart Berserker")
        before = tuple(berserker.state)
        await env.trigger(berserker, "when_start_defend", env.p2, env.p1, env.p2)
        self.assertEqual(tuple(berserker.state), before)

    async def test_emberheart_berserker_single_mountain_adds_one_toughness_on_defend(self):
        card_cls = load_card_class_from_path("pycards/creature/Emberheart_Berserker__/model.py", "Emberheart_Berserker__")
        env = self.make_env()
        card = card_cls(env.p1)
        mountain_cls = card.when_start_defend.__globals__["Mountain"]
        env.p1.land_area.append(mountain_cls(env.p1))
        result = await env.play_card(card, env.p1)
        await env.resolve_stack()
        self.assertTrue(result[0])
        berserker = env.get_battlefield_creature(env.p1, "Emberheart Berserker")
        before = berserker.state
        await env.trigger(berserker, "when_start_defend", env.p2, env.p1, env.p2)
        self.assertEqual(berserker.state[0], before[0])
        self.assertEqual(berserker.state[1], before[1] + 1)
