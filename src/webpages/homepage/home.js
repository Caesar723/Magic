// Keep the existing entry methods and backend contracts in one place.
function choose_a_deck() {
    const dialog = document.getElementById('deck-dialog');
    if (dialog.open) dialog.close('cancel');
    else { document.getElementById('box_decks').classList.add('box_decks-visible'); dialog.showModal(); }
}

class Home {
    constructor(decks) {
        this.decks = decks;
        this.pendingMode = null;
        this.match = null;
        this.set_listener();
    }
    notify(message) {
        const notice = document.getElementById('lobby-notice');
        notice.textContent = message; notice.hidden = false;
        clearTimeout(this.noticeTimer);
        this.noticeTimer = setTimeout(() => notice.hidden = true, 6500);
    }
    showModes(open, restoreFocus = false) {
        document.getElementById('mode-picker').hidden = !open;
        document.getElementById('start-game').setAttribute('aria-expanded', String(open));
        if (open) document.getElementById('start').focus();
        else if (restoreFocus) document.getElementById('start-game').focus();
    }
    set_listener() {
        const pages = { draw:'/draw_card', deck:'/deck_building', shop:'/shop', studio:'/studio', tasks:'/task', history:'/game_replay' };
        Object.entries(pages).forEach(([id,path]) => document.getElementById(id).addEventListener('click', () => { (window.PageTransition?.navigate || (path => location.assign(path)))(path); }));
        document.getElementById('start-game').addEventListener('click', () => this.showModes(document.getElementById('mode-picker').hidden));
        document.getElementById('close-modes').addEventListener('click', () => this.showModes(false,true));
        document.addEventListener('pointerdown', event => {
            if (!event.target.closest('#mode-picker, #start-game')) this.showModes(false);
        });
        document.addEventListener('keydown', event => {
            if (event.key === 'Escape' && !document.getElementById('mode-picker').hidden) this.showModes(false,true);
        });
        document.getElementById('choose').addEventListener('click', () => {
            this.pendingMode = null;
            document.getElementById('deck-context').textContent = 'Select a deck.';
            choose_a_deck();
        });
        document.getElementById('start').addEventListener('click', () => this.requestMode('pvp'));
        // This legacy ID has always started /matching_ai. Keep that contract.
        document.getElementById('tutorial').addEventListener('click', () => this.requestMode('ai'));
        document.getElementById('rogue').addEventListener('click', () => this.requestMode('rogue'));
        document.getElementById('guide-practice').addEventListener('click', () => {
            document.getElementById('guide-dialog').close(); this.requestMode('ai');
        });
        document.getElementById('close-decks').addEventListener('click', () => this.decks.close_all('cancel'));
        document.getElementById('deck-dialog').addEventListener('close', event => {
            document.getElementById('box_decks').classList.remove('box_decks-visible');
            if (event.target.returnValue !== 'selected') this.pendingMode = null;
        });
        document.addEventListener('lobby:deck-selected', () => {
            this.updateDeckLabel();
            const mode = this.pendingMode; this.pendingMode = null;
            if (mode) this.runMode(mode);
        });
        document.addEventListener('lobby:deck-deleted', () => this.updateDeckLabel());
        document.addEventListener('lobby:error', event => this.notify(event.detail));
        document.getElementById('game-tutorial').addEventListener('click', () => document.getElementById('guide-dialog').showModal());
        document.getElementById('setting').addEventListener('click', () => document.getElementById('settings-dialog').showModal());
        document.querySelectorAll('[data-close-dialog]').forEach(button => button.addEventListener('click', () => button.closest('dialog').close()));
        const cancel = () => {
            if (!this.match) return;
            this.match.cancelled = true;
            this.match.wake?.();
            document.getElementById('cancel-matching').disabled = true;
            document.getElementById('matching-title').textContent = 'Cancelling match…';
        };
        document.getElementById('cancel-matching').addEventListener('click', cancel);
        document.getElementById('matching-dialog').addEventListener('cancel', event => { event.preventDefault(); cancel(); });
    }
    updateDeckLabel() {
        const selected = this.decks.seleted_deck;
        const label = document.getElementById('selected-deck');
        label.textContent = selected ? `Deck: ${selected[1]}` : '';
        label.hidden = !selected;
        document.getElementById('choose').title = selected ? selected[1] : 'Choose Deck';
    }
    requestMode(mode) {
        if (this.match) return;
        this.showModes(false);
        if (!this.decks.seleted_deck) {
            this.pendingMode = mode;
            const label = {pvp:'PVP',ai:'Play vs AI',rogue:'Rogue'}[mode];
            document.getElementById('deck-context').textContent = `Select a deck to continue to ${label}.`;
            if (!document.getElementById('deck-dialog').open) choose_a_deck();
            return;
        }
        return this.runMode(mode);
    }
    async runMode(mode) {
        if (this.match || !this.decks.seleted_deck) return;
        const match = {cancelled:false,mode}; this.match = match;
        const dialog = document.getElementById('matching-dialog');
        document.getElementById('matching-title').textContent = {pvp:'Finding an opponent…',ai:'Preparing match…',rogue:'Opening Rogue…'}[mode];
        document.getElementById('matching-description').textContent = `Deck: ${this.decks.seleted_deck[1]}`;
        document.getElementById('cancel-matching').disabled = false;
        dialog.showModal();
        let entering = false;
        try {
            const endpoint = {pvp:'/matching',ai:'/matching_ai',rogue:'/rogue/initinal_room'}[mode];
            let data = await this.send_match_request(endpoint);
            while (mode === 'pvp' && data.state === 'waiting' && !match.cancelled) {
                await this.set_time(match);
                if (!match.cancelled) data = await this.send_match_request(endpoint);
            }
            if (match.cancelled) return;
            const success = mode === 'rogue' ? ['success','already in room'].includes(data.state) : data.state === 'find!';
            if (!success) throw new Error(data.state === 'unvalid deck' ? 'This deck cannot be used. Choose another deck or edit it.' : 'Unable to start the game. Please try again.');
            entering = true;
            (window.PageTransition?.navigate || (path => location.assign(path)))({pvp:'/gaming',ai:'/gaming_ai',rogue:'/rogue/rogue_map'}[mode]);
        } catch (error) {
            if (!match.cancelled) this.notify(error.name === 'TimeoutError' ? 'Connection timed out. Please try again.' : error.message || 'Connection failed. Please try again.');
        } finally {
            // Wait for the in-flight matching response before deleting the queue entry:
            // cancelling must never race a late "find!" response into /gaming.
            if (!entering && mode !== 'rogue') {
                try { await this.post('/matching_delete'); }
                catch (_) { this.notify('Unable to cancel the match. Check your connection and retry.'); }
            }
            dialog.close(); this.match = null;
        }
    }
    start_matching() { return this.requestMode('pvp'); }
    start_matching_ai() { return this.requestMode('ai'); }
    start_matching_rogue() { return this.requestMode('rogue'); }
    set_time(match) {
        return new Promise(resolve => {
            const timer = setTimeout(resolve,3000);
            match.wake = () => { clearTimeout(timer); resolve(); };
        });
    }
    async post(url, body) {
        const response = await fetch(url, {method:'POST',headers:{'Content-Type':'application/json'}, ...(body ? {body:JSON.stringify(body)} : {}), signal:AbortSignal.timeout(20000)});
        if (!response.ok) throw new Error('Connection failed. Check your connection or sign in again.');
        try { return await response.json(); }
        catch (_) { throw new Error('Your session may have expired. Refresh the page and try again.'); }
    }
    send_match_request(name) {
        return this.post(name,{id:this.decks.seleted_deck[0],name:this.decks.seleted_deck[1]});
    }
}
