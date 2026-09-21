class Decks_Container {
    constructor() {
        // Keep the legacy spelling and [id, name] shape used by every game entry.
        this.seleted_deck = NaN;
        this.all_decks = [];
        this.process_listener();
        this.ready = this.get_all_decks();
    }
    error(message) { document.dispatchEvent(new CustomEvent('lobby:error',{detail:message})); }
    async get_all_decks() {
        try {
            const response = await fetch('/get_decks_home',{method:'POST',headers:{'Content-Type':'application/json'},signal:AbortSignal.timeout(20000)});
            if (!response.ok) throw new Error();
            const data = await response.json();
            if (!Array.isArray(data)) throw new Error();
            this.process_data(data);
        } catch (_) {
            const empty = document.getElementById('deck-empty');
            empty.hidden = false; empty.textContent = 'Unable to load decks.';
            const retry = document.createElement('button'); retry.className='text-link';retry.textContent='Retry';
            retry.addEventListener('click',()=>{empty.textContent='Loading…';this.ready=this.get_all_decks();}); empty.append(retry);
        }
    }
    process_data(data) {
        this.all_decks.forEach(deck=>deck.divbutton.remove());
        this.all_decks = data.map(item=>new Deck(...item.content,this,item.id));
        this.updateEmpty();
    }
    updateEmpty() {
        const empty=document.getElementById('deck-empty');
        empty.hidden=this.all_decks.length>0;empty.textContent='No decks yet. Build a deck to get started.';
    }
    process_listener() {
        document.getElementById('choose_deck').addEventListener('click',()=>{
            const selected=this.find_child('button_process_deck_click');
            if (!selected || this.deleting) return;
            this.seleted_deck=[selected.id,selected.name];
            this.close_all('selected');
            document.dispatchEvent(new CustomEvent('lobby:deck-selected',{detail:this.seleted_deck}));
        });
        document.getElementById('delete_deck').addEventListener('click',async()=>{
            const selected=this.find_child('button_process_deck_click');
            if (!selected || this.deleting) return;
            this.deleting=true;this.setActions(false);
            try { await this.delete_deck(selected); }
            finally { this.deleting=false;this.setActions(Boolean(this.find_child('button_process_deck_click'))); }
        });
    }
    setActions(enabled) {
        document.getElementById('choose_deck').disabled=!enabled;
        document.getElementById('delete_deck').disabled=!enabled;
    }
    async delete_deck(deck) {
        try {
            const response=await fetch('/delete_deck',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:deck.id,name:deck.name}),signal:AbortSignal.timeout(20000)});
            if (!response.ok || (await response.json()).state!=='successful') throw new Error();
            deck.divbutton.remove();this.all_decks=this.all_decks.filter(item=>item!==deck);
            if (this.seleted_deck && this.seleted_deck[0]===deck.id) this.seleted_deck=NaN;
            this.resetPreview();this.updateEmpty();document.dispatchEvent(new Event('lobby:deck-deleted'));
        } catch (_) { this.error('Unable to delete the deck. Please try again.'); }
    }
    resetPreview() {
        this.clear_child('button_process_deck_click');
        document.getElementById('button_process').classList.remove('show_button_process');
        document.querySelectorAll('.box_cards').forEach(box=>{box.classList.remove('box_cards_front');box.replaceChildren();});
        document.getElementById('deck-preview-hint').hidden=false;this.setActions(false);
    }
    close_all(reason='cancel') {
        this.resetPreview();
        document.getElementById('box_decks').classList.remove('box_decks-visible');
        document.getElementById('deck-dialog').close(reason);
    }
    clear_child(className) {
        this.all_decks.forEach(deck=>{deck.divbutton.classList.remove(className);deck.divbutton.setAttribute('aria-pressed','false');});
    }
    find_child(className) { return this.all_decks.find(deck=>deck.divbutton.classList.contains(className)) || false; }
    // The list now uses HTML, so no perpetual canvas redraw is needed.
    draw() {}
}
