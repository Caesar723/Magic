// This page owns presentation only. Inventory and card rolls remain server-owned.
class Draw_card {
    constructor() {
        this.ui = Object.fromEntries([...document.querySelectorAll('[id]')].map(node => [node.id, node]));
        this.packs = [];
        this.card_in_pack = [];
        this.card_show = [];
        this.moving_mouse_obj = null;
        this.state = 'loading';
        this.phase = 0;
        this.reduced = false;
        this.frame_generator = new Card_frame();
        this.card_faces = [];
        this.face_observers = new Set();
    }
    node(tag, className, text) {
        const node = document.createElement(tag);
        if (className) node.className = className;
        if (text != null) node.textContent = String(text);
        return node;
    }
    image(path, className) {
        const image = this.node('img', className);
        image.alt = '';
        image.src = '/' + String(path || '').replace(/^\/+/, '');
        image.addEventListener('error', () => { image.hidden = true; });
        return image;
    }
    style_for(pack) {
        return getPackArt(pack);
    }
    artwork(element, pack) {
        const style = this.style_for(pack);
        element.style.setProperty('--accent', style.color);
        element.style.setProperty('--pack-trim', style.trim);
        element.dataset.shape = style.shape;
        const image = element.querySelector('img');
        if (image) {
            image.onerror = () => { image.onerror = () => { image.hidden = true; }; image.src = style.fallback; };
            image.hidden = false;
            image.src = style.image;
        }
    }
    set_listener(canvas) {
        this.canvas = canvas;
        this.ui['open-pack'].addEventListener('click', () => this.open_pack());
        this.ui['retry-packs'].addEventListener('click', () => this.send_packs_request());
        this.ui['skip-animation'].addEventListener('click', () => this.finish_opening());
        this.ui['reveal-all'].addEventListener('click', () => {
            this.card_in_pack.forEach((_, index) => this.draw_a_card(index));
        });
        this.ui['open-another'].addEventListener('click', () => this.reset());
        this.ui['close-detail'].addEventListener('click', () => this.ui['card-detail'].close());
        this.ui['pack-list'].addEventListener('click', event => {
            const button = event.target.closest('[data-pack]');
            if (button) this.select_pack(this.packs[Number(button.dataset.pack)]);
        });
        this.ui['pack-list'].addEventListener('dragstart', event => {
            const button = event.target.closest('[data-pack]');
            if (!button || this.state !== 'ready') { event.preventDefault(); return; }
            event.dataTransfer.setData('application/x-magic-pack', button.dataset.pack);
            event.dataTransfer.effectAllowed = 'move';
        });
        const stage = this.ui.canvasContainer;
        stage.addEventListener('dragover', event => {
            if (this.state === 'ready' && event.dataTransfer.types.includes('application/x-magic-pack')) {
                event.preventDefault(); stage.classList.add('is-dragging');
            }
        });
        stage.addEventListener('dragleave', event => {
            if (!stage.contains(event.relatedTarget)) stage.classList.remove('is-dragging');
        });
        stage.addEventListener('drop', event => {
            event.preventDefault(); stage.classList.remove('is-dragging');
            const index = event.dataTransfer.getData('application/x-magic-pack');
            if (index !== '' && this.select_pack(this.packs[Number(index)])) this.open_pack();
        });
        document.addEventListener('dragend', () => stage.classList.remove('is-dragging'));
        this.ui['rotate-pack'].addEventListener('click', () => this.scene?.rotate());
    }
    set_state(state) {
        this.state = state;
        this.ui.canvasContainer.dataset.state = state;
        this.ui['rotate-pack'].hidden = state !== 'ready' || !this.scene || !this.moving_mouse_obj;
        const showingCards = ['opening', 'reveal', 'complete'].includes(state);
        this.ui['draw-results'].hidden = !showingCards;
        this.ui['open-pack'].hidden = showingCards;
        this.ui['open-pack'].disabled = state !== 'ready' || !this.moving_mouse_obj;
        this.ui['skip-animation'].hidden = state !== 'opening';
        this.ui['result-actions'].hidden = !['reveal', 'complete'].includes(state);
        this.ui['reveal-all'].hidden = state !== 'reveal';
        this.ui['open-another'].hidden = state !== 'complete';
        this.ui['pack-list'].querySelectorAll('button').forEach(button => {
            button.disabled = state !== 'ready'; button.draggable = state === 'ready';
        });
        this.invalidate?.();
    }
    notify(message) {
        this.ui['draw-notice'].textContent = message;
        this.ui['draw-notice'].hidden = false;
    }
    async post(path, body) {
        const response = await fetch(path, {
            method: 'POST', headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(body), signal: AbortSignal.timeout(30000)
        });
        if (!response.ok || response.redirected) throw new Error('Please check your connection or sign in again.');
        const data = await response.json();
        const decoded = typeof data === 'string' ? JSON.parse(data) : data;
        if (!Array.isArray(decoded)) throw new Error('Unexpected server response. Please reload your packs.');
        return decoded;
    }
    async send_packs_request() {
        if (this.loading || ['requesting', 'opening', 'reveal', 'complete'].includes(this.state)) return;
        this.loading = true;
        this.set_state('loading');
        this.ui['pack-list'].setAttribute('aria-busy', 'true');
        this.ui['retry-packs'].hidden = true;
        this.ui['inventory-message'].hidden = false;
        this.ui['inventory-message'].textContent = 'Loading packs…';
        try {
            const data = await this.post('/get_packs_information', {message: 'get_packs_information'});
            this.process_responseData(data);
        } catch (error) {
            this.set_state('error');
            this.ui['inventory-message'].textContent = 'Unable to load your packs.';
            this.ui['retry-packs'].hidden = false;
            this.ui['opening-status'].textContent = error.message;
        } finally {
            this.loading = false;
            this.ui['pack-list'].setAttribute('aria-busy', 'false');
        }
    }
    process_responseData(data) {
        const selectedId = this.moving_mouse_obj?.id;
        this.packs = data.filter(pack => Number(pack.quantity) > 0).map(pack => ({...pack, quantity: Number(pack.quantity)}));
        this.render_inventory();
        this.set_state('ready');
        this.select_pack(this.packs.find(pack => pack.id === selectedId) || this.packs[0]);
    }
    render_inventory() {
        const fragment = document.createDocumentFragment();
        this.packs.forEach((pack, index) => {
            const button = this.node('button', 'pack-choice');
            button.dataset.pack = index;
            button.setAttribute('aria-label', pack.name + ', ' + pack.quantity + ' owned');
            button.setAttribute('aria-pressed', String(pack === this.moving_mouse_obj));
            const icon = this.node('span', 'pack-mini'); icon.setAttribute('aria-hidden', 'true');
            icon.append(this.node('img'));
            button.append(icon, this.node('span', 'pack-choice-name', pack.name), this.node('span', 'pack-quantity', '× ' + pack.quantity));
            this.artwork(button, pack);
            fragment.append(button);
        });
        this.ui['pack-list'].replaceChildren(fragment);
        this.ui['pack-total'].textContent = this.packs.reduce((total, pack) => total + pack.quantity, 0);
        this.ui['inventory-message'].hidden = this.packs.length > 0;
        this.ui['inventory-message'].textContent = 'No unopened packs.';
        this.ui['empty-shop'].hidden = this.packs.length > 0;
    }
    select_pack(pack) {
        if (this.state !== 'ready') return false;
        this.moving_mouse_obj = pack || null;
        this.ui['pack-focus'].hidden = !pack;
        this.ui['pack-title'].textContent = pack ? pack.name + ' Pack' : 'Choose a Pack';
        this.ui['pack-owned'].textContent = pack ? pack.quantity + ' owned' : '';
        this.ui['opening-status'].textContent = pack ? '' : 'Visit the shop to get a pack.';
        this.ui['open-pack'].disabled = !pack;
        this.ui['pack-list'].querySelectorAll('[data-pack]').forEach(button => {
            button.setAttribute('aria-pressed', String(this.packs[Number(button.dataset.pack)] === pack));
        });
        if (pack) this.artwork(this.ui['pack-focus'], pack);
        this.ui['rotate-pack'].hidden = !pack || !this.scene;
        this.invalidate?.();
        return Boolean(pack);
    }
    async open_pack(pack = this.moving_mouse_obj) {
        if (this.state !== 'ready' || !pack || pack.quantity < 1) return;
        this.moving_mouse_obj = pack;
        this.ui['draw-notice'].hidden = true;
        this.phase = 0;
        this.set_state('requesting');
        this.ui['opening-status'].textContent = 'Opening pack…';
        try {
            await this.send_pack_detail();
            // Only a confirmed response consumes the displayed pack. Never retry a roll.
            pack.quantity -= 1;
            this.packs = this.packs.filter(item => item.quantity > 0);
            this.render_inventory();
            this.ui['pack-owned'].textContent = pack.quantity + ' remaining';
            this.phase = 0;
            this.set_state('opening');
            this.position_cards();
            this.ui['opening-status'].textContent = 'Breaking the seal…';
            if (this.reduced) this.finish_opening();
        } catch (_) {
            this.card_in_pack = []; this.card_show = [];
            this.set_state('error');
            await this.send_packs_request();
            this.notify('Opening could not be confirmed. Check your collection before opening another pack.');
        }
    }
    async send_pack_detail() {
        const pack = this.moving_mouse_obj;
        const data = await this.post('/send_pack', {id: pack.id, name: pack.name, name_id: pack.name_id});
        this.process_response_cards(data);
    }
    process_response_cards(data) {
        if (data.some(card => !card || typeof card.Name !== 'string')) throw new Error('Invalid card data.');
        this.clear_faces();
        this.card_in_pack = data;
        this.card_show = [];
        const fragment = document.createDocumentFragment();
        data.forEach((card, index) => {
            const button = this.node('button', 'reveal-card');
            button.disabled = true;
            button.dataset.rarity = String(card.Rarity || 'Common').toLowerCase().replace(/[\s_]+/g, '-');
            button.dataset.color = String(card.Background_url || '').trim();
            button.setAttribute('aria-label', 'Reveal card ' + (index + 1));
            button.style.setProperty('--arrival', (.9 + index * .09) + 's');
            const inner = this.node('span', 'card-inner');
            const back = this.image('webpages/image_source/card/back.png?v=compass', 'card-back');
            const front = this.node('span', 'card-front'); front.setAttribute('aria-hidden', 'true');
            const foot = this.node('span', 'card-foot');
            foot.append(this.node('span', 'rarity-mark', String(card.Rarity || '').replaceAll('_', ' ')), this.node('span', '', card.Cost || ''),
                this.node('span', '', card.Power != null ? card.Power + ' / ' + card.Toughness : ''));
            front.append(this.node('span', 'card-name', card.Name), this.image(card.Image_url, 'card-art'),
                this.node('span', 'card-type', card.Type_card), this.node('span', 'card-ability', card.Ability), foot);
            inner.append(back, front); button.append(inner);
            button.addEventListener('click', () => {
                if (this.card_show.includes(index)) this.show_detail(card);
                else this.draw_a_card(index);
            });
            fragment.append(button);
        });
        this.ui['draw-results'].replaceChildren(fragment);
        this.ui['draw-results'].style.setProperty('--card-count', Math.max(1, Math.min(data.length, 6)));
        this.ui['draw-results'].style.setProperty('--tablet-count', Math.max(1, Math.min(data.length, 3)));
        this.ui['draw-results'].style.setProperty('--phone-count', Math.max(1, Math.min(data.length, 2)));
        data.forEach((card, index) => {
            try { this.original_face(card, index); }
            catch (_) { /* A presentation failure must not invalidate a confirmed roll. */ }
        });
    }
    clear_faces() {
        this.face_observers.forEach(observer => observer.disconnect());
        this.face_observers.clear();
        this.card_faces = [];
    }
    original_face(card, index) {
        const front = this.ui['draw-results'].children[index].querySelector('.card-front');
        const surfaces = this.frame_generator.generate_card(
            card.Background_url || 'colorless', card.Name, card.Type_card || '',
            card.Rarity || 'Common', card.Ability || '', card.Image_url
        );
        const args = [4, 5.62, [0, 0, 40], 3, surfaces];
        let original;
        if (card.Type_card === 'land') original = new Land(...args, card.Name);
        else if (card.Type_card === 'Instant') original = new Instant(...args, card.Cost || '0', card.Name);
        else if (card.Type_card === 'sorcery') original = new Sorcery(...args, card.Cost || '0', card.Name);
        else original = new Creature(...args, card.Cost || '0', card.Toughness, card.Power, card.Name);

        // The legacy renderer sizes its canvas after its images load, but exposes no promise.
        // Observe that completion locally instead of changing shared rendering or polling.
        const observer = new MutationObserver(async () => {
            observer.disconnect(); this.face_observers.delete(observer);
            try {
                await Promise.all(original.images_fee.map(image => image.decode()));
                if (!front.isConnected || this.card_in_pack[index] !== card) return;
                original.update();
                const face = surfaces[0];
                face.className = 'original-card-face';
                face.setAttribute('role', 'img');
                face.setAttribute('aria-label', [card.Name, card.Type_card, card.Cost, card.Ability].filter(Boolean).join('. '));
                front.replaceChildren(face);
                front.classList.add('original-face');
                this.card_faces[index] = face;
            } catch (_) {
                // Keep the accessible metadata if an original card asset is unavailable.
            }
        });
        observer.observe(surfaces[2], {attributes: true, attributeFilter: ['width', 'height']});
        this.face_observers.add(observer);
    }
    position_cards() {
        this.scene?.layoutCards();
    }
    finish_opening() {
        if (this.state !== 'opening') return;
        this.set_state(this.card_in_pack.length ? 'reveal' : 'complete');
        this.ui['draw-results'].querySelectorAll('button').forEach(button => button.disabled = false);
        this.ui['opening-status'].textContent = this.card_in_pack.length ? '0 / ' + this.card_in_pack.length + ' revealed · Select a card' : 'No cards were returned. Check your collection.';
        if (!document.hidden && document.hasFocus()) {
            (this.ui['draw-results'].querySelector('button') || this.ui['open-another']).focus({preventScroll: true});
        }
    }
    draw_a_card(index = this.card_in_pack.findIndex((_, i) => !this.card_show.includes(i))) {
        if (this.state !== 'reveal' || !this.card_in_pack[index] || this.card_show.includes(index)) return;
        this.card_show.push(index);
        const button = this.ui['draw-results'].children[index];
        button.classList.add('is-revealed');
        this.scene?.reveal(index, this.card_in_pack[index].Rarity);
        button.setAttribute('aria-label', this.card_in_pack[index].Name + '. View card details');
        button.querySelector('.card-front').setAttribute('aria-hidden', 'false');
        if (this.card_show.length === this.card_in_pack.length) {
            const revealAllFocused = document.activeElement === this.ui['reveal-all'];
            this.set_state('complete');
            if (revealAllFocused) this.ui['open-another'].focus({preventScroll: true});
        }
        this.ui['opening-status'].textContent = this.card_show.length + ' / ' + this.card_in_pack.length + ' revealed';
        this.invalidate?.();
    }
    show_detail(card) {
        const image = this.ui['detail-image'];
        image.hidden = false; image.onerror = () => image.hidden = true;
        const face = this.card_faces[this.card_in_pack.indexOf(card)];
        image.classList.toggle('original-face', Boolean(face));
        image.src = face ? face.toDataURL() : '/' + String(card.Image_url || '').replace(/^\/+/, '');
        this.ui['detail-name'].textContent = card.Name;
        this.ui['detail-rarity'].textContent = String(card.Rarity || '').replaceAll('_', ' ');
        this.ui['detail-type'].textContent = card.Type_card;
        this.ui['detail-cost'].textContent = card.Cost ? 'Mana cost: ' + card.Cost : '';
        this.ui['detail-ability'].textContent = card.Ability || '';
        this.ui['detail-stats'].textContent = card.Power != null ? 'Power / Toughness: ' + card.Power + ' / ' + card.Toughness : '';
        this.ui['card-detail'].showModal();
    }
    reset() {
        if (this.state !== 'complete') return;
        this.clear_faces();
        this.card_show = []; this.card_in_pack = [];
        this.ui['draw-results'].replaceChildren();
        this.set_state('ready');
        this.select_pack(this.packs.find(pack => pack === this.moving_mouse_obj) || this.packs[0]);
        (this.moving_mouse_obj ? this.ui['open-pack'] : this.ui['empty-shop']).focus({preventScroll: true});
    }
    update(dt) {
        if (this.state !== 'opening') return;
        this.phase += dt;
        const message = this.phase < 1.3 ? 'Breaking the seal…' : this.phase < 3 ? 'Opening the pack…' : 'Drawing your cards…';
        if (this.ui['opening-status'].textContent !== message) this.ui['opening-status'].textContent = message;
        if (this.phase >= 6.6 || this.reduced) this.finish_opening();
    }
}
