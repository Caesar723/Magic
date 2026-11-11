import random


class ScenarioTools:
    scenario_zones=("hand","library","graveyard","battlefield","land_area","exile_area")

    scenario_limits={"hand":10,"library":40,"graveyard":40,"battlefield":10,"land_area":20,"exile_area":40}
    scenario_profiles={
        "sparse":{"weight":0.3,"hand":(0,2),"library":(0,10),"graveyard":(0,6),"battlefield":(0,2),"land_area":(0,3)},
        "normal":{"weight":0.5,"hand":(3,5),"library":(11,25),"graveyard":(7,15),"battlefield":(3,5),"land_area":(4,8)},
        "dense":{"weight":0.2,"hand":(6,9),"library":(26,40),"graveyard":(16,30),"battlefield":(6,9),"land_area":(9,15)},
    }

    def scenario_begin(self,method):
        settings=self.room.env_config.get("scenario_generation",{})
        profiles=settings.get("levels",self.scenario_profiles)
        names=list(profiles)
        self._scenario_level=random.choices(names,[profiles[name].get("weight",1) for name in names])[0]
        self._scenario_profile=profiles[self._scenario_level]
        self._scenario_locks=set()
        visited=set()

        def visit(name):
            if name in visited:
                return
            visited.add(name)
            self._scenario_locks.update(getattr(self,"scenario_locks",{}).get(name,()))
            if name in ("scenario_combat","scenario_unblocked"):
                self._scenario_locks.update(("self.battlefield","opponent.battlefield"))
                return
            if name=="scenario_stack":
                self._scenario_locks.update(("self.battlefield","opponent.battlefield","self.land_area","opponent.land_area","self.graveyard","opponent.graveyard"))
                return
            function=getattr(type(self),name,None)
            if callable(function) and name not in ("scenario_prepare","scenario_cast","scenario_cards","scenario_replace_cards","scenario_random_cards","stage_card","unstage_card"):
                function=getattr(function,"__wrapped__",function)
                for child in getattr(getattr(function,"__code__",None),"co_names",()):
                    if child in getattr(self,"scenario_locks",{}) or child in ("scenario_combat","scenario_unblocked","scenario_stack"):
                        visit(child)
        visit(method.__name__)
        if "without_mana" in method.__name__:
            self._scenario_locks.add("self.land_area")

    def scenario_space(self,owner,zone):
        reserved=owner is self.player and (
            zone=="hand" or zone=="battlefield" and self.card.type=="Creature"
            or zone=="land_area" and self.card.type=="Land"
            or zone=="graveyard" and self.card.type in ("Instant","Sorcery")
        )
        cards=getattr(owner,zone)
        if self.card in cards:
            reserved=False
        return max(0,self.scenario_limits[zone]-len(cards)-int(reserved))

    def scenario_count(self,zone,value=None,minimum=0,reserve=0):
        if not hasattr(self,"_scenario_profile"):
            self.scenario_begin(self.scenario_prepare)
        if value is None:
            value=self._scenario_profile.get(zone,(0,0))
            growth=self.card.effect_params.get("draw_count",0) if zone=="hand" else self.card.effect_params.get("token_count",0) if zone=="battlefield" else 0
            limit=max(0,self.scenario_limits[zone]-reserve-int(zone in ("hand","battlefield"))-int(growth))
            if isinstance(value,(list,tuple)):
                value=(min(limit,max(minimum,value[0])),min(limit,max(minimum,value[1])))
            else:
                value=min(limit,max(minimum,value))
        if isinstance(value,(list,tuple)):
            return random.randint(int(value[0]),int(value[1]))
        return int(value)

    def _scenario_keys(self,card):
        names=("when_end_turn","when_start_turn","when_a_creature_die","aura","when_play_a_card","when_an_object_hert")
        signature=tuple(getattr(getattr(card,name),"__func__",getattr(card,name)) for name in names)
        if any(function is not getattr(type(card),name) for name,function in zip(names,signature)):
            return card.check_overwritten()
        room=card.player.room
        cache=getattr(room,"_scenario_hook_cache",None)
        if cache is None:
            cache=room._scenario_hook_cache={}
        if signature not in cache:
            cache[signature]=card.check_overwritten()
        return cache[signature]

    def _scenario_pool(self,owner,kind=None,basic=None,safe=False):
        from initinal_file import CARD_DICTION
        cache=getattr(self.room,"_scenario_card_pools",None)
        if cache is None:
            cache=self.room._scenario_card_pools={}
        key=(kind,basic,safe)
        if key not in cache:
            pool=[]
            for name,cls in CARD_DICTION.items():
                if name in self.room.test_cards:
                    continue
                card=cls(owner)
                if card.type.lower() not in ("land","instant","sorcery","creature") or kind is not None and card.type.lower()!=kind:
                    continue
                is_basic=card.type=="Land" and card.name in ("Plains","Island","Swamp","Mountain","Forest")
                if basic is not None and is_basic!=basic:
                    continue
                if safe and self._scenario_keys(card):
                    continue
                pool.append(cls)
            cache[key]=pool
        return cache[key]

    def scenario_cards(self,owner,zone=None,land=0,instant=0,sorcery=0,creature=0,basic=None,safe=False):
        specs={"land":land,"instant":instant,"sorcery":sorcery,"creature":creature}
        counts={kind:self.scenario_count(zone or "library",value) for kind,value in specs.items()}
        if any(value<0 for value in counts.values()):
            raise ValueError(f"Negative scenario card count: {counts}")
        if zone is not None and sum(counts.values())>self.scenario_space(owner,zone):
            raise ValueError(f"Scenario exceeds {zone} capacity: {counts}")
        cards=[]
        for kind,count in counts.items():
            if not count:
                continue
            pool=self._scenario_pool(owner,kind,basic if kind=="land" else None,safe)
            if not pool:
                raise ValueError(f"No complete scenario cards match kind={kind}, basic={basic}, safe={safe}")
            for _ in range(count):
                card=random.choice(pool)(owner)
                if zone is not None:
                    self.stage_card(card,owner,zone=zone)
                cards.append(card)
        return cards

    def scenario_random_cards(self,owner,zone,count=None,safe=True):
        count=self.scenario_count(zone,count)
        if count<0 or count>self.scenario_space(owner,zone):
            raise ValueError(f"Scenario card count {count} exceeds available {zone} slots")
        pool=self._scenario_pool(owner,"creature" if zone=="battlefield" else "land" if zone=="land_area" else None,safe=safe)
        if count and not pool:
            raise ValueError(f"No complete scenario cards available for {zone}")
        cards=[]
        for _ in range(count):
            card=random.choice(pool)(owner)
            self.stage_card(card,owner,zone=zone)
            if zone in ("battlefield","land_area"):
                self.scenario_tapped(card,random.random()<0.5)
            cards.append(card)
        return cards

    def scenario_clear(self,owner,zone):
        for card in list(getattr(owner,zone)):
            self.unstage_card(card,owner)

    def scenario_replace_cards(self,owner,zone,**counts):
        self.scenario_clear(owner,zone)
        return self.scenario_cards(owner,zone=zone,**counts)

    def scenario_finish(self,result):
        action=result["action"]
        target=None
        scope=getattr(getattr(self.card,{"Creature":"when_enter_battlefield","Land":"when_enter_landarea"}.get(self.card.type,"card_ability"),None),"select_range","") or self.card.select_range
        if action is not None and action>=32:
            sub=(action-32)%33
            if 1<=sub<=20:
                owner=self.player.opponent if sub<=10 else self.player
                zone="land_area" if scope in ("all_lands","opponent_lands","your_lands") else "battlefield"
                index=sub-1 if sub<=10 else sub-11
                if index<len(getattr(owner,zone)):
                    target=getattr(owner,zone)[index]
        defender=None
        forced=self.room.simulation_opponent_action
        if forced is not None and 12<=forced<=21 and forced-12<len(self.player.opponent.battlefield):
            defender=self.player.opponent.battlefield[forced-12]
        for side,owner in (("self",self.player),("opponent",self.player.opponent)):
            for zone in ("hand","library","graveyard","battlefield","land_area"):
                if side+"."+zone in self._scenario_locks:
                    continue
                desired=self.scenario_count(zone)
                current=len(getattr(owner,zone))-int(self.card in getattr(owner,zone))
                amount=min(max(0,desired-current),self.scenario_space(owner,zone))
                self.scenario_random_cards(owner,zone,amount)
        # Preserve exact target objects while randomizing the visible slots.
        for owner in (self.player,self.player.opponent):
            random.shuffle(owner.battlefield)
            head=owner.land_area[:10]
            random.shuffle(head)
            if owner is self.player and action is not None and 22<=action<=31:
                head.remove(self.card)
                head.insert(0,self.card)
            owner.land_area[:10]=head
        if action is not None and action>=32:
            sub=(action-32)%33
            if sub<23:
                random.shuffle(self.player.hand)
            if target is not None:
                owner=target.player
                zone="land_area" if scope in ("all_lands","opponent_lands","your_lands") else "battlefield"
                sub=(1 if owner is self.player.opponent else 11)+getattr(owner,zone).index(target)
            result["action"]=32+self.player.hand.index(self.card)*33+sub
        elif action is not None and 2<=action<=21:
            result["action"]=(2 if action<=11 else 12)+self.player.battlefield.index(self.card)
        elif action is not None and 22<=action<=31:
            result["action"]=22+self.player.land_area.index(self.card)
        if defender is not None:
            self.room.simulation_opponent_action=12+self.player.opponent.battlefield.index(defender)
        for owner in (self.player,self.player.opponent):
            present=[card for zone in self.scenario_zones for card in getattr(owner,zone)]
            present.extend(item["card"] for item in self.room.stack if item["card"].player is owner)
            for key,items in list(owner.cards_store_dict.items()):
                for card in list(items):
                    if hasattr(card,"card_id") and card not in present:
                        owner.remove_card_from_dict(key,card)
            for card in present:
                self._scenario_register(card,owner)
        result["generation"]={"level":self._scenario_level,"counts":{side:{zone:len(getattr(owner,zone)) for zone in self.scenario_zones} for side,owner in (("self",self.player),("opponent",self.player.opponent))}}
        return result

    def _scenario_register(self,card,owner):
        keys=self._scenario_keys(card)
        for key,cards in list(owner.cards_store_dict.items()):
            if card in cards and key not in keys:
                owner.remove_card_from_dict(key,card)
        for key in keys:
            owner.put_card_to_dict(key,card)

    def unstage_card(self,card,player=None):
        """Remove a setup card without gameplay events or leave-zone effects."""
        owner=player or card.player
        for zone in self.scenario_zones:
            cards=getattr(owner,zone)
            while card in cards:
                cards.remove(card)
        for key,cards in list(owner.cards_store_dict.items()):
            if card in cards:
                owner.remove_card_from_dict(key,card)
        return card

    def stage_card(self,card,player=None,zone="battlefield",index=None):
        """Place an initial entity, preserving its identity and existing target slot."""
        owner=player or card.player
        target=getattr(owner,zone)
        if card.player is not owner:
            self.unstage_card(card)
            card.player=owner
        for name in self.scenario_zones:
            if name!=zone:
                cards=getattr(owner,name)
                while card in cards:
                    cards.remove(card)
        if index is not None:
            if card in target:
                target.remove(card)
            target.insert(index,card)
        elif card not in target:
            target.append(card)
        self._scenario_register(card,owner)
        return card

    def scenario_tapped(self,card,tapped=True):
        card.flag_dict["tap"]=bool(tapped)
        return card

    def scenario_fresh_creature(self,card):
        card.flag_dict["summoning_sickness"]=True
        card.set_counter_dict("attack_counter",2 if card.get_flag("Double strike") else 1)
        return card

    def scenario_buff(self,card,buff,end_of_turn=False):
        """Initialize a real buff and its modifiers without an acquisition event."""
        card.buffs.append(buff)
        card.update_buff()
        if any(card in getattr(card.player,zone) for zone in self.scenario_zones):
            self._scenario_register(card,card.player)
        if end_of_turn:
            buff.set_end_of_turn()
        return buff

    def description_values(self):
        values = dict(self.card.effect_params, card_name=self.card.name)
        words = (
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
            "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty",
        )
        for name, value in self.card.effect_params.items():
            if type(value) is int:
                word = words[value] if 0 <= value < len(words) else str(value)
                values[name + "_word"] = word
                values[name + "_article"] = "a" if value == 1 else word
                values[name + "_article_an"] = "an" if value == 1 else word
                values[name + "_plural"] = "" if value == 1 else "s"
        return values

    def scenario_prepare(self,parameters=None):
        if not hasattr(self,"_scenario_profile"):
            self.scenario_begin(self.scenario_prepare)
        self.room.clear_environmrnt()
        for zone,counts in (parameters or {}).items():
            translated={name.removesuffix("_number"):value for name,value in counts.items()}
            self.scenario_cards(self.player,zone=zone,**translated)
            self._scenario_locks.add("self."+zone)
        self.random_life()(self.player)
        self.random_life()(self.player.opponent)
        self.room.simulation_opponent_action=None

    def scenario_creature(self, owner, power=None, health=None, flags=None, mana_cost=None, creature_type=None, zone="battlefield"):
        creature=self.room.create_scenario_creature(owner)
        if power is not None:
            creature.power = creature.actual_power = power
        if health is not None:
            creature.live = creature.actual_live = health
        if flags is not None:
            creature.flag_dict.clear()
            creature.flag_dict.update(flags)
            if "_saved_keywords" in type(creature).__dict__:
                type(creature)._saved_keywords = dict(flags)
            creature.content = ", ".join(name for name, enabled in flags.items() if enabled)
        if mana_cost is not None:
            creature.mana_cost = mana_cost
        if creature_type is not None:
            creature.type_creature = creature.type_card = creature_type
        return self.stage_card(creature,owner,zone=zone) if zone is not None else creature

    def scenario_cast(self,preferred_subactions=(0,),extra_cost=None,in_stack=False,provide_mana=True):
        if provide_mana:
            cost=dict(self.card.calculate_cost())
            for color,amount in (extra_cost or {}).items():
                cost[color]=cost.get(color,0)+amount
            available=self.room.get_cost_total(self.player)
            for color in ("U","W","B","R","G"):
                deficit=max(0,cost.get(color,0)-available.get(color,0))
                self.player.mana[color]+=deficit
            available=self.room.get_cost_total(self.player)
            remaining=sum(available.values())-sum(cost.get(color,0) for color in ("U","W","B","R","G"))
            self.player.mana["colorless"]+=max(0,cost.get("colorless",0)-remaining)
        cast=self.room.simulate_play_in_stack if in_stack else self.room.simulate_play
        return cast(self.card,preferred_subactions=preferred_subactions,populate_targets=False)

    def scenario_skip(self):
        return {"card": self.card, "type": 0, "action": None}

    def scenario_combat(self, defending, opponent_dies, self_dies, margin=0, enemy_flags=None):
        self.scenario_prepare()
        attack, health = self.card.state
        if health <= 0 or (opponent_dies and attack <= margin) or (not self_dies and health <= margin):
            return self.scenario_skip()
        enemy_attack = health + margin if self_dies else health - 1 - margin
        enemy_health = attack - margin if opponent_dies else attack + 1 + margin
        flags = dict(enemy_flags or {})
        if not defending and self.card.get_flag("flying"):
            flags["reach"] = True
        self.scenario_creature(self.player.opponent, enemy_attack, enemy_health, flags)
        if defending:
            result = self.room.simulate_creature_defend(self.card)
        else:
            result = self.room.simulate_creature_attack(self.card)
            self.scenario_block()
        self.stage_card(self.card)
        return result

    def scenario_unblocked(self, with_creature=False):
        self.scenario_prepare()
        if with_creature:
            self.scenario_creature(self.player.opponent, flags={})
        result = self.room.simulate_creature_attack(self.card)
        self.stage_card(self.card)
        self.room.simulation_opponent_action = 1
        return result

    def scenario_stack(self, target_type="instant", own_target=False, cost=2, power=3, lower_count=0):
        target_type = target_type.lower()
        self.room.env_stack_cards(self.player, self.card if target_type == "land" else None, preferred_types=(target_type,))
        top = self.room.stack[-1]
        zones = {"Creature": "battlefield", "Land": "land_area"}
        for item in self.room.stack[:-1]:
            card = item["card"]
            zone = zones.get(card.type, "graveyard")
            self.unstage_card(card)
        self.room.stack[:] = [top]
        target = top["card"]
        if own_target:
            zone = zones.get(target.type, "graveyard")
            self.unstage_card(target)
            target = target.copy_for_player(self.player)
            self.stage_card(target,self.player,zone=zone)
            top["card"] = target
            top["message"] = random.choice(self.room.all_play_card_messages(self.player))
        target.mana_cost = str(max(0, cost))
        if target.type == "Creature":
            target.power = target.actual_power = power
            target.live = target.actual_live = 4
        for _ in range(lower_count):
            lower = target.copy_for_player(target.player)
            zone = zones.get(lower.type, "graveyard")
            self.stage_card(lower,zone=zone)
            self.room.stack.insert(0, dict(top, card=lower))
        return target

    def scenario_option(self, option):
        selection_step = self.card.selection_step

        async def choose_option(player=None, opponent=None, selection_random=False):
            send_selection_cards = player.send_selection_cards

            async def select_cards(cards, *args, **kwargs):
                if cards and all(getattr(card, "selection_index", None) in (1, 2) for card in cards):
                    return next(card for card in cards if card.selection_index == option)
                return await send_selection_cards(cards, *args, **kwargs)

            player.send_selection_cards = select_cards
            try:
                return await selection_step(player, opponent, selection_random)
            finally:
                player.send_selection_cards = send_selection_cards

        self.card.selection_step = choose_option

    def scenario_block(self):
        defender = self.player.opponent.battlefield[0]
        if self.card.get_flag("flying") and not (defender.get_flag("flying") or defender.get_flag("reach")):
            defender.flag_dict["reach"] = True
            defender.extra_content.append("Reach.")
            if "_saved_keywords" in type(defender).__dict__:
                type(defender)._saved_keywords["reach"] = True
        self.room.simulation_opponent_action = 12
