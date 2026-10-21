const topics = [
    ['life', 'Life', 'Reduce the opponent’s life to zero.'],
    ['decks', 'Decks', 'Draw from your deck; the enemy hand stays hidden.'],
    ['hand', 'Your hand', 'Tap a card to spread your hand.', 'tap'],
    ['lands', 'Play a land', 'Drag a land forward to build your mana.', 'drag'],
    ['mana', 'Mana', 'Tap an unused land for mana.', 'tap'],
    ['cast', 'Play a card', 'Drag a glowing card forward. Then respond or pass.', 'drag'],
    ['attack', 'Attack', 'Drag a ready creature forward to open Bullet Time.', 'drag'],
    ['block', 'Defend now', 'Drag a blocker forward. Queue more before passing.', 'drag'],
    ['targets', 'Choose a target', 'Click a highlighted target or card.', 'tap'],
    ['bullet', 'Bullet Time', 'Respond or block. Click the left ring to pass.', 'tap'],
    ['turn', 'Your turn', 'Finish your actions, then click the right ring.', 'tap'],
    ['controls', 'Action log', 'Hover the left strip to review recent actions.']
].map(([key, title, cue, gesture]) => ({key, title, cue, gesture, group: 'Match hints'}));

export async function mountBattleGuide(client, {practice} = {}) {
    const style = document.createElement('link');
    style.rel = 'stylesheet'; style.href = new URL('./battle-guide.css', import.meta.url).href;
    await new Promise((resolve, reject) => { style.onload = resolve; style.onerror = reject; document.head.append(style); });
    return new BattleGuide(client, practice);
}

