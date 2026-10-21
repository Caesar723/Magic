// The static tutorial replaces only network transport; table controls stay native.
class Tutorial_Client extends Game_Client {
    init() {
        this.socket_main = {readyState: 1, send: message => queueMicrotask(() => this.training?.command(message))};
        this.socket_select = {readyState: 1, send: message => queueMicrotask(() => this.training?.select(message))};
    }
    constructor() {
        super(); this.music.start_flag = false; this.training = new TutorialCampaign(this);
        const ready = Promise.all(Object.values(TutorialCampaign.cards).map(card => loadImage(card.image)))
            .then(() => import('/webpages/gaming_page/battle-guide.js'))
            .then(({mountBattleGuide}) => mountBattleGuide(this, {practice: this.training}));
        window.PageTransition?.wait(ready);
    }
    update() { super.update(); this.training?.update(); }
    draw() { super.draw(); if (this.training?.refreshGuide) { this.training.refreshGuide = false; this.training.guide?.update(); } }
}
class Tutorial_Play_Card extends Play_Cards {
    set_animate() { this.remaining = this.duration ?? .85; this.show_2D.show_a_card(this.object_hold); }
    finished() { return this.remaining <= 0; }
}
class Tutorial_Point_To extends Point_To {
    finished() { return this.missile?.disappear === true; }
}
class TutorialCampaign {
    static cards = {
        forest: {"name": "Forest", "type": "Land", "color": "green", "rarity": "Uncommon", "cost": "", "text": "", "faceType": "Land", "image": "/cards/land/Forest/image.jpg", "mana": 4, "reach": false, "flying": false, "trample": false},
        mountain: {"name": "Mountain", "type": "Land", "color": "red", "rarity": "Uncommon", "cost": "", "text": "", "faceType": "Land", "image": "/cards/land/Mountain/image.jpg", "mana": 3, "reach": false, "flying": false, "trample": false},
        island: {"name": "Island", "type": "Land", "color": "blue", "rarity": "Uncommon", "cost": "", "text": "", "faceType": "Land", "image": "/cards/land/Island/image.jpg", "mana": 0, "reach": false, "flying": false, "trample": false},
        ranger: {"name": "Thornwood Ranger", "type": "Creature", "color": "green", "rarity": "Common", "cost": "1G", "text": "Reach. When Thornwood Ranger enters the battlefield, another target creature you control gets +1/+0 until end of turn.", "faceType": "Human Warrior", "image": "/cards/creature/Thornwood Ranger/image.jpg", "power": 2, "life": 1, "reach": true, "flying": false, "trample": false},
        sentinel: {"name": "Thornwood Sentinel", "type": "Creature", "color": "green", "rarity": "Common", "cost": "2G", "text": "Reach (This creature can block creatures with flying)", "faceType": "Elemental Creature", "image": "/cards/creature/Thornwood Sentinel/image.jpg", "power": 2, "life": 3, "reach": true, "flying": false, "trample": false},
        sprite: {"name": "Tidal Sprite", "type": "Creature", "color": "blue", "rarity": "Common", "cost": "1U", "text": "Flying (This creature can't be blocked except by creatures with flying or reach.)", "faceType": "Merfolk Creature", "image": "/cards/creature/Tidal Sprite/image.jpg", "power": 1, "life": 1, "reach": false, "flying": true, "trample": false},
        channeler: {"name": "Essence Channeler", "type": "Creature", "color": "green", "rarity": "Rare", "cost": "1G", "text": "Whenever you cast a creature spell, you may add G to your mana pool.", "faceType": "Human Shaman", "image": "/cards/creature/Essence Channeler/image.jpg", "power": 2, "life": 2, "reach": false, "flying": false, "trample": false},
        wayfinder: {"name": "Merfolk Wayfinder", "type": "Creature", "color": "blue", "rarity": "Common", "cost": "2U", "text": "Whenever Merfolk Wayfinder enters the battlefield, you may scry 1. (Look at the top card of your library. You may put that card on the bottom of your library.)", "faceType": "Merfolk Creature", "image": "/cards/creature/Merfolk Wayfinder/image.jpg", "power": 1, "life": 1, "reach": false, "flying": false, "trample": false},
        sage: {"name": "Sage of the Ancient Grove", "type": "Creature", "color": "green", "rarity": "Rare", "cost": "2GG", "text": "Reach, When Sage of the Ancient Grove enters the battlefield, you may search your library for a basic land card, put it onto the battlefield tapped, then shuffle your library.", "faceType": "Treefolk Creature - Treefolk", "image": "/cards/creature/Sage of the Ancient Grove/image.jpg", "power": 4, "life": 4, "reach": true, "flying": false, "trample": false},
        guardian: {"name": "Thornwood Guardian", "type": "Creature", "color": "green", "rarity": "Rare", "cost": "3GG", "text": "Reach, Trample (This creature can block creatures with flying, and it can deal excess combat damage to the player or planeswalker it's attacking.)", "faceType": "Elemental Creature - Elemental", "image": "/cards/creature/Thornwood Guardian/image.jpg", "power": 5, "life": 4, "reach": true, "flying": false, "trample": true},
        blast: {"name": "Fiery Blast", "type": "Instant", "color": "red", "rarity": "Common", "cost": "1R", "text": "Fiery Blast deals 2 damage to any target.", "faceType": "Instant", "image": "/cards/Instant/Fiery Blast/image.jpg", "reach": false, "flying": false, "trample": false},
        growth: {"name": "Overgrowth Surge", "type": "Instant", "color": "green", "rarity": "Uncommon", "cost": "1G", "text": "Target creature gets +3/+3 until end of turn. If that creature is a Treefolk, it also gains trample until end of turn.", "faceType": "Instant", "image": "/cards/Instant/Overgrowth Surge/image.jpg", "reach": false, "flying": false, "trample": false, "boost": 3},
        counter: {"name": "Ephemeral Response", "type": "Instant", "color": "blue", "rarity": "Common", "cost": "1U", "text": "Counter target spell unless its controller pays 2. If it is countered this way, scry 1.", "faceType": "Instant", "image": "/cards/Instant/Ephemeral Response/image.jpg", "reach": false, "flying": false, "trample": false},
        rush: {"name": "Wild Growth Rush", "type": "Instant", "color": "green", "rarity": "Rare", "cost": "1GG", "text": "Target creature gains +2/+2 and trample until end of turn. Then, if you control a Forest, you may search your library for a basic land card and put it onto the battlefield tapped.", "faceType": "Instant", "image": "/cards/Instant/Wild Growth Rush/image.jpg", "reach": false, "flying": false, "trample": false, "boost": 2},
        storm: {"name": "Storm Bringer", "type": "Creature", "color": "blue", "rarity": "Rare", "cost": "4UU", "text": "Flying. When Storm Bringer enters the battlefield, it deals 3 damage to each opponent and you gain 3 life.", "faceType": "Creature - Elemental", "image": "/cards/creature/Storm Bringer/image.jpg", "power": 5, "life": 5, "flying": true},
        bolt: {"name": "Ephemeral Bolt", "type": "Instant", "color": "red", "rarity": "Uncommon", "cost": "1R", "text": "Ephemeral Bolt deals 1 damage to target creature or player. If a creature dealt damage this way dies this turn, you may draw a card.", "faceType": "Instant", "image": "/cards/Instant/Ephemeral Bolt/image.jpg", "damage": 1},
        practiceSurge: {"name": "Practice Surge", "type": "Instant", "color": "green", "rarity": "Common", "cost": "1G", "text": "Tutorial only. Target creature gets +8/+8 until end of turn. No effect if the target has left the battlefield.", "faceType": "Tutorial Instant", "image": "/cards/Instant/Overgrowth Surge/image.jpg", "boost": 8}
    };
    constructor(client) {
        this.c = client; this.id = 5000; this.index = 0;
        const scene = (key, title, cue, setup = {}, group = 'Basics', mode = key) => ({key, title, cue, setup, group, mode, gesture: ['lands', 'cast', 'attack', 'block'].includes(key) ? 'drag' : 'tap'});
        this.lessons = [
            scene('life', 'The table', 'Your life below. Enemy life above. Reach zero to win.', {hand: ['forest', 'sentinel', 'blast'], own: ['sentinel'], enemy: ['ranger'], lands: ['forest', 'mountain']}),
            scene('decks', 'Decks & hands', 'Your deck is face down. Only your hand is visible.', {hand: ['forest', 'sentinel', 'blast']}),
            scene('hand', 'Inspect a card', 'Tap your hand to spread the cards.', {hand: ['forest', 'sentinel', 'blast']}),
            scene('lands', 'Play a land', 'Drag Forest forward, then pass Bullet Time.', {hand: ['forest']}),
            scene('mana', 'Generate mana', 'Tap Forest and Mountain.', {lands: ['forest', 'mountain']}),
            scene('cast', 'Play a creature', 'Play Sentinel. Its entry waits in Bullet Time.', {hand: ['sentinel'], lands: ['forest', 'mountain', 'island'], mana: [1, 0, 0, 1, 1]}),
            scene('attack', 'Attack & pass', 'Drag Sentinel forward, then pass the left ring.', {own: ['sentinel'], enemyLife: 6}),
            scene('block', 'Queue a defender', 'Drag Sentinel to defend, then pass.', {own: ['sentinel'], enemy: ['sprite'], incoming: true}),
            scene('cast', 'Aim a spell', 'Cast Fiery Blast at the 2/1 Ranger.', {hand: ['blast'], enemy: ['ranger', 'sentinel'], lands: ['forest', 'mountain']}, 'Basics', 'target'),
            scene('targets', 'Card choices', 'Choose Forest.', {hand: ['sentinel']}, 'Basics', 'choice'),
            scene('bullet', 'Bullet Time', 'Click the left ring. Both passes release the stack.', {waiting: 'blast', enemyLands: ['mountain', 'forest']}, 'Basics'),
            scene('turn', 'End your turn', 'Click the right ring to refresh your turn.', {own: ['sentinel'], lands: ['forest', 'mountain'], tapped: true}),
            scene('controls', 'Log & Auto Pass', 'Open the left log. Switch Auto Pass on, then off.', {hand: ['forest'], lands: ['forest']}),
            scene('cast', 'Buff, fight, expire', 'Buff your Ranger. Pass, attack, then end the turn.', {hand: ['growth'], own: ['ranger'], enemy: ['sentinel'], lands: ['forest', 'mountain']}, 'Advanced', 'buff'),
            scene('cast', 'Respond to damage', 'Buff your Ranger before the waiting Blast resolves.', {hand: ['growth'], own: ['ranger'], lands: ['forest', 'mountain'], waiting: 'blast', enemyLands: ['mountain', 'forest']}, 'Advanced', 'response'),
            scene('cast', 'Counter the top spell', 'Cast Ephemeral Response. It counters the top spell.', {hand: ['counter'], enemy: ['ranger'], lands: ['island', 'forest'], waiting: 'growth', enemyLands: ['forest', 'mountain']}, 'Advanced', 'counter'),
            scene('block', 'Block → buff → counter', 'Defend the 1/1 with your 2/2.', {hand: ['counter'], own: ['channeler'], enemy: ['wayfinder'], lands: ['island', 'forest'], enemyLands: ['forest', 'forest', 'mountain'], incoming: true}, 'Advanced', 'chain'),
            scene('block', 'Multiple defenders', 'Queue both 2/2 defenders before passing.', {own: ['channeler', 'channeler'], enemy: ['sage'], incoming: true}, 'Advanced', 'multiple'),
            scene('block', 'Flying & Reach', 'The attacker flies. Choose your creature with Reach.', {own: ['channeler', 'sentinel'], enemy: ['sprite'], incoming: true}, 'Advanced', 'flying'),
            scene('attack', 'Trample overflow', 'Attack. Watch excess damage reach the player.', {own: ['guardian'], enemy: ['channeler']}, 'Advanced', 'trample'),
            scene('block', 'When a target dies', 'Defend the 5/5 with your 1/1.', {hand: ['practiceSurge'], own: ['sprite'], enemy: ['storm'], lands: ['forest', 'mountain'], enemyLands: ['mountain', 'forest'], incoming: true}, 'Advanced', 'fizzle'),
            scene('attack', 'Win a practice duel', 'Defeat the opponent. Spells and combat use Bullet Time.', {hand: ['forest', 'blast', 'sentinel'], own: ['sentinel'], enemy: ['ranger'], lands: ['forest', 'mountain', 'forest'], ownLife: 8, enemyLife: 4}, 'Practice', 'final'),
            scene('finish', 'Victory', 'Opponent defeated.', {}, 'Practice', 'win')
        ];
    }
    get lesson() { return this.lessons[this.index]; }
    get finalDuel() { return this.lesson.mode === 'final'; }
    attach(guide) {
        this.guide = guide; this.stackView = document.createElement('section'); this.stackView.className = 'bg-stack';
        this.stackView.setAttribute('aria-label', 'Stack playback');
        this.stackView.innerHTML = `<header><strong>Action stack</strong><span class="bg-stack-phase"></span></header>
            <div class="bg-stack-body"><div class="bg-stack-slots" aria-label="Waiting slots"></div><div class="bg-stack-out"><span>Resolve →</span><div class="bg-resolve-slot"></div></div></div>
            <div class="bg-combat"></div><p class="bg-stack-result" role="status"></p>
            <footer><span>Last in · first out</span><button class="bg-playback" type="button"></button><button class="bg-resolve" type="button">Resolve ▶</button></footer>`;
        guide.root.append(this.stackView);
        guide.on(this.stackView.querySelector('.bg-playback'), 'click', () => { this.stepMode = !this.stepMode; if (!this.stepMode) this.continueStack(); this.renderStack(); });
        guide.on(this.stackView.querySelector('.bg-resolve'), 'click', () => this.continueStack()); this.goTo(0);
    }
    get focusCreature() {
        return this.c.table.self_battlefield.find(card => !card.activated && !this.stack.some(entry => entry.kind === 'defense' && entry.target === card)
            && (!this.pendingCombat?.attacker.card.flying || card.card.flying || TutorialCampaign.cards[card.card.trainingKey].reach));
    }
    get targetKey() {
        if (this.failed) return 'life';
        if (this.choiceMode) return 'targets';
        if (this.pendingCombat?.player === this.c.oppo_player) {
            if (this.lesson.mode === 'chain' && this.enemyBuffPlayed && !this.counterPlayed) return 'cast';
            if (this.lesson.mode === 'fizzle' && this.stack.some(entry => entry.kind === 'defense') && !this.responsePlayed) return 'cast';
            return this.stack.some(entry => entry.kind === 'defense') && (this.lesson.mode !== 'multiple' || this.stack.filter(entry => entry.kind === 'defense').length === 2) ? 'bullet' : 'block';
        }
        if (this.bulletActive) return this.lesson.mode === 'response' && !this.responsePlayed || this.lesson.mode === 'counter' && !this.counterPlayed ? 'cast' : 'bullet';
        if (this.lesson.mode === 'buff' && this.buffApplied) return this.combatDone ? 'turn' : 'attack';
        if (this.finalDuel) return this.focusCreature && !this.focusCreature.card.trainingSick ? 'attack' : this.c.self_player.cards.some(card => card.type !== 'Land' && card.check_weather_can_used()) ? 'cast' : 'turn';
        return this.lesson.key;
    }
    get gesture() { return ['cast', 'attack', 'block', 'lands'].includes(this.targetKey) ? 'drag' : 'tap'; }
    get canAdvance() { return !this.busy && !this.resolving && (this.index < 2 || this.lesson.mode === 'win' || this.fizzleDone); }
    advance() {
        if (!this.canAdvance) return;
        if (this.lesson.mode === 'win') { (window.PageTransition?.navigate || (path => location.assign(path)))('/'); return; }
        this.goTo(this.index + 1);
    }
    card(key, player = this.c.self_player) {
        const d = TutorialCampaign.cards[key];
        const face = this.c.card_frame.generate_card(d.color, d.name, d.faceType, d.rarity, d.text, d.image);
        const args = [4, 5.62, [0, 0, 0], 1, face];
        const card = d.type === 'Land' ? new Land_Hand(...args, d.name, this.id++, player, [0, 0, 0, 0, 0].map((_, i) => Number(i === d.mana)))
            : d.type === 'Creature' ? new Creature_Hand(...args, d.cost, d.life, d.power, d.life, d.power, d.name, this.id++, player)
            : new Instant_Hand(...args, d.cost, d.name, this.id++, player);
        card.trainingKey = key; card.flying = d.flying; card.trainingTrample = d.trample; return card;
    }
    goTo(index) {
        if (!Number.isInteger(index) || index < 0 || index >= this.lessons.length) return;
        if (index === this.lessons.length - 1) {
            if (!this.won) return;
            this.index = index; this.busy = this.resolving = false; this.work = null; this.hint('Opponent defeated.'); this.guide.setStep(index); return;
        }
        const c = this.c, t = c.table; c.message_processor.end_select(); c.card_hold = [undefined, false, false];
        this.index = index; this.work = this.stepTask = null; this.busy = this.resolving = this.failed = this.won = false;
        this.stepMode = this.lesson.group === 'Advanced'; this.stackNodes = new Map(); this.slotCount = 3;
        this.stackView.querySelector('.bg-stack-slots').replaceChildren(); this.stackView.querySelector('.bg-resolve-slot').replaceChildren();
        this.pendingSpell = this.pendingCombat = this.activeEntry = this.choiceMode = this.combatLink = this.context = null;
        this.stack = []; this.history = []; this.buffs = []; this.entryId = 0; this.landPlayed = this.buffApplied = this.combatDone = this.responsePlayed = this.counterPlayed = this.enemyBuffPlayed = false;
        this.logSeen = this.passOn = this.passOff = this.fizzleDone = false; this.stackResult = ''; this.library = Array.from({length: 15}, (_, i) => ['forest', 'sentinel', 'blast'][i % 3]);
        this.mana = this.lesson.setup.mana?.slice() || [0, 0, 0, 0, 0]; this.bulletActive = false;
        c.action_bar.actions_processing = []; c.action_bar.actions_finsihed = true; c.action_bar.mode = c.action_bar.card_mode = 'hide'; c.buttons.auto_pass.end();
        t.special_effects.missiles = []; t.special_effects.particles = []; c.show_2d.unshow_a_card(); c.show_2d.delete_mouse_card(); c.win_lose.finish = false; c.self_player.cards_mode = 'ignore';
        const s = this.lesson.setup;
        c.message_processor.initinal_all((s.hand || []).map(key => this.card(key)), Array.from({length: 4}, () => new Card_Hand_Oppo(4, 5.62, [0, 0, 0], .7, this.id++, c.oppo_player)),
            (s.own || []).map(key => this.card(key)), (s.enemy || []).map(key => this.card(key, c.oppo_player)), (s.lands || []).map(key => this.card(key)), (s.enemyLands || []).map(key => this.card(key, c.oppo_player)), [], this.mana,
            120, 0, s.ownLife || 20, 20, s.enemyLife || 20, 20, this.library.length, 15, s.incoming || s.waiting ? 0 : 1, 0);
        for (const [ring, value] of [[c.self_player.player_life_ring, s.ownLife || 20], [c.oppo_player.player_life_ring, s.enemyLife || 20]]) { ring.life = value; ring.moving = false; }
        for (const ring of [t.timmer_turn, t.timmer_bullet]) { ring.moving = false; ring.time = ring === t.timmer_turn ? 120 : 0; }
        t.timmer_bullet.change_yellow();
        if (s.tapped || s.mana) for (const card of [...t.self_landfield, ...(s.tapped ? t.self_battlefield : [])]) { card.activated = true; card.angle_z = Math.PI / 2; }
        this.hint(this.lesson.cue); this.renderStack();
        if (s.incoming) this.declareAttack(t.opponent_battlefield[0], c.oppo_player);
        if (s.waiting) {
            this.hint('Enemy turn.');
            this.enqueue([], () => this.presentEnemySpell(s.waiting, s.waiting === 'growth' ? t.opponent_battlefield[0] : t.self_battlefield[0] || c.self_player, this.lesson.cue), .65);
        }
        if (this.lesson.mode === 'choice') { this.choiceMode = 'choice'; this.choices = ['forest', 'sentinel', 'blast'].map(key => this.card(key)); this.choose('cards', this.choices); }
        if (this.lesson.mode === 'controls') c.action_bar.actions = [new Activate_Ability(t.self_landfield[0], c.self_player)];
        Game_Client.prototype.update.call(c); this.guide.setStep(index); this.refreshGuide = true;
    }
    hint(message) { this.status = message; this.refreshGuide = true; }
    enqueue(actions, after = null, delay = .35) {
        for (const action of actions) this.c.action_bar.actions_cache.push(action, false);
        if (after) { this.busy = true; this.work = {time: 0, after, delay}; }
    }
    update() {
        const c = this.c, dt = Math.min(.05, TIME_INTERVAL / 120);
        for (const action of c.action_bar.actions_processing) if (action instanceof Tutorial_Play_Card && action.remaining > 0) { action.remaining -= dt; if (action.remaining <= 0 && !action.keepPreview) c.show_2d.unshow_a_card(); }
        if (this.work) {
            this.work.time += dt;
            if (this.work.time > this.work.delay && c.action_bar.actions_finsihed && !c.action_bar.actions_cache.length) { const after = this.work.after; this.work = null; this.busy = false; after(); }
        }
        if (this.busy || this.resolving) return;
        if (this.finalDuel && this.bulletActive && c.buttons.auto_pass.flag) this.resolveWindow();
        if (this.lesson.mode === 'hand' && c.self_player.cards_mode === 'focus') this.complete('Hand opened.');
        if (this.lesson.mode === 'controls') { this.logSeen ||= c.action_bar.mode === 'show'; if (this.logSeen && this.passOff) this.complete('Controls ready.'); }
    }
    complete(message) { this.hint(message); this.enqueue([], () => this.goTo(this.index + 1), 1.2); }
    command(message) {
        const [, action, value] = message.split('|'), mode = this.lesson.mode;
        if (this.busy || this.resolving || this.failed) return;
        const allowed = {lands: ['play_card', 'end_bullet'], mana: ['activate_ability'], cast: ['play_card', 'end_bullet'], attack: ['select_attacker', 'end_bullet'], block: ['select_defender', 'end_bullet'],
            target: ['play_card', 'end_bullet'], bullet: ['end_bullet'], turn: ['end_step'], controls: ['auto_passing'], buff: ['play_card', 'activate_ability', 'select_attacker', 'end_bullet', 'end_step'],
            response: ['play_card', 'activate_ability', 'end_bullet'], counter: ['play_card', 'activate_ability', 'end_bullet'], chain: ['play_card', 'activate_ability', 'select_defender', 'end_bullet'],
            multiple: ['select_defender', 'end_bullet'], flying: ['select_defender', 'end_bullet'], trample: ['select_attacker', 'end_bullet'], fizzle: ['select_defender', 'play_card', 'activate_ability', 'end_bullet'], final: ['play_card', 'activate_ability', 'select_attacker', 'select_defender', 'end_bullet', 'end_step', 'auto_passing']};
        if (!allowed[mode]?.includes(action)) return;
        if (action === 'play_card') this.play(Number(value));
        if (action === 'activate_ability') this.tapLand(Number(value.split(';')[1]));
        if (action === 'select_attacker') this.attack(Number(value));
        if (action === 'select_defender') this.block(Number(value));
        if (action === 'end_bullet') this.resolveWindow();
        if (action === 'end_step') this.endTurn();
        if (action === 'auto_passing') { this.c.message_processor.auto_passing(value); if (value === 'true') this.passOn = true; else if (this.passOn) this.passOff = true; }
    }
    tapLand(index) {
        const c = this.c, land = c.table.self_landfield[index]; if (!land || land.activated) return;
        land.activated = true; this.mana = this.mana.map((n, i) => n + land.manas[i]); c.self_player.mana_bar.set_mana(this.mana);
        this.enqueue([new Activate_Ability(land, c.self_player)], () => { if (this.lesson.mode === 'mana' && c.table.self_landfield.every(card => card.activated)) this.complete('Mana ready.'); });
    }
    pay(card) {
        const pool = this.mana.slice(), lands = this.c.table.self_landfield.filter(card => !card.activated), used = [];
        const cost = TutorialCampaign.cards[card.trainingKey].cost;
        const take = color => {
            const i = color ?? pool.findIndex(n => n > 0); if (i >= 0 && pool[i] > 0) { pool[i]--; return true; }
            const j = lands.findIndex(land => color === undefined || land.manas[color]); if (j < 0) return false; used.push(lands.splice(j, 1)[0]); return true;
        };
        for (const symbol of cost.replace(/\d/g, '')) if (!take({U: 0, W: 1, B: 2, R: 3, G: 4}[symbol])) return false;
        for (let i = 0; i < Number(cost.match(/^\d+/)?.[0] || 0); i++) if (!take()) return false;
        this.refund = {mana: this.mana.slice(), lands: used}; this.mana = pool; this.c.self_player.mana_bar.set_mana(pool);
        for (const land of used) { land.activated = true; this.enqueue([new Activate_Ability(land, this.c.self_player)]); } return true;
    }
    play(index) {
        const c = this.c, card = c.self_player.cards[index]; if (!card || this.pendingSpell) return;
        if (this.lesson.mode === 'fizzle' && !this.stack.some(entry => entry.kind === 'defense')) { this.hint('Defend with your 1/1 first.'); return; }
        if ((!c.self_player.my_turn || this.bulletActive) && card.type !== 'Instant') { this.hint('Use an Instant during Bullet Time.'); return; }
        if (card.trainingKey === 'counter' && !this.canCounter(this.stack.at(-1))) { this.hint('Counter the top spell, not a land or defender.'); return; }
        if (card.type === 'Land' && this.landPlayed) { this.hint('One land per turn.'); return; }
        if (card.type !== 'Land' && !this.pay(card)) { this.hint('Not enough mana.'); return; }
        if (card.type === 'Instant' && card.trainingKey !== 'counter') { const buff = TutorialCampaign.cards[card.trainingKey].boost; this.pendingSpell = card; this.choose(buff ? 'your_creatures' : 'opponent_roles'); this.hint(buff ? 'Choose your creature.' : 'Choose the enemy Ranger or player.'); return; }
        c.self_player.cards.splice(index, 1);
        const animation = new Tutorial_Play_Card(card, c.self_player, c.show_2d);
        if (card.type === 'Land' || card.type === 'Creature') {
            this.landPlayed ||= card.type === 'Land'; card.trainingSick = card.type === 'Creature';
            this.enqueue([animation, new Summon(card, c.self_player)], () => { this.push('entry', card, c.self_player); this.openWindow(); this.hint('Card entered. Pass Bullet Time to resolve its entry.'); });
        } else {
            this.counterPlayed = true; this.enqueue([animation], () => { this.push('spell', card, c.self_player); this.openWindow(); this.hint('Counter is on top. Pass the left ring.'); });
        }
    }
    choose(type, cards = []) { this.c.message_processor.select(type, cards); this.c.selectionPage.update(); this.refreshGuide = true; }
    select(message) {
        const c = this.c, [, kind, field, value] = message.split('|');
        if (this.choiceMode === 'scry') {
            if (kind !== 'cancel' && kind !== 'cards') return;
            c.message_processor.end_select(); if (kind === 'cancel') this.library.push(this.library.shift());
            this.choiceMode = null; this.hint(kind === 'cancel' ? 'Card put below. Defense resolves next.' : 'Card kept. Defense resolves next.');
            this.activeEntry.state = 'resolved'; this.activeEntry = null; this.renderStack(); this.drain(); return;
        }
        if (this.choiceMode === 'choice') {
            if (kind !== 'cards' || field !== '0') { c.message_processor.end_select(); this.choose('cards', this.choices); return; }
            this.choiceMode = null; this.enqueue([new Gain_Card(c.self_player, c.self_player, this.choices[0])], () => this.complete('Forest added.')); return;
        }
        if (!this.pendingSpell) return;
        if (kind === 'cancel') {
            c.message_processor.end_select(); this.pendingSpell = null; this.mana = this.refund.mana; c.self_player.mana_bar.set_mana(this.mana);
            for (const land of this.refund.lands) land.activated = false;
            this.enqueue(this.refund.lands.map(land => new Reset_Ability(land, c.self_player))); this.hint('Cancelled. Mana returned.'); return;
        }
        if (kind !== 'field') return;
        const growth = Boolean(TutorialCampaign.cards[this.pendingSpell.trainingKey].boost);
        const target = growth ? field === 'self_battlefield' && c.table.self_battlefield[Number(value)] : field === 'oppo' ? c.oppo_player : field === 'opponent_battlefield' && c.table.opponent_battlefield[Number(value)];
        if (!target || this.lesson.mode === 'target' && target.card?.trainingKey !== 'ranger') { this.hint('Choose the 2/1 Ranger.'); this.choose(growth ? 'your_creatures' : 'opponent_creatures'); return; }
        const card = this.pendingSpell; this.pendingSpell = null; c.self_player.cards.splice(c.self_player.cards.indexOf(card), 1); this.responsePlayed = true;
        this.enqueue([new Tutorial_Play_Card(card, c.self_player, c.show_2d)], () => {
            this.push('spell', card, c.self_player, target); this.openWindow();
            if (this.lesson.mode === 'fizzle') this.presentEnemySpell('bolt', target, '1 damage is on top. Pass the left ring.');
            else this.hint('Spell queued. Pass the left ring.');
        });
    }
    push(kind, card, player, target = null) {
        const entry = {id: `q${++this.entryId}`, kind, card, player, target, state: 'waiting', slot: this.stack.length};
        this.stack.push(entry); this.history.push(entry); this.slotCount = Math.max(this.slotCount, this.stack.length); this.renderStack(); return entry;
    }
    openWindow() {
        this.bulletActive = true; this.resolving = false; this.c.message_processor.start_bullet(); const ring = this.c.table.timmer_bullet; ring.time = 10; ring.moving = false;
        this.renderStack();
    }
    canCounter(entry) { return this.bulletActive && entry && entry.player === this.c.oppo_player && entry.kind !== 'defense' && entry.card.type !== 'Land' && !(entry.card.type === 'Creature' && this.pendingCombat); }
    resolveWindow() {
        if (!this.bulletActive) return;
        if (this.lesson.mode === 'response' && !this.responsePlayed || this.lesson.mode === 'counter' && !this.counterPlayed) { this.hint(this.lesson.cue); return; }
        if (this.lesson.mode === 'multiple' && this.stack.filter(entry => entry.kind === 'defense').length < 2) { this.hint('Queue both defenders before passing.'); return; }
        if (this.lesson.mode === 'fizzle' && !this.responsePlayed) { this.hint('Defend, then cast +8/+8 before passing.'); return; }
        this.bulletActive = false; this.resolving = true; this.c.message_processor.end_bullet(); this.hint('Both passed. Resolving the full stack.'); this.drain();
    }
    drain() {
        // Room.end_bullet_time drains the whole stack after both players pass.
        const entry = this.stack.pop();
        if (!entry) {
            if (this.pendingCombat && !this.pendingCombat.blocked && this.pendingCombat.attacker.Life > 0) { this.fight(this.pendingCombat.attacker, this.pendingCombat.player, this.pendingCombat.player.oppo, () => this.finishWindow()); return; }
            this.finishWindow(); return;
        }
        this.activeEntry = entry; entry.state = 'lifting'; this.renderStack();
        // Playback pauses do not reopen Bullet Time or require another pass.
        this.enqueue([], () => {
            entry.state = 'ready'; this.stepTask = () => this.resolveEntry(entry); this.renderStack();
            if (!this.stepMode) this.continueStack();
        }, .75);
    }
    continueStack() {
        if (!this.stepTask) return;
        const next = this.stepTask; this.stepTask = null; next();
    }
    resolveEntry(entry) {
        const c = this.c; entry.state = 'resolving'; this.renderStack();
        const done = () => { if (!['fizzled', 'skipped'].includes(entry.state)) entry.state = 'resolved'; this.activeEntry = null; this.renderStack(); this.drain(); };
        if (entry.kind === 'defense') {
            const combat = this.pendingCombat;
            if (!combat || combat.attacker.Life <= 0 || entry.target.Life <= 0) {
                entry.state = 'skipped'; this.stackResult = 'Defender gone · no combat with this creature.'; this.hint('No defender remains. The attack continues.'); this.renderStack(); this.enqueue([], done, 1.4); return;
            }
            combat.blocked = true; this.hint('Defender resolves. Creatures exchange damage.'); this.fight(combat.attacker, combat.player, entry.target, done); return;
        }
        if (entry.card.trainingKey === 'counter') {
            const top = this.stack.at(-1);
            if (top && top.player !== entry.player && top.kind !== 'defense' && top.card.type !== 'Land') {
                this.stack.pop(); top.state = 'countered'; entry.counterTarget = top; this.stackResult = 'Top spell cancelled. No buff applied.';
                this.renderStack(); this.enqueue([], () => { top.ejected = true; this.choiceMode = 'scry'; this.choices = [this.card(this.library[0])]; this.choose('cards', this.choices); this.renderStack(); this.hint('Scry 1: click to keep; empty table puts it below.'); }, 1.1);
            } else done();
            return;
        }
        if (entry.kind === 'entry') { this.enqueue([], done); return; }
        const key = entry.card.trainingKey, target = entry.target;
        if (!(target instanceof Player) && (target?.Life <= 0 || ![...c.table.self_battlefield, ...c.table.opponent_battlefield].includes(target))) {
            entry.state = 'fizzled'; this.stackResult = 'Target left play · no effect'; this.hint('Target gone. The buff cannot apply.'); this.renderStack(); this.enqueue([], done, 1.6); return;
        }
        if (TutorialCampaign.cards[key].boost) {
            const amount = TutorialCampaign.cards[key].boost, state = [target.Damage + amount, target.Life + amount];
            const buff = new Buff(entry.card.name, TutorialCampaign.cards[key].image, `+${amount}/+${amount}`, this.id++);
            const record = {target, source: entry.card, buff, power: amount, remaining: amount}; this.buffs.push(record);
            if (key === 'rush') target.card.trainingTrample = true;
            this.buffApplied = true; this.stackResult = `${target.Damage}/${target.Life} → ${state[0]}/${state[1]}`;
            const actions = [new Attack_To_Object(entry.player, entry.player, target, 'rgba(155, 211, 173, .9)', 'Missile_Hit', state), new Add_Buff(entry.card, entry.player, target, '', 'None', state, buff)];
            if (key === 'rush' && c.table.opponent_landfield.length) {
                const land = this.card('forest', entry.player); actions.push(new Summon(land, entry.player));
                this.enqueue(actions, () => { this.enqueue([new Activate_Ability(land, entry.player)], done); });
            } else this.enqueue(actions, done);
        } else {
            const damage = TutorialCampaign.cards[key].damage ?? 2, state = target instanceof Player ? [Math.max(0, target.player_life_ring.life - damage)] : [target.Damage, target.Life - damage];
            if (!(target instanceof Player)) this.consumeBuff(target, damage);
            this.stackResult = `${entry.card.name} · ${damage} damage`;
            this.enqueue([new Attack_To_Object(entry.player, entry.player, target, 'rgba(183, 128, 104, .9)', 'Missile_Hit', state)], () => this.removeDead(() => {
                if (key === 'bolt') { this.c.table.deck_oppo_graph.number_of_cards--; this.enqueue([new Gain_Card(entry.player, entry.player, new Card_Hand_Oppo(4, 5.62, [0, 0, 0], .7, this.id++, entry.player))], done); }
                else done();
            }));
        }
    }
    declareAttack(card, player) {
        // Room.select_attacker keeps combat pending; defenders enter room.stack.
        const ready = () => { this.pendingCombat = {attacker: card, player, blocked: false}; this.openWindow(); };
        if (player === this.c.oppo_player) {
            this.context = {source: card, target: player.oppo, phase: 'prepare'};
            this.hint(`Enemy attacks with ${card.card.name} (${card.Damage}/${card.Life}).`);
            this.enqueue([], () => this.enqueue([new Creature_Prepare_Attack(card, player)], () => {
                this.context.phase = 'target'; this.hint(`${card.card.name} → your life.`);
                this.enqueue([new Tutorial_Point_To(card, player, player.oppo)], () => {
                    this.context = null; ready(); this.hint(this.finalDuel ? 'Enemy attacks. Defend or pass.' : this.lesson.cue);
                }, .9);
            }, .6), .65);
        } else { this.enqueue([new Creature_Prepare_Attack(card, player)]); ready(); }
    }
    presentEnemySpell(key, target, cue) {
        const c = this.c, player = c.oppo_player, card = this.card(key, player), preview = new Tutorial_Play_Card(card, player, c.show_2d);
        preview.duration = 2; preview.keepPreview = true; player.cards.pop();
        this.context = {source: player, card, target, phase: 'play'}; this.hint(`Enemy plays ${card.name}.`);
        this.enqueue(c.table.opponent_landfield.filter(land => !land.activated).map(land => new Activate_Ability(land, player)).concat(preview), () => {
            this.context.phase = 'target';
            this.hint(`${card.name} → ${target === c.self_player ? 'your life' : `${target.player === 'self' ? 'your' : 'enemy'} ${target.card.name}`}.`);
            this.enqueue([new Tutorial_Point_To(player, player, target)], () => {
                card.position_in_screen = c.show_2d.showed_card?.position_in_screen?.map(point => point.slice());
                c.show_2d.unshow_a_card(); this.context.phase = 'queue'; this.push('spell', card, player, target);
                this.enqueue([], () => { this.context = null; this.openWindow(); this.hint(cue); }, .65);
            }, .9);
        });
    }
    attack(index) {
        const c = this.c, card = c.table.self_battlefield[index];
        if (!card || !c.self_player.my_turn || this.bulletActive || card.activated || card.card.trainingSick) return;
        if (this.lesson.mode === 'buff' && !this.buffApplied) { this.hint('Resolve the buff first.'); return; }
        this.declareAttack(card, c.self_player); const defender = c.table.opponent_battlefield.find(card => !card.activated);
        if (defender) {
            this.context = {source: defender, target: card, phase: 'target'}; this.hint(`Enemy defends with ${defender.card.name}.`);
            this.enqueue([new Tutorial_Point_To(defender, c.oppo_player, card), new Creature_Prepare_Defense(defender, c.oppo_player, card)], () => {
                this.push('defense', defender.card, c.oppo_player, defender);
                this.enqueue([], () => { this.context = null; this.hint('Enemy defender queued. Pass Bullet Time.'); }, .65);
            });
        } else this.hint('Attack waits. Pass the left ring.');
    }
    block(index) {
        const c = this.c, card = c.table.self_battlefield[index], combat = this.pendingCombat;
        if (!combat || combat.player !== c.oppo_player || !card || card.activated || this.stack.some(entry => entry.kind === 'defense' && entry.target === card)) return;
        if (combat.attacker.card.flying && !card.card.flying && !TutorialCampaign.cards[card.card.trainingKey].reach) { this.hint('Flying needs a blocker with Reach or Flying.'); return; }
        this.push('defense', card.card, c.self_player, card); this.enqueue([new Creature_Prepare_Defense(card, c.self_player, combat.attacker)]); this.openWindow();
        if (this.lesson.mode === 'chain' && !this.enemyBuffPlayed) {
            this.enemyBuffPlayed = true; this.hint('Enemy responds.');
            this.enqueue([], () => this.presentEnemySpell('rush', combat.attacker, 'Enemy +2/+2 queued. Cast your counter.'));
        } else this.hint(this.lesson.mode === 'fizzle' ? 'Cast +8/+8 on your defending 1/1.' : this.lesson.mode === 'multiple' && this.stack.filter(entry => entry.kind === 'defense').length < 2 ? 'Queue the other defender too.' : 'Defense queued. Pass the left ring.');
    }
    consumeBuff(card, damage) { for (const buff of this.buffs.slice().reverse()) if (buff.target === card) { const absorbed = Math.min(damage, buff.remaining); buff.remaining -= absorbed; damage -= absorbed; } }
    fight(attacker, player, defender, after) {
        const state = defender instanceof Player ? [Math.max(0, defender.player_life_ring.life - attacker.Damage)] : [defender.Damage, defender.Life - attacker.Damage];
        const own = [attacker.Damage, attacker.Life - (defender instanceof Player ? 0 : defender.Damage)];
        const overflow = !(defender instanceof Player) && attacker.card.trainingTrample ? Math.max(0, -state[1]) : 0;
        if (!(defender instanceof Player)) { this.consumeBuff(attacker, defender.Damage); this.consumeBuff(defender, attacker.Damage); defender.activated = true; }
        this.combatDone = true; this.combatLink = {from: attacker, to: defender, color: '#cf9680'};
        this.stackResult = defender instanceof Player ? `${attacker.Damage} damage → ${defender.name}` : `${attacker.Damage}/${attacker.Life} vs ${defender.Damage}/${defender.Life} → ${Math.max(0, own[1])} / ${Math.max(0, state[1])} life`;
        this.renderStack();
        this.enqueue([new Creature_Start_Attack(attacker, player, defender, own, state)], () => {
            const finish = () => this.removeDead(after);
            if (overflow) { this.stackResult = `Trample · ${overflow} damage reaches the player`; this.renderStack(); this.enqueue([new Attack_To_Object(attacker.card, player, player.oppo, 'rgba(190, 140, 113, .9)', 'Missile_Hit', [Math.max(0, player.oppo.player_life_ring.life - overflow)])], finish); }
            else finish();
        });
    }
    removeDead(after) { const c = this.c; this.enqueue([...c.table.self_battlefield, ...c.table.opponent_battlefield].filter(card => card.Life <= 0).map(card => new Die(card, card.player === 'self' ? c.self_player : c.oppo_player)), after); }
    finishWindow() {
        const c = this.c, combat = this.pendingCombat;
        const finish = () => {
            this.pendingCombat = this.activeEntry = this.combatLink = null; this.resolving = false; this.renderStack();
            if (this.finalDuel) {
                if (c.oppo_player.player_life_ring.life <= 0) { this.won = true; this.complete('Opponent defeated.'); }
                else if (c.self_player.player_life_ring.life <= 0) { this.failed = true; this.hint('Defeated. Replay this lesson.'); }
                else if (!c.self_player.my_turn) this.beginTurn(); else this.hint('Your move.');
            } else if (this.lesson.mode === 'buff') this.hint(this.combatDone ? 'End your turn to remove the temporary buff.' : 'Buff resolved. Attack with your Ranger.');
            else if (this.lesson.mode === 'fizzle') { this.fizzleDone = true; this.hint('1/1 destroyed. +8/+8 had no target. The attack dealt 5.'); }
            else if (this.lesson.mode === 'chain' && !this.counterPlayed) { this.failed = true; this.hint('Replay: counter the buff before passing.'); }
            else this.complete('Resolved.');
        };
        if (combat?.attacker.Life > 0) this.enqueue([new Activate_Ability(combat.attacker, combat.player)], finish);
        else finish();
    }
    endTurn() {
        const c = this.c;
        if (!c.self_player.my_turn || this.bulletActive || this.pendingCombat || this.pendingSpell) return;
        if (this.lesson.mode === 'buff' && !this.combatDone) { this.hint('Attack with your strengthened Ranger first.'); return; }
        const actions = [];
        for (const buff of this.buffs.filter(buff => buff.target.player === 'self' && buff.target.Life > 0)) actions.push(new Lose_Buff(buff.source, c.self_player, buff.target, [buff.target.Damage - buff.power, buff.target.Life - buff.remaining], buff.buff));
        this.buffs = this.buffs.filter(buff => buff.target.player !== 'self');
        actions.push(new Turn(c.oppo_player, c.oppo_player));
        this.enqueue(actions, () => {
            if (this.lesson.mode === 'buff') { this.stackResult = 'Temporary buff expired · Ranger 2/1'; this.renderStack(); this.complete('Buff expired.'); }
            else if (this.finalDuel && c.table.opponent_battlefield.length) this.declareAttack(c.table.opponent_battlefield[0], c.oppo_player);
            else this.beginTurn();
        });
    }
    beginTurn() {
        const c = this.c; this.landPlayed = false; this.mana = [0, 0, 0, 0, 0]; c.self_player.mana_bar.set_mana(this.mana);
        const actions = [new Turn(c.self_player, c.self_player)];
        for (const card of [...c.table.self_landfield, ...c.table.self_battlefield]) { card.card.trainingSick = false; card.mode = 'none'; actions.push(new Reset_Ability(card, c.self_player)); }
        if (this.library.length) actions.push(new Gain_Card(c.self_player, c.self_player, this.card(this.library.shift())));
        this.enqueue(actions, () => this.lesson.mode === 'turn' ? this.complete('New turn ready.') : this.hint('Your turn.'));
    }
    renderStack() {
        this.refreshGuide = true; if (!this.stackView) return;
        const view = this.stackView, find = selector => view.querySelector(selector);
        const text = (tag, value) => Object.assign(document.createElement(tag), {textContent: value});
        view.hidden = !this.stack.length && !this.activeEntry && !this.pendingCombat && !this.stackResult;
        view.classList.toggle('bg-choosing', Boolean(this.choiceMode));
        view.dataset.phase = this.bulletActive ? 'respond' : this.resolving ? 'playback' : 'done';
        find('.bg-stack-phase').textContent = this.bulletActive ? 'Respond / pass' : this.stepTask ? 'Playback · ready' : this.activeEntry?.state === 'lifting' ? 'Taking out ↑' : this.resolving ? 'Playback · resolving' : 'Complete';
        find('.bg-stack-result').textContent = this.stackResult;
        find('.bg-playback').textContent = this.stepMode ? 'Play all »' : 'Step view';
        find('.bg-playback').setAttribute('aria-pressed', String(this.stepMode));
        find('.bg-resolve').hidden = !this.stepTask;
        const slots = find('.bg-stack-slots'), out = find('.bg-resolve-slot');
        while (slots.children.length < this.slotCount) {
            const slot = document.createElement('div'); slot.className = 'bg-stack-slot'; slot.dataset.slot = slots.children.length;
            slot.append(text('span', String(slots.children.length + 1).padStart(2, '0'))); slots.append(slot);
        }
        for (const slot of slots.children) { slot.dataset.top = String(Number(slot.dataset.slot) === this.stack.at(-1)?.slot); slot.dataset.empty = String(!this.stack.some(entry => entry.slot === Number(slot.dataset.slot))); }
        for (const entry of this.history) {
            let node = this.stackNodes.get(entry.id);
            if (entry.ejected) { node?.remove(); continue; }
            if (!node) {
                node = document.createElement('div'); node.className = 'bg-stack-card'; node.dataset.entry = entry.id;
                const image = document.createElement('img'); image.src = TutorialCampaign.cards[entry.card.trainingKey].image; image.alt = ''; image.draggable = false;
                const label = text('div', ''); label.append(text('small', `${entry.player === this.c.self_player ? 'You' : 'Enemy'} · ${entry.kind === 'defense' ? 'Defend' : entry.kind === 'entry' ? 'Entry' : entry.card.trainingKey === 'counter' ? 'Counter' : TutorialCampaign.cards[entry.card.trainingKey].boost ? 'Buff' : 'Spell'}`), text('strong', entry.card.name), text('b', ''));
                node.append(image, label); this.stackNodes.set(entry.id, node);
            }
            const previous = node.dataset.state, animate = !previous || previous !== entry.state && entry.state === 'lifting';
            const before = node.isConnected ? node.getBoundingClientRect() : this.guide.item(entry.kind === 'defense' ? entry.target : entry.card, '');
            if (animate) node.style.animation = 'none';
            if (entry === this.activeEntry) { if (node.parentElement !== out) out.append(node); }
            else if (['waiting', 'countered'].includes(entry.state)) { const slot = slots.children[entry.slot]; if (node.parentElement !== slot) slot.append(node); }
            else { node.remove(); continue; }
            node.dataset.state = entry.state;
            node.querySelector('b').textContent = entry.state === 'waiting' ? entry === this.stack.at(-1) ? 'TOP ↑' : 'WAIT' : entry.state === 'ready' ? 'READY' : entry.state === 'fizzled' ? 'NO TARGET' : entry.state === 'skipped' ? 'NO DEFENDER' : entry.state === 'countered' ? 'CANCELLED' : entry.state === 'lifting' ? 'TAKE OUT' : this.choiceMode ? 'SCRY 1' : 'RESOLVE';
            if (animate) {
                const after = node.getBoundingClientRect(); node.style.setProperty('--card-x', `${before ? before.x + (before.w || before.width) / 2 - after.x - after.width / 2 : 0}px`); node.style.setProperty('--card-y', `${before ? before.y - after.y : -40}px`);
                node.style.removeProperty('animation');
            }
        }
        const combat = find('.bg-combat'); combat.hidden = !this.pendingCombat;
        if (this.pendingCombat) {
            if (combat.dataset.card !== String(this.pendingCombat.attacker.id)) {
                combat.replaceChildren(); const card = this.pendingCombat.attacker.card, image = document.createElement('img'); image.src = TutorialCampaign.cards[card.trainingKey].image; image.alt = ''; image.draggable = false;
                const label = text('div', ''); label.append(text('small', 'Pending attack · outside the stack'), text('strong', card.name)); combat.append(image, label); combat.dataset.card = this.pendingCombat.attacker.id;
            }
            combat.dataset.entry = 'attack';
        }
    }
    get flowLinks() {
        const links = [];
        if (this.pendingCombat) links.push({from: this.pendingCombat.attacker, to: 'attack', color: '#bd8a77'});
        for (const entry of [...this.stack, ...(this.activeEntry ? [this.activeEntry] : [])]) {
            const source = entry.kind === 'defense' ? entry.target : entry.player;
            const targetPresent = entry.target instanceof Player || entry.target?.Life > 0 && [...this.c.table.self_battlefield, ...this.c.table.opponent_battlefield].includes(entry.target);
            if (entry.kind !== 'defense' || targetPresent) links.push({from: source, to: entry.id});
            if (entry.kind === 'spell' && targetPresent) links.push({from: entry.id, to: entry.target, color: '#9fc7ae'});
            if (entry.counterTarget) links.push({from: entry.id, to: entry.counterTarget.id, color: '#c58b78'});
        }
        if (this.combatLink) links.push(this.combatLink);
        return links.slice(-9);
    }
}
