// Page presentation only. The existing Deck model owns quantities and save serialization.
class Book {
    constructor(deck) {
        this.deck = deck;
        this.ui = Object.fromEntries([...document.querySelectorAll('[id]')].map(element => [element.id, element]));
        this.frame_generator = new Card_frame();
        this.records = new Map();
        this.visible = [];
        this.page_number = 1;
        this.current_type_mark = 'creature';
        this.current_color_mark = 'blue';
        this.request = 0;
        this.busy = false;
        this.loading = false;
        this.uncertain = false;
        this.editing = null;
        this.replacement = null;
        this.savedDecks = [];
        this.savedRequest = 0;
        this.cleanDraft = this.draft_signature();
        this.flights = new Set();
        this.soundEffect_card = new Audio('/webpages/audio/music_sorce/card/send.mp3');
        this.soundEffect_card.volume = .3;
        this.set_listener();
    }
    node(tag, className, text) {
        const element = document.createElement(tag);
        if (className) element.className = className;
        if (text != null) element.textContent = String(text);
        return element;
    }
    key(data) {
        const type = data.Type_card === 'land' ? 'Land' : data.Type_card === 'sorcery' ? 'Sorcery' : data.Type_card === 'Instant' ? 'Instant' : 'Creature';
        return data.Name + '_' + type;
    }
    async post(path, body) {
        const response = await fetch(path, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body), signal: AbortSignal.timeout(20000)});
        if (!response.ok || response.redirected) throw new Error('Request could not be confirmed.');
        const data = await response.json();
        return typeof data === 'string' ? JSON.parse(data) : data;
    }
    async send_page_request(offset, type, color) {
        const data = await this.post('/deck_page', {offset, type_card: type, color_card: color});
        if (!Array.isArray(data) || data.some(card => !card || typeof card.Name !== 'string' || typeof card.Type_card !== 'string' || !Number.isSafeInteger(card.quantity) || card.quantity < 0)) throw new Error('Invalid collection.');
        return data;
    }
    async fetch_saved_decks() {
        const data = await this.post('/get_decks_home');
        if (!Array.isArray(data)) throw new Error('Invalid deck list.');
        return data.map(item => {
            if (!Number.isSafeInteger(item?.id) || !Array.isArray(item.content) || typeof item.content[0] !== 'string' || !Array.isArray(item.content[1])) throw new Error('Invalid deck.');
            const cards = new Map();
            for (const card of item.content[1]) {
                if (!card || typeof card.name !== 'string' || !['creature', 'Instant', 'sorcery', 'land'].includes(card.type_card) || !Number.isSafeInteger(card.quantity) || card.quantity < 1) throw new Error('Invalid deck card.');
                const key = JSON.stringify([card.name, card.type_card]);
                const entry = cards.get(key) || {...card, quantity: 0};
                entry.quantity += card.quantity; cards.set(key, entry);
            }
            return {id: item.id, name: item.content[0], cards: [...cards.values()]};
        });
    }
    async open_saved() {
        if (this.busy || this.replacement) return;
        const request = ++this.savedRequest;
        this.selectedSaved = null;
        this.ui['saved-list'].replaceChildren(); this.ui['saved-preview'].hidden = true;
        this.ui['saved-status'].textContent = 'Loading decks…'; this.ui['retry-saved'].hidden = true;
        this.update_stock();
        if (!this.ui['saved-decks'].open) this.ui['saved-decks'].showModal();
        try {
            const decks = await this.fetch_saved_decks();
            if (request !== this.savedRequest || this.disposed) return;
            this.savedDecks = decks;
            this.ui['saved-status'].textContent = decks.length ? '' : 'No saved decks yet.';
            this.ui['saved-list'].replaceChildren(...decks.map(saved => {
                const button = this.node('button', 'saved-deck'); button.type = 'button';
                button.dataset.id = saved.id; button.setAttribute('aria-pressed', 'false');
                const image = this.node('img'); image.src = '/webpages/image_source/card/back.png?v=compass'; image.alt = '';
                const label = this.node('span', '', saved.name);
                label.append(this.node('small', '', this.saved_count(saved)));
                button.append(image, label); return button;
            }));
            if (decks.length) this.select_saved(decks[0]);
        } catch (_) {
            if (request !== this.savedRequest || this.disposed) return;
            this.ui['saved-status'].textContent = 'Unable to load saved decks.'; this.ui['retry-saved'].hidden = false;
        }
    }
    saved_count(saved) {
        const count = saved.cards.reduce((sum, card) => sum + card.quantity, 0);
        return count + (count === 1 ? ' card' : ' cards');
    }
    select_saved(saved) {
        this.selectedSaved = saved;
        this.ui['saved-status'].textContent = '';
        this.ui['saved-list'].querySelectorAll('button').forEach(button => button.setAttribute('aria-pressed', String(Number(button.dataset.id) === saved.id)));
        this.ui['saved-name'].textContent = saved.name;
        this.ui['saved-count'].textContent = this.saved_count(saved);
        this.ui['saved-cards'].replaceChildren(...saved.cards.map(card => {
            const row = this.node('li'), image = this.node('img'); image.alt = ''; image.loading = 'lazy';
            image.src = '/cards/' + encodeURIComponent(card.type_card) + '/' + encodeURIComponent(card.name) + '/compress_img.jpg';
            image.onerror = () => { image.hidden = true; };
            row.append(image, this.node('span', '', card.name), this.node('b', '', '× ' + card.quantity)); return row;
        }));
        this.ui['saved-preview'].hidden = false; this.update_stock();
    }
    async editable_cards(saved) {
        const groups = new Map(), found = new Map();
        // Saved decks contain names and counts only. Read metadata to find the relevant collection pages.
        for (let i = 0; i < saved.cards.length; i += 4) {
            await Promise.all(saved.cards.slice(i, i + 4).map(async card => {
                const type = {creature: 'Creature', Instant: 'Instant', sorcery: 'Sorcery', land: 'Land'}[card.type_card];
                let color = this.records.get(card.name + '_' + type)?.data.Background_url;
                if (!color) {
                    const response = await fetch('/cards/' + encodeURIComponent(card.type_card) + '/' + encodeURIComponent(card.name) + '/data.json', {signal: AbortSignal.timeout(20000)});
                    if (!response.ok || response.redirected) throw new Error('Card unavailable.');
                    const data = await response.json();
                    color = card.type_card === 'land' ? {Water: 'blue', Light: 'gold', Dark: 'black', Fire: 'red', Forest: 'green', Arcane: 'colorless'}[data.Type]
                        : {U: 'blue', W: 'gold', B: 'black', R: 'red', G: 'green'}[data.Cost?.slice(-1)] || 'colorless';
                    if (!color) throw new Error('Unknown card color.');
                }
                const key = card.type_card + '/' + color;
                if (!groups.has(key)) groups.set(key, {type: card.type_card, color, names: new Set()});
                groups.get(key).names.add(card.name);
            }));
        }
        const selections = [...groups.values()];
        for (let i = 0; i < selections.length; i += 4) {
            await Promise.all(selections.slice(i, i + 4).map(async group => {
                for (let offset = 0; group.names.size; offset += 8) {
                    const page = await this.send_page_request(offset, group.type, group.color);
                    for (const card of page) if (group.names.delete(card.Name)) found.set(group.type + '/' + card.Name, card);
                    if (page.length < 8) break;
                }
            }));
        }
        return saved.cards.map(card => {
            const data = found.get(card.type_card + '/' + card.name);
            if (!data || data.quantity < card.quantity) throw new Error('Some cards are no longer available in the saved quantities. Your current deck is unchanged.');
            return {data, quantity: card.quantity};
        });
    }
    draft_signature() {
        return JSON.stringify([this.ui.deck_name.value, Object.entries(this.deck.cards).map(([key, entry]) => [key, entry.quantity]).sort(([a], [b]) => a.localeCompare(b))]);
    }
    replace_draft(cards = [], source = null) {
        if (this.draft_signature() !== this.cleanDraft && !window.confirm('Discard your unsaved changes and open another deck?')) return false;
        this.pause();
        for (const record of this.records.values()) record.card.quantity = record.owned;
        this.deck.cards = {};
        for (const {data, quantity} of cards) {
            const key = this.key(data);
            let record = this.records.get(key);
            if (!record) { record = this.create_record(data); this.records.set(key, record); }
            record.owned = data.quantity; record.card.quantity = data.quantity - quantity;
            this.deck.push_card(record.card); this.deck.cards[key].quantity = quantity;
        }
        this.editing = source ? {id: source.id, name: source.name} : null;
        this.ui.deck_name.value = source?.name || ''; this.ui.deck_name.removeAttribute('aria-invalid');
        this.ui['deck-title'].textContent = source ? 'Editing Deck' : 'Your Deck';
        this.render_deck(); this.cleanDraft = this.draft_signature(); this.status('', false);
        return true;
    }
    async edit_saved() {
        if (this.busy || this.uncertain || this.replacement || !this.selectedSaved) return;
        this.busy = true; this.update_stock(); this.ui['saved-status'].textContent = 'Loading deck…';
        try {
            const cards = await this.editable_cards(this.selectedSaved);
            if (this.disposed) return;
            if (this.replace_draft(cards, this.selectedSaved)) {
                this.ui['saved-decks'].close(); this.ui.deck.scrollIntoView({block: 'nearest'});
            }
            this.ui['saved-status'].textContent = '';
        } catch (error) {
            this.ui['saved-status'].textContent = error.message.startsWith('Some cards') ? error.message : 'Unable to load this deck. Your current deck is unchanged. Try again.';
        } finally {
            this.busy = false; this.update_stock();
            if (!this.ui['saved-decks'].open) this.ui.deck_name.focus({preventScroll: true});
        }
    }
    async load_page(page = this.page_number) {
        if (this.busy) return;
        this.requested_page = page;
        const request = ++this.request;
        this.loading = true;
        this.ui.myCanvas.setAttribute('aria-busy', 'true');
        this.ui.myCanvas.hidden = true;
        this.ui['collection-message'].hidden = false;
        this.ui['collection-message'].dataset.error = 'false';
        this.ui['collection-status'].textContent = 'Loading cards…';
        this.ui['retry-collection'].hidden = true;
        this.ui['previous-page'].disabled = this.ui['next-page'].disabled = true;
        try {
            const data = await this.send_page_request((page - 1) * 8, this.current_type_mark, this.current_color_mark);
            if (request !== this.request || this.disposed) return;
            this.page_number = page;
            const keys = new Set(data.map(card => this.key(card)));
            // Keep only this page and selected cards, rather than retaining canvases for the entire collection.
            for (const [key, record] of this.records) {
                if (!keys.has(key) && !this.deck.cards[key]) { record.observer?.disconnect(); this.records.delete(key); }
            }
            this.visible = data.map(card => {
                const key = this.key(card);
                let record = this.records.get(key);
                if (!record) {
                    record = this.create_record(card);
                    this.records.set(key, record);
                }
                record.owned = card.quantity;
                record.card.quantity = Math.max(0, card.quantity - (this.deck.cards[key]?.quantity || 0));
                return record;
            });
            this.ui.myCanvas.replaceChildren(...this.visible.map((record, index) => this.create_card(record, index)));
            this.ui.myCanvas.hidden = data.length === 0;
            this.ui['collection-message'].hidden = data.length > 0;
            this.ui['collection-status'].textContent = page > 1 ? 'No more cards in this selection.' : 'No cards in this selection. Try another color or type.';
            this.ui['page-number'].textContent = 'Page ' + page;
        } catch (_) {
            if (request !== this.request || this.disposed) return;
            this.ui['collection-message'].dataset.error = 'true';
            this.ui['collection-status'].textContent = 'Unable to load cards. Your deck is still here.';
            this.ui['retry-collection'].hidden = false;
        } finally {
            if (request === this.request && !this.disposed) {
                this.loading = false;
                this.ui.myCanvas.setAttribute('aria-busy', 'false');
                this.ui['previous-page'].disabled = this.page_number <= 1;
                this.ui['next-page'].disabled = this.visible.length < 8 || !this.ui['retry-collection'].hidden;
                this.update_stock();
            }
        }
    }
    create_record(data) {
        const surfaces = this.frame_generator.generate_card(data.Background_url || 'colorless', data.Name, data.Type_card, data.Rarity || 'Common', data.Ability || '', data.Image_url);
        const args = [4, 5.62, [0, 0, 40], 3, surfaces];
        let card;
        if (data.Type_card === 'land') card = new Land(...args, data.Name);
        else if (data.Type_card === 'Instant') card = new Instant(...args, data.Cost || '0', data.Name);
        else if (data.Type_card === 'sorcery') card = new Sorcery(...args, data.Cost || '0', data.Name);
        else card = new Creature(...args, data.Cost || '0', data.Toughness, data.Power, data.Name);
        const record = {key: this.key(data), data, card, owned: data.quantity, ready: false};
        // Card_frame finishes asynchronously; observe its existing canvas without changing the shared renderer.
        record.observer = new MutationObserver(async () => {
            record.observer.disconnect();
            try {
                await Promise.all(card.images_fee.map(image => image.decode()));
                if (this.disposed || this.records.get(record.key) !== record) return;
                card.update(); record.ready = true;
                if (record.element?.isConnected) this.paint_face(record.element.querySelector('.card-preview'), record);
                if (this.detail === record) this.paint_face(this.ui['detail-face'], record);
            } catch (_) { /* The card remains usable through its HTML details if an asset fails. */ }
        });
        record.observer.observe(surfaces[2], {attributes: true, attributeFilter: ['width', 'height']});
        return record;
    }
    paint_face(target, record) {
        if (record.ready) {
            const original = record.card.dynamic_canvas[0];
            const canvas = this.node('canvas', 'original-card-face');
            canvas.width = original.width; canvas.height = original.height;
            canvas.getContext('2d').drawImage(original, 0, 0);
            canvas.setAttribute('role', 'img'); canvas.setAttribute('aria-label', record.data.Name);
            target.replaceChildren(canvas);
        } else {
            const image = this.node('img'); image.alt = '';
            image.src = '/webpages/image_source/card/back.png?v=compass';
            target.replaceChildren(image, this.node('span', 'card-placeholder', record.data.Name));
        }
    }
    action_button(label, action, record, className, text) {
        const button = this.node('button', className, text);
        button.type = 'button'; button.dataset.action = action; button.dataset.key = record.key;
        button.setAttribute('aria-label', label + ' ' + record.data.Name);
        return button;
    }
    create_card(record, index) {
        const element = this.node('article', 'collection-card');
        element.dataset.key = record.key;
        element.style.setProperty('--order', index);
        const preview = this.action_button('View', 'inspect', record, 'card-preview');
        preview.draggable = true;
        this.paint_face(preview, record);
        const controls = this.node('div', 'collection-controls');
        const labels = this.node('div', 'card-labels');
        const name = this.node('span', 'collection-name', record.data.Name); name.title = record.data.Name;
        labels.append(name, this.node('span', 'card-stock'));
        controls.append(labels, this.action_button('Add', 'add', record, 'add-card', '+'));
        element.append(preview, controls); record.element = element;
        return element;
    }
    update_stock() {
        const locked = this.busy || Boolean(this.replacement);
        for (const record of this.visible) {
            if (!record.element?.isConnected) continue;
            record.element.dataset.available = String(record.card.quantity > 0);
            record.element.querySelector('.card-stock').textContent = record.card.quantity + ' available';
            record.element.querySelector('.add-card').disabled = locked || record.card.quantity <= 0;
            record.element.querySelector('.card-preview').draggable = !locked && record.card.quantity > 0;
        }
        this.ui['deck_name'].disabled = locked;
        this.ui.build.disabled = this.busy || this.uncertain;
        if (!this.busy) this.ui.build.textContent = this.replacement ? 'Retry Update' : this.editing ? 'Save Changes →' : 'Save Deck →';
        this.ui['open-saved-decks'].disabled = locked;
        this.ui['new-deck'].disabled = locked || this.uncertain;
        this.ui['edit-saved'].disabled = locked || this.uncertain || !this.selectedSaved;
        this.ui['close-saved'].disabled = this.busy;
        this.ui['saved-list'].querySelectorAll('button').forEach(button => { button.disabled = this.busy; });
        this.ui['deck-list'].querySelectorAll('[data-action]').forEach(button => {
            const record = this.records.get(button.dataset.key);
            button.disabled = locked || (button.dataset.action === 'add' && record.card.quantity <= 0);
        });
        if (this.detail) {
            const count = this.deck.cards[this.detail.key]?.quantity || 0;
            this.ui['detail-quantity'].textContent = this.detail.card.quantity + ' available · ' + count + ' in deck';
            this.ui['detail-add'].disabled = locked || this.detail.card.quantity <= 0;
        }
    }
    render_deck() {
        const active = document.activeElement;
        const focus = this.ui['deck-list'].contains(active) ? {key: active.dataset.key, action: active.dataset.action} : null;
        const rows = [], totals = {Creature: 0, Instant: 0, Sorcery: 0, Land: 0};
        for (const [key, entry] of Object.entries(this.deck.cards)) {
            const record = this.records.get(key);
            totals[entry.card.constructor.name] += entry.quantity;
            const row = this.node('li', 'deck-row'); row.dataset.key = key;
            const image = this.node('img'); image.alt = ''; image.src = '/' + record.data.Image_url.replace(/^\/+/, '');
            image.onerror = () => { image.hidden = true; };
            const name = this.action_button('View', 'inspect', record, 'deck-card-name', record.data.Name);
            name.append(this.node('span', '', record.data.Cost || entry.card.constructor.name));
            const quantity = this.node('div', 'quantity-controls');
            quantity.append(this.action_button('Remove one', 'remove', record, '', '−'), this.node('span', 'deck-quantity', entry.quantity), this.action_button('Add', 'add', record, '', '+'));
            row.append(image, name, quantity); rows.push(row);
        }
        this.ui['deck-list'].replaceChildren(...rows);
        this.ui['deck-empty'].hidden = rows.length > 0;
        const count = Object.values(totals).reduce((sum, value) => sum + value, 0);
        this.ui['deck-count'].textContent = this.ui['mobile-deck-count'].textContent = count;
        this.ui['deck-breakdown'].textContent = totals.Creature + ' creatures · ' + (totals.Instant + totals.Sorcery) + ' spells · ' + totals.Land + ' lands';
        this.update_stock();
        if (focus) {
            const target = [...this.ui['deck-list'].querySelectorAll('button')].find(button => button.dataset.key === focus.key && button.dataset.action === focus.action && !button.disabled)
                || this.ui['deck-list'].querySelector('button') || this.ui['deck_name'];
            target.focus({preventScroll: true});
        }
    }
    change_card(key, delta, source) {
        if (this.busy || this.replacement) return;
        const record = this.records.get(key);
        if (!record) return;
        if (delta > 0) {
            if (record.card.quantity <= 0) return;
            record.card.quantity--; this.deck.push_card(record.card);
            this.animate_add(source, record);
            if (!document.hidden && document.hasFocus()) { this.soundEffect_card.currentTime = 0; this.soundEffect_card.play().catch(() => {}); }
            if (record.element?.isConnected) { record.element.classList.remove('is-added'); void record.element.offsetWidth; record.element.classList.add('is-added'); }
        } else if (this.deck.cards[key]) this.deck.delete_card(this.deck.cards[key], key);
        else return;
        if (!this.uncertain) this.status(delta > 0 ? record.data.Name + ' added.' : 'Removed one ' + record.data.Name + '.', false);
        this.render_deck();
    }
    show_detail(record) {
        this.detail = record;
        const data = record.data;
        this.paint_face(this.ui['detail-face'], record);
        for (const [id, value] of Object.entries({'detail-name': data.Name, 'detail-rarity': data.Rarity, 'detail-type': data.Type_card,
            'detail-cost': data.Cost ? 'Mana cost: ' + data.Cost : '', 'detail-ability': data.Ability,
            'detail-stats': data.Power != null ? 'Power / Toughness: ' + data.Power + ' / ' + data.Toughness : ''})) this.ui[id].textContent = value || '';
        this.update_stock(); this.ui['card-detail'].showModal();
    }
    status(message, error = true) {
        this.ui['deck-status'].textContent = message;
        this.ui['deck-status'].dataset.error = String(error);
    }
    async remove_original() {
        const original = this.replacement;
        try {
            const response = await this.post('/delete_deck', original);
            if (response.state === 'successful') return;
        } catch (_) { /* A lost deletion response can be checked against the saved list. */ }
        const decks = await this.fetch_saved_decks();
        if (decks.some(saved => saved.id === original.id)) throw new Error('Original deck still exists.');
    }
    async save() {
        if (this.busy || this.uncertain) return;
        const name = this.ui.deck_name.value.replace(/[|+]/g, '').trim();
        if (!name) { this.status('Give your deck a name.'); this.ui.deck_name.setAttribute('aria-invalid', 'true'); this.ui.deck_name.focus(); return; }
        if (this.deck.check_empty()) { this.status('Add at least one card before saving.'); return; }
        if (!this.replacement && this.editing && this.draft_signature() === this.cleanDraft) { this.status('No changes to save.', false); return; }
        this.ui.deck_name.value = name;
        this.busy = true; this.update_stock();
        this.ui.build.textContent = 'Saving…'; this.status('Saving your deck…', false);
        let sent = false, saved = false, created = Boolean(this.replacement);
        try {
            if (!created) {
                const data = await this.deck.settle_deck(name);
                sent = true;
                const response = await this.post('/send_deck', {data});
                if (response.state === 'unsuccessful') { this.status('Unable to save this deck. Check that you still own the selected cards.'); return; }
                if (response.state !== 'successful') throw new Error('Unexpected save result.');
                created = true;
                // Capture the original identity, including its old name, only after the new deck is confirmed saved.
                if (this.editing) this.replacement = {...this.editing};
            }
            if (this.replacement) {
                this.ui.build.textContent = 'Updating…';
                this.status('New deck saved. Finishing the update…', false);
                await this.remove_original();
            }
            saved = true; this.status('Deck saved. Returning to the lobby…', false);
            (window.PageTransition?.navigate || (path => location.assign(path)))('/');
        } catch (_) {
            if (created) {
                this.status('Your updated deck is saved. Removing the original could not be confirmed. Retry Update to finish.');
            } else if (sent) {
                // A lost response may already have created the deck. Never automatically resubmit it.
                this.uncertain = true;
                const message = this.editing ? 'Saving could not be confirmed. The original deck was not deleted. Check your decks in the lobby before saving again.' : 'Saving could not be confirmed. Check your decks in the lobby before saving again.';
                this.status(message); this.ui.text_box.textContent = message;
                this.ui.box.showModal(); this.ui['check-decks'].focus();
            } else this.status('Saving is unavailable. Use a browser with a secure connection and try again.');
        } finally {
            if (!saved) { this.busy = false; this.update_stock(); }
        }
    }
    set_listener() {
        this.ui['open-saved-decks'].addEventListener('click', () => this.open_saved());
        this.ui['retry-saved'].addEventListener('click', () => this.open_saved());
        this.ui['close-saved'].addEventListener('click', () => this.ui['saved-decks'].close());
        this.ui['saved-decks'].addEventListener('cancel', event => { if (this.busy) event.preventDefault(); });
        this.ui['saved-decks'].addEventListener('close', () => { ++this.savedRequest; });
        this.ui['saved-list'].addEventListener('click', event => {
            if (this.busy) return;
            const button = event.target.closest('[data-id]');
            const saved = button && this.savedDecks.find(item => item.id === Number(button.dataset.id));
            if (saved) this.select_saved(saved);
        });
        this.ui['edit-saved'].addEventListener('click', () => this.edit_saved());
        this.ui['new-deck'].addEventListener('click', () => {
            if (!this.busy && !this.uncertain && !this.replacement && this.replace_draft()) this.ui.deck_name.focus();
        });
        for (const [id, field, attribute] of [['type-filters', 'current_type_mark', 'type'], ['color-filters', 'current_color_mark', 'color']]) {
            this.ui[id].addEventListener('click', event => {
                const button = event.target.closest('button');
                if (!button || this.busy || this[field] === button.dataset[attribute]) return;
                this[field] = button.dataset[attribute]; this.page_number = 1;
                this.ui[id].querySelectorAll('button').forEach(entry => entry.setAttribute('aria-pressed', String(entry === button)));
                this.load_page(1);
            });
        }
        for (const id of ['myCanvas', 'deck-list']) this.ui[id].addEventListener('click', event => {
            const button = event.target.closest('[data-action]');
            if (!button) return;
            const record = this.records.get(button.dataset.key);
            if (!record) return;
            if (button.dataset.action === 'inspect') this.show_detail(record);
            else this.change_card(record.key, button.dataset.action === 'add' ? 1 : -1, button);
        });
        this.ui['previous-page'].addEventListener('click', () => { if (!this.loading && this.page_number > 1) this.load_page(this.page_number - 1); });
        this.ui['next-page'].addEventListener('click', () => { if (!this.loading) this.load_page(this.page_number + 1); });
        this.ui['retry-collection'].addEventListener('click', () => this.load_page(this.requested_page));
        this.ui.build.addEventListener('click', () => this.save());
        this.ui.deck_name.addEventListener('input', () => { this.ui.deck_name.removeAttribute('aria-invalid'); if (!this.uncertain) this.status('', false); });
        this.ui['detail-add'].addEventListener('click', () => { if (this.detail) this.change_card(this.detail.key, 1, this.ui['detail-face']); });
        this.ui['close-detail'].addEventListener('click', () => this.ui['card-detail'].close());
        this.ui['card-detail'].addEventListener('close', () => { this.detail = null; });
        this.ui['close-message'].addEventListener('click', () => { this.ui.box.close(); this.ui.deck_name.focus(); });
        this.ui.myCanvas.addEventListener('dragstart', event => {
            const preview = event.target.closest('.card-preview');
            const record = preview && this.records.get(preview.dataset.key);
            if (!record || this.busy || this.replacement || record.card.quantity <= 0) { event.preventDefault(); return; }
            event.dataTransfer.setData('application/x-magic-card', record.key);
            event.dataTransfer.effectAllowed = 'copy'; this.dragSource = preview;
        });
        this.ui.deck.addEventListener('dragover', event => {
            if (!this.busy && !this.replacement && event.dataTransfer.types.includes('application/x-magic-card')) { event.preventDefault(); event.dataTransfer.dropEffect = 'copy'; this.ui.deck.classList.add('is-dragover'); }
        });
        this.ui.deck.addEventListener('dragleave', event => { if (!this.ui.deck.contains(event.relatedTarget)) this.ui.deck.classList.remove('is-dragover'); });
        this.ui.deck.addEventListener('drop', event => {
            if (!event.dataTransfer.types.includes('application/x-magic-card')) return;
            event.preventDefault(); this.ui.deck.classList.remove('is-dragover');
            this.change_card(event.dataTransfer.getData('application/x-magic-card'), 1, this.dragSource);
        });
        document.addEventListener('dragend', () => { this.dragSource = null; this.ui.deck.classList.remove('is-dragover'); });
    }
    animate_add(source, record) {
        if (!source || !record.ready || document.hidden || !document.hasFocus() || document.body.classList.contains('motion-reduced')) return;
        const origin = (source.closest('.collection-card')?.querySelector('.card-preview') || source).getBoundingClientRect();
        const deckBounds = this.ui['deck-count'].getBoundingClientRect();
        const target = deckBounds.top > innerHeight ? this.ui['mobile-deck-count'].getBoundingClientRect() : deckBounds;
        const ghost = this.node('canvas');
        ghost.width = 150; ghost.height = 210; ghost.setAttribute('aria-hidden', 'true');
        const context = ghost.getContext('2d');
        // The shared 3D renderer stores the original face upside down.
        context.setTransform(1, 0, 0, -1, 0, ghost.height);
        context.drawImage(record.card.dynamic_canvas[0], 0, 0, 150, 210);
        Object.assign(ghost.style, {position: 'fixed', pointerEvents: 'none', zIndex: '8', width: '75px', height: '105px', left: origin.x + origin.width / 2 - 37 + 'px', top: origin.y + 'px'});
        document.body.append(ghost);
        const animation = ghost.animate([{transform: 'translate(0,0) rotate(-7deg)', opacity: .9}, {transform: 'translate(' + (target.x + target.width / 2 - origin.x - origin.width / 2) + 'px,' + (target.y - origin.y) + 'px) rotate(12deg) scale(.18)', opacity: 0}], {duration: 480, easing: 'cubic-bezier(.2,.7,.2,1)'});
        this.flights.add(animation);
        if (this.flights.size > 4) this.flights.values().next().value.cancel();
        animation.finished.catch(() => {}).finally(() => { ghost.remove(); this.flights.delete(animation); });
    }
    pause() { this.flights.forEach(animation => animation.cancel()); this.soundEffect_card.pause(); }
    dispose() {
        this.disposed = true; this.pause();
        this.records.forEach(record => record.observer?.disconnect());
    }
}