// Demo only observes client state. Offline scenes provide their own controller.
class BattleGuide {
    constructor(client, practice) {
        this.client = client; this.practice = practice; this.lessons = practice?.lessons || topics;
        this.events = new AbortController(); this.focused = document.hasFocus(); this.motion = matchMedia('(prefers-reduced-motion: reduce)');
        this.index = 0; this.enabled = true; this.seen = new Set(); this.nextAt = 0;
        try {
            if (!practice) { const saved = JSON.parse(sessionStorage.getItem('magic-context-guide-v2')); this.enabled = saved?.enabled !== false; this.seen = new Set(saved?.seen || []); }
        } catch (_) {}
        this.root = document.createElement('section'); this.root.id = 'battle-guide';
        this.root.setAttribute('aria-label', 'Battle guide'); this.root.dataset.practice = String(Boolean(practice));
        this.root.innerHTML = `
            <button class="bg-launch" type="button" aria-controls="bg-panel"></button>
            <button class="bg-menu-toggle" type="button" aria-expanded="false" aria-controls="bg-lessons">Lessons ☰</button>
            <nav id="bg-lessons" class="bg-lessons" aria-label="Choose a lesson" hidden></nav>
            <div class="bg-scene" hidden aria-hidden="true"><svg class="bg-lines" xmlns="http://www.w3.org/2000/svg">
                <defs><marker id="bg-arrowhead" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M1 1 6 4 1 7" fill="none" stroke="#c6dfbf" stroke-width="1.7"/></marker></defs>
                <g class="bg-outlines"/><path class="bg-arrow" marker-end="url(#bg-arrowhead)"/><path class="bg-drag-route"/><g class="bg-flows"/>
            </svg><div class="bg-labels"></div><div class="bg-gesture"><i class="bg-ghost"></i><svg viewBox="0 0 32 40"><path d="M11 22V5a3 3 0 0 1 6 0v12l2-1 4 2 4 3v10l-4 7H12L3 26q-1-5 4-4l4 5"/></svg></div></div>
            <article id="bg-panel" class="bg-panel" aria-labelledby="bg-title" hidden>
                <header><h2 id="bg-title"></h2><button class="bg-close" type="button" aria-label="Dismiss hint">×</button></header>
                <p class="bg-status" role="status" aria-live="polite"></p>
                <footer><button class="bg-replay" type="button" aria-label="Replay lesson">↺</button><a class="bg-exit" href="/">Lobby ↗</a><button class="bg-next" type="button">Continue →</button></footer>
            </article>`;
        document.body.append(this.root); this.$ = selector => this.root.querySelector(selector);
        this.panel = this.$('.bg-panel'); this.scene = this.$('.bg-scene');
        let group;
        this.lessons.forEach((lesson, index) => {
            if (lesson.key === 'finish') return;
            if (group !== lesson.group) { group = lesson.group; const label = document.createElement('p'); label.textContent = group; this.$('.bg-lessons').append(label); }
            const button = document.createElement('button'); button.type = 'button'; button.dataset.lesson = index;
            button.textContent = `${String(index + 1).padStart(2, '0')}  ${lesson.title}`;
            this.on(button, 'click', () => { practice ? practice.goTo(index) : this.setStep(index, true); this.toggleMenu(false); });
            this.$('.bg-lessons').append(button);
        });
        this.on(this.$('.bg-menu-toggle'), 'click', () => this.toggleMenu(this.$('.bg-lessons').hidden));
        this.on(this.$('.bg-launch'), 'click', () => {
            if (practice) this.open ? this.hide() : this.show();
            else { this.enabled = !this.enabled; this.enabled ? this.show() : this.hide(); this.save(); }
            this.updateSwitch(); this.schedule();
        });
        this.on(this.$('.bg-close'), 'click', () => { this.hide(); this.nextAt = performance.now() + 6000; });
        this.on(this.$('.bg-replay'), 'click', () => practice?.goTo(this.index));
        this.on(this.$('.bg-next'), 'click', () => practice?.advance());
        this.$('.bg-replay').hidden = this.$('.bg-exit').hidden = this.$('.bg-next').hidden = !practice;
        this.on(document, 'keydown', event => { if (event.key === 'Escape') { this.toggleMenu(false); this.hide(); } });
        const pause = event => {
            if (event?.type === 'blur') this.focused = false;
            if (event?.type === 'focus') this.focused = true;
            const stopped = !this.focused || document.hidden;
            this.root.classList.toggle('bg-paused', stopped);
            const svg = this.$('.bg-lines'); stopped || this.motion.matches ? svg.pauseAnimations() : svg.unpauseAnimations();
            clearTimeout(this.timer); if (!stopped) { this.update(); this.schedule(); }
        };
        for (const event of ['blur', 'focus', 'pageshow']) this.on(window, event, pause);
        this.on(document, 'visibilitychange', pause); this.on(this.motion, 'change', pause);
        this.on(window, 'pagehide', event => { clearTimeout(this.timer); if (!event.persisted) { this.events.abort(); this.root.remove(); } });
        this.updateSwitch();
        if (practice) practice.attach(this);
        else this.update();
        pause();
    }
    on(element, event, handler) { element.addEventListener(event, handler, {signal: this.events.signal}); }
    save() { if (!this.practice) try { sessionStorage.setItem('magic-context-guide-v2', JSON.stringify({enabled: this.enabled, seen: [...this.seen]})); } catch (_) {} }
    updateSwitch() { this.$('.bg-launch').textContent = this.practice ? this.open ? 'Guide −' : 'Guide +' : this.enabled ? 'Hints on' : 'Hints off'; this.$('.bg-launch').setAttribute('aria-expanded', String(this.practice ? this.open : this.enabled)); }
    toggleMenu(open) { this.$('.bg-lessons').hidden = !open; this.$('.bg-menu-toggle').setAttribute('aria-expanded', String(open)); }
    show() { this.enabled = true; this.open = Boolean(this.practice); this.panel.hidden = this.scene.hidden = !this.open; this.root.classList.remove('bg-hidden'); this.updateSwitch(); this.update(); this.schedule(); }
    hide() { this.open = false; this.panel.hidden = this.scene.hidden = true; this.root.classList.add('bg-hidden'); this.updateSwitch(); }
    setStep(index, manual = false) {
        this.index = Math.max(0, Math.min(this.lessons.length - 1, index)); this.manual = manual;
        this.until = performance.now() + 9000; this.panel.guidePlacement = null;
        if (this.practice?.stackView) this.practice.stackView.guidePlacement = null;
        this.enabled = this.open = true; this.panel.hidden = this.scene.hidden = false;
        this.root.classList.remove('bg-hidden');
        this.root.dataset.step = this.lessons[this.index].key;
        this.$('#bg-title').textContent = this.lessons[this.index].title;
        for (const button of this.$('.bg-lessons').querySelectorAll('button')) button.setAttribute('aria-current', String(Number(button.dataset.lesson) === this.index));
        this.updateSwitch(); if (manual) { this.seen.add(this.lessons[this.index].key); this.save(); }
        this.update(); this.schedule();
    }
    schedule() {
        clearTimeout(this.timer);
        if (this.enabled && this.focused && !document.hidden) this.timer = setTimeout(() => { this.update(); this.schedule(); }, 150);
    }
    observe() {
        const c = this.client, t = c.table, p = c.self_player;
        const ring = t.timmer_bullet, color = ring.changing_color ? ring.changing_store[6] : ring.current_color;
        this.bulletActive = color[0] === ring.rgb_green[0];
        const enemy = t.opponent_battlefield.find(card => card.mode === 'attack');
        const land = p.cards.some(card => card.type === 'Land'), spell = p.cards.some(card => card.type !== 'Land' && card.check_weather_can_used());
        this.conditions = {
            targets: c.selectionPage.in_selection, block: this.bulletActive && enemy && !enemy.flag_dict?.unblockable && t.self_battlefield.some(card => !card.activated && (!enemy.card.flying || card.card.flying || card.flag_dict?.reach)),
            bullet: this.bulletActive, lands: p.my_turn && !this.bulletActive && land,
            mana: p.my_turn && !this.bulletActive && t.self_landfield.some(card => !card.activated),
            cast: spell && (p.my_turn || this.bulletActive), attack: p.my_turn && !this.bulletActive && t.self_battlefield.some(card => !card.activated && (!card.flag_dict?.summoning_sickness || card.flag_dict?.haste) && (card.counter_dict?.attack_counter ?? 1) > 0),
            hand: p.cards.length > 0 && p.cards_mode !== 'focus', turn: p.my_turn && !this.bulletActive,
            life: p.cards.length > 0, decks: p.cards.length > 0, controls: c.action_bar.actions.length > 0
        };
        const priority = ['targets', 'block', 'bullet', 'lands', 'mana', 'cast', 'attack', 'hand', 'turn', 'life', 'decks', 'controls'];
        const now = performance.now(), current = this.lessons[this.index].key;
        if (this.open && ((!this.manual && !this.conditions[current]) || now > this.until || c.win_lose.finish)) { this.hide(); this.manual = false; this.nextAt = now + 4500; }
        const key = priority.find(key => this.conditions[key] && !this.seen.has(key));
        if (!key || c.win_lose.finish) return;
        const urgent = ['targets', 'block', 'bullet'].includes(key);
        if (this.open && (!urgent || priority.indexOf(key) >= priority.indexOf(current))) return;
        if (!urgent && now < this.nextAt) return;
        this.index = this.lessons.findIndex(lesson => lesson.key === key); this.manual = false; this.until = now + 8000;
        this.seen.add(key); this.save(); this.open = true; this.panel.hidden = this.scene.hidden = false; this.root.classList.remove('bg-hidden'); this.panel.guidePlacement = null;
    }
    // The same projected corners drive the existing hit tests, in both renderers.
    rect(points, label) {
        if (!points?.length || points.some(p => !Number.isFinite(p[0]) || !Number.isFinite(p[1]))) return null;
        const canvas = this.client.main_canvas, bounds = canvas.getBoundingClientRect();
        // Stone surfaces retain camera-space vertices; cards/rings expose pixels.
        const camera = this.client.table.camera;
        points = points.map(p => p.length === 3 ? [canvas.width / 2 + camera.similar_tri_2(p[0], p[2]), canvas.height / 2 + camera.similar_tri_2(p[1], p[2])] : p);
        const xs = points.map(p => bounds.left + p[0] * bounds.width / canvas.width);
        const ys = points.map(p => bounds.top + p[1] * bounds.height / canvas.height);
        const x = Math.max(6, Math.min(...xs) - 6), y = Math.max(6, Math.min(...ys) - 6);
        const right = Math.min(innerWidth - 6, Math.max(...xs) + 6), bottom = Math.min(innerHeight - 6, Math.max(...ys) + 6);
        return right - x > 8 && bottom - y > 8 ? {x, y, w: right - x, h: bottom - y, label} : null;
    }
    item(object, label) { return this.rect(object?.position_in_screen || object?.get_position_in_screen?.(), label); }
    area(x, y, w, h, label) { return this.rect([[x, y], [x + w, y + h]], label); }
    field(own, label) {
        const points = this.client.table.table_graph.get_position_in_screen();
        if (!points?.length) return null;
        // Table corners are top-left, bottom-left, bottom-right, top-right.
        const at = (u, v) => points[0].map((_, i) => (points[0][i] * (1 - u) + points[3][i] * u) * (1 - v) + (points[1][i] * (1 - u) + points[2][i] * u) * v);
        const a = own ? .52 : .22, b = own ? .77 : .48;
        return this.rect([at(.2, a), at(.8, a), at(.8, b), at(.2, b)], label);
    }
    targets(key) {
        const c = this.client, t = c.table, hand = c.self_player.cards;
        const land = hand.find(card => card.type === 'Land');
        const spells = hand.filter(card => card.type !== 'Land');
        const spell = spells.find(card => card.check_weather_can_used()) || spells[0];
        const creature = this.practice?.focusCreature || t.self_battlefield.find(card => !card.activated) || t.self_battlefield[0];
        const manaLand = t.self_landfield.find(card => !card.activated) || t.self_landfield[0];
        const enemy = t.opponent_battlefield.find(card => card.mode === 'attack');
        let target, rects = [], destination;
        const union = (cards, label) => this.rect(cards.flatMap(card => card.position_in_screen || []), label);
        switch (key) {
            case 'life': rects = [this.item(c.self_player.player_life_ring, 'Your life'), this.item(c.oppo_player.player_life_ring, 'Opponent’s life')]; break;
            case 'field': rects = [this.field(true, 'Your creatures'), this.field(false, 'Enemy creatures')]; break;
            case 'decks': rects = [this.item(t.deck_self_graph, 'Your deck'), this.item(t.deck_oppo_graph, 'Opponent’s deck'), union(c.oppo_player.cards, 'Opponent’s hand')]; break;
            case 'hand': target = this.item(hand.at(-1), 'Your hand'); rects = [union(hand, 'Your hand')]; break;
            case 'anatomy': target = this.item(spells.find(card => card.type === 'Creature') || hand.at(-1), 'Read this card'); rects = [target]; break;
            case 'lands': target = this.item(land, 'Land in hand'); rects = [target || union(t.self_landfield, 'Your land row')]; break;
            case 'mana': target = this.item(manaLand, 'Land ability'); rects = [target, this.area(c.main_canvas.width - 220, 2, 210, 96, 'Stored mana')]; break;
            case 'cast': target = this.item(spell, 'Creature or spell'); rects = [target]; break;
            case 'attack': case 'block': target = this.item(creature, 'Your creature'); rects = [target || this.field(true, 'Your creature row')]; break;
            case 'targets': target = this.item(t.opponent_battlefield[0], 'Example target'); rects = [target]; break;
            case 'bullet': target = this.item(t.timmer_bullet, 'Bullet Time · pass response'); rects = [target]; break;
            case 'turn': target = this.item(t.timmer_turn, 'Turn timer · end turn'); rects = [target]; break;
            case 'controls': {
                const b = c.buttons.auto_pass;
                rects = [this.area(b.x, b.y, b.width, b.height, 'Auto Pass'), this.area(0, 0, c.action_bar.canvas.width - 70, c.main_canvas.height, 'Action log')]; break;
            }
        }
        let selection = c.selectionPage.in_selection;
        if (selection) {
            const s = c.selectionPage;
            rects = s.selection_mode === 'cards' ? s.selection_list.map(card => this.item(card, 'Choose a card'))
                : [...t.self_battlefield, ...t.opponent_battlefield, ...t.self_landfield, ...t.opponent_landfield].filter(card => card.select_flag).map(card => this.item(card, 'Eligible target'));
            for (const player of [c.self_player, c.oppo_player]) if (s.selection_mode !== 'cards' && player.select_flag) rects.push(this.item(player.player_life_ring, 'Eligible player'));
            target = rects.find(Boolean);
        }
        let gesture = selection ? 'tap' : this.practice?.gesture || this.lessons[this.index].gesture;
        if (!selection && gesture === 'drag' && target) {
            const bounds = c.main_canvas.getBoundingClientRect();
            const field = this.field(false, '');
            const limit = ['lands', 'cast'].includes(key) ? .42 : .28;
            destination = {x: field ? field.x + field.w / 2 : bounds.left + bounds.width * .5,
                y: Math.min(field ? field.y + field.h / 2 : bounds.top + bounds.height * limit, bounds.top + bounds.height * limit)};
            if (key === 'block' && enemy) {
                const r = this.item(enemy, 'Attacking creature');
                if (r) destination = {x: r.x + r.w / 2, y: Math.min(r.y + r.h / 2, bounds.top + bounds.height * .35)};
            }
            const x = (destination.x - bounds.left) * c.main_canvas.width / bounds.width;
            const y = (destination.y - bounds.top) * c.main_canvas.height / bounds.height;
            rects.push(this.area(x - c.main_canvas.width * .09, y - c.main_canvas.height * .04, c.main_canvas.width * .18, c.main_canvas.height * .08, 'Drag here, then release'));
        }
        if (c.card_hold[0] || (!selection && ((['lands', 'cast', 'attack', 'turn'].includes(key) && !c.self_player.my_turn && !(key === 'cast' && spell?.type === 'Instant' && this.bulletActive)) || (key === 'block' && !enemy) || (key === 'bullet' && !this.bulletActive)))) gesture = null;
        return {rects: rects.filter(Boolean).slice(0, 8), target, destination, gesture, selection, land, spell, creature, enemy, manaLand};
    }
    update() {
        if (!this.enabled) return;
        if (!this.practice) this.observe(); else this.bulletActive = this.practice.bulletActive;
        if (!this.open) return;
        const lesson = this.lessons[this.index], state = this.targets(this.practice?.targetKey || lesson.key);
        this.root.classList.toggle('bg-dragging', Boolean(this.client.card_hold[0]));
        if (this.practice?.resolving) {
            const entry = this.practice.activeEntry, target = entry?.target;
            const present = target?.player_life_ring || target?.Life > 0 && [...this.client.table.self_battlefield, ...this.client.table.opponent_battlefield].includes(target);
            state.rects = present && !['fizzled', 'skipped'].includes(entry?.state) ? [this.item(target?.player_life_ring || target, '')].filter(Boolean) : [];
        }
        const context = this.practice?.context;
        if (context) {
            const target = context.target, preview = context.card && this.client.show_2d.showed_card;
            state.rects = [
                context.phase !== 'play' && context.phase !== 'prepare' && this.item(target?.player_life_ring || target, target === this.client.self_player ? 'Your life' : target?.card?.name),
                this.item(preview || context.source?.player_life_ring || context.source, preview ? 'Enemy card' : 'Enemy action')
            ].filter(Boolean);
            state.gesture = state.destination = null;
        }
        this.root.dataset.step = lesson.key;
        const title = context ? context.card ? 'Enemy plays' : 'Enemy combat' : state.selection ? 'Choose' : lesson.title;
        if (this.$('#bg-title').textContent !== title) this.$('#bg-title').textContent = title;
        const status = this.practice?.status || lesson.cue;
        if (this.$('.bg-status').textContent !== status) this.$('.bg-status').textContent = status;
        this.$('.bg-next').hidden = !this.practice?.canAdvance;
        this.$('.bg-next').textContent = lesson.key === 'finish' ? 'Lobby →' : 'Continue →';
        const clearance = state.destination ? [{x: state.destination.x - 32, y: state.destination.y - 32, w: 64, h: 64}] : [];
        this.drawHighlights(state.rects); this.placePanel([...state.rects, ...clearance]); this.drawArrow(context || this.practice?.resolving ? null : state.rects[0]);
        const gesture = this.$('.bg-gesture'), from = state.target;
        gesture.hidden = !state.gesture || !from || this.practice?.busy || this.practice?.resolving;
        this.$('.bg-drag-route').setAttribute('d', '');
        if (!gesture.hidden) {
            const x = from.x + from.w / 2, y = from.y + Math.min(from.h / 3, 30), to = state.destination || {x, y};
            gesture.dataset.kind = state.gesture; gesture.style.cssText = `left:${x}px;top:${y}px;--dx:${to.x - x}px;--dy:${to.y - y}px`;
            if (state.gesture === 'drag') this.$('.bg-drag-route').setAttribute('d', `M${x},${y} L${to.x},${to.y}`);
        }
        this.drawFlow();
    }
    drawHighlights(rects) {
        const outlines = this.$('.bg-outlines'), labels = this.$('.bg-labels');
        while (outlines.children.length < rects.length) { outlines.append(document.createElementNS('http://www.w3.org/2000/svg', 'rect')); labels.append(document.createElement('span')); }
        [...outlines.children].forEach((outline, i) => {
            const r = rects[i], label = labels.children[i]; outline.style.display = label.style.display = r ? '' : 'none'; if (!r) return;
            for (const [key, value] of Object.entries({x: r.x, y: r.y, width: r.w, height: r.h, rx: 7})) outline.setAttribute(key, value);
            label.textContent = i === 0 ? r.label : ''; label.style.cssText = `left:${r.x}px;top:${Math.max(4, r.y - 22)}px`;
        });
    }
    placePanel(rects) {
        const c = this.client, t = c.table;
        const objects = c.selectionPage.in_selection ? [] : [...c.self_player.cards, ...c.oppo_player.cards, ...t.self_battlefield, ...t.opponent_battlefield, ...t.self_landfield, ...t.opponent_landfield, t.timmer_bullet, t.timmer_turn, c.self_player.player_life_ring, c.oppo_player.player_life_ring];
        const avoid = [...rects, ...objects.map(card => this.item(card, '')).filter(Boolean)];
        for (const element of [this.panel, this.practice?.stackView].filter(element => element && !element.hidden)) {
            const w = element.offsetWidth, h = element.offsetHeight, maxX = Math.max(12, innerWidth - w - 12), maxY = Math.max(62, innerHeight - h - 12);
            const xs = [...new Set([112, maxX, 12, ...avoid.flatMap(r => [r.x + r.w + 14, r.x - w - 14])].map(x => Math.min(maxX, Math.max(12, x))))];
            const ys = [70, maxY, ...avoid.flatMap(r => [r.y + r.h + 12, r.y - h - 12])].map(y => Math.min(maxY, Math.max(62, y)));
            const score = ({x, y}) => avoid.reduce((sum, r, i) => sum + (i < rects.length ? 5 : 2) * Math.max(0, Math.min(x + w + 8, r.x + r.w) - Math.max(x - 8, r.x)) * Math.max(0, Math.min(y + h + 8, r.y + r.h) - Math.max(y - 8, r.y)), 0);
            let best = {x: xs[0], y: ys[0]}, value = score(best);
            for (const x of xs) for (const y of ys) { const next = score({x, y}); if (next < value) { best = {x, y}; value = next; } }
            if (!element.guidePlacement || element.guidePlacement.x > maxX || element.guidePlacement.y > maxY || score(element.guidePlacement) > value + 700) element.guidePlacement = best;
            element.style.left = `${element.guidePlacement.x}px`; element.style.top = `${element.guidePlacement.y}px`;
            avoid.push({x: element.guidePlacement.x, y: element.guidePlacement.y, w, h});
        }
    }
    drawArrow(target) {
        let path = '';
        if (target) {
            const p = this.panel.getBoundingClientRect(), tx = target.x + target.w / 2, ty = target.y + target.h / 2;
            const sx = tx < p.left ? p.left : tx > p.right ? p.right : Math.max(p.left + 12, Math.min(p.right - 12, tx));
            const sy = ty < p.top ? p.top : ty > p.bottom ? p.bottom : p.top + p.height / 2;
            const ex = Math.max(target.x, Math.min(target.x + target.w, sx)), ey = Math.max(target.y, Math.min(target.y + target.h, sy));
            if (Math.hypot(ex - sx, ey - sy) > 18) path = `M${sx},${sy} Q${(sx + ex) / 2},${sy} ${ex},${ey}`;
        }
        this.$('.bg-arrow').setAttribute('d', path);
    }
    flowPoint(object) {
        let r;
        if (typeof object === 'string') r = this.root.querySelector(`[data-entry="${object}"]`)?.getBoundingClientRect();
        else r = this.item(object?.player_life_ring || object, '');
        return r ? {x: r.x + (r.w || r.width) / 2, y: r.y + (r.h || r.height) / 2} : null;
    }
    drawFlow() {
        const group = this.$('.bg-flows'), links = this.practice?.flowLinks || [];
        const ns = 'http://www.w3.org/2000/svg';
        while (group.children.length < links.length) {
            const g = document.createElementNS(ns, 'g'); g.append(document.createElementNS(ns, 'path'));
            for (let i = 0; i < 3; i++) {
                const dot = document.createElementNS(ns, 'circle'), motion = document.createElementNS(ns, 'animateMotion');
                dot.setAttribute('r', i ? '2' : '3'); motion.setAttribute('dur', '1.8s'); motion.setAttribute('begin', `${-i * .6}s`); motion.setAttribute('repeatCount', 'indefinite'); dot.append(motion); g.append(dot);
            }
            group.append(g);
        }
        [...group.children].forEach((g, i) => {
            const a = this.flowPoint(links[i]?.from), b = this.flowPoint(links[i]?.to); g.style.display = a && b ? '' : 'none'; if (!a || !b) return;
            const d = `M${a.x},${a.y} Q${(a.x + b.x) / 2 + 35},${Math.min(a.y, b.y) - 28} ${b.x},${b.y}`;
            g.style.color = links[i].color || '#a4d4bb'; g.firstChild.setAttribute('d', d);
            for (const motion of g.querySelectorAll('animateMotion')) if (motion.getAttribute('path') !== d) motion.setAttribute('path', d);
        });
        if (this.motion.matches || document.hidden || !this.focused) this.$('.bg-lines').pauseAnimations();
    }
}
