class Shelf {
    constructor() {
        this.ui = Object.fromEntries([...document.querySelectorAll('[id]')].map(element => [element.id, element]));
        this.all_items = [];
        this.selected = null;
        this.balance = null;
        this.currencyRequest = 0;
        this.busy = false;
        this.reduced = false;
        this.purchaseState = 'review';
        this.ui.shop_list.addEventListener('click', event => {
            const button = event.target.closest('[data-item-id]');
            if (button) this.select(this.all_items.find(item => String(item.id) === button.dataset.itemId));
        });
        this.ui['buy-pack'].addEventListener('click', () => this.buy());
        this.ui['retry-shop'].addEventListener('click', () => this.send_request());
        for (const id of ['refresh-balance', 'retry-balance']) this.ui[id].addEventListener('click', () => this.get_currency());
        for (const id of ['close-purchase', 'cancel-purchase', 'continue-shopping']) this.ui[id].addEventListener('click', () => this.close_purchase());
        this.ui['confirm-purchase'].addEventListener('click', () => this.confirm_purchase());
        this.ui['purchase-dialog'].addEventListener('cancel', event => { if (this.busy) event.preventDefault(); });
        this.ui['purchase-dialog'].addEventListener('close', () => { this.activeItem = null; this.ui['buy-pack'].focus({preventScroll: true}); });
        this.ui['purchase-dialog'].addEventListener('click', event => {
            if (event.target !== this.ui['purchase-dialog']) return;
            const box = this.ui['purchase-dialog'].getBoundingClientRect();
            if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) this.close_purchase();
        });
        this.ui['rotate-pack'].addEventListener('click', () => this.scene?.rotate());
    }
    async post(path, body) {
        const options = {method: 'POST', signal: AbortSignal.timeout(20000)};
        if (body !== undefined) { options.headers = {'Content-Type': 'application/json'}; options.body = JSON.stringify(body); }
        const response = await fetch(path, options);
        if (!response.ok || response.redirected) throw new Error('Request could not be confirmed.');
        const data = await response.json();
        return typeof data === 'string' ? JSON.parse(data) : data;
    }
    async send_request() {
        if (this.loading || this.busy) return;
        this.loading = true;
        this.ui.shop_list.setAttribute('aria-busy', 'true');
        this.ui['catalog-message'].hidden = false;
        this.ui['catalog-message'].textContent = 'Loading packs…';
        this.ui['retry-shop'].hidden = true;
        try {
            const data = await this.post('/shop/items');
            if (!Array.isArray(data) || data.some(item => typeof item.name !== 'string' || !Number.isFinite(item.price) || item.price < 0 || !Number.isFinite(item.id))) throw new Error('Invalid catalog.');
            this.create_list(data);
        } catch (_) {
            this.ui['catalog-message'].textContent = 'Unable to load the shop. Please try again.';
            this.ui['retry-shop'].hidden = false;
        } finally {
            this.loading = false;
            this.ui.shop_list.setAttribute('aria-busy', 'false');
        }
    }
    create_list(data) {
        const selectedId = this.selected?.id;
        this.all_items = data.map(item => new Item(item.name, item.price, item.pack_url, item.id));
        const rows = document.createDocumentFragment();
        for (let index = 0; index < this.all_items.length; index += 4) {
            const row = Item.node('div', 'shop_line');
            row.append(...this.all_items.slice(index, index + 4).map(item => item.element));
            rows.append(row);
        }
        this.ui.shop_list.replaceChildren(rows);
        this.ui['catalog-count'].textContent = data.length ? String(data.length).padStart(2, '0') : '';
        this.ui['catalog-message'].hidden = data.length > 0;
        this.ui['catalog-message'].textContent = 'No packs are available right now.';
        this.select(this.all_items.find(item => item.id === selectedId) || this.all_items[0]);
    }
    select(item) {
        if (this.busy) return;
        this.selected = item || null;
        this.all_items.forEach(entry => entry.element.setAttribute('aria-pressed', String(entry === item)));
        this.ui['selected-art'].hidden = !item;
        this.ui['selected-name'].textContent = item ? item.name + ' Pack' : 'Choose a Pack';
        this.ui['purchase-pack-name'].textContent = item ? item.name + ' Pack' : 'Choose a Pack';
        this.ui['selected-price'].querySelector('span:last-of-type').textContent = item ? item.price : '—';
        if (item) item.apply_art(this.ui['selected-art']);
        this.ui['buy-pack'].disabled = !item;
        this.ui['rotate-pack'].hidden = !item || !this.scene;
        this.update_balance();
        this.scene?.select(item);
    }
    async get_currency() {
        if (this.busy) return;
        const request = ++this.currencyRequest;
        this.ui['refresh-balance'].disabled = true;
        this.ui['retry-balance'].disabled = true;
        try {
            const data = await this.post('/get_currency');
            if (!Number.isFinite(data.currency) || data.currency < 0) throw new Error('Invalid balance.');
            if (request !== this.currencyRequest) return;
            this.balance = data.currency;
        } catch (_) {
            if (request === this.currencyRequest) this.balance = null;
        } finally {
            if (request === this.currencyRequest) {
                this.ui['refresh-balance'].disabled = false;
                this.ui['retry-balance'].disabled = false;
                this.update_balance();
            }
        }
    }
    update_balance() {
        this.ui.currency.querySelector('.button-text').textContent = this.balance == null ? '—' : this.balance.toLocaleString('en-US');
        const shortfall = this.selected && this.balance != null ? this.selected.price - this.balance : 0;
        this.ui['balance-message'].textContent = this.balance == null ? 'Balance unavailable. Refresh your coins to purchase.' : shortfall > 0 ? 'You need ' + shortfall.toLocaleString('en-US') + ' more coins.' : '';
        const item = this.activeItem;
        if (!item || ['success', 'uncertain'].includes(this.purchaseState)) return;
        this.ui['purchase-balance'].textContent = this.balance == null ? '—' : this.balance.toLocaleString('en-US');
        this.ui['purchase-remaining'].textContent = this.balance == null ? '—' : Math.max(0, this.balance - item.price).toLocaleString('en-US');
        const affordable = this.balance != null && this.balance >= item.price;
        this.ui['confirm-purchase'].disabled = this.busy || !affordable;
        this.ui['retry-balance'].hidden = affordable || this.busy;
        if (!this.busy && this.purchaseState !== 'error') {
            this.ui['purchase-status'].textContent = this.balance == null ? 'Refresh your balance to continue.' : !affordable ? 'Not enough coins for this pack.' : '';
        }
    }
    buy() {
        if (!this.selected || this.busy || this.ui['purchase-dialog'].open) return;
        this.activeItem = this.selected;
        this.purchaseState = 'review';
        this.ui['purchase-dialog'].dataset.state = 'review';
        this.activeItem.apply_art(this.ui['purchase-art']);
        this.ui['purchase-title'].textContent = 'Confirm Purchase';
        this.ui['purchase-name'].textContent = this.activeItem.name + ' Pack';
        this.ui['purchase-price'].textContent = this.activeItem.price.toLocaleString('en-US') + ' coins';
        this.ui['purchase-actions'].hidden = false;
        this.ui['purchase-result'].hidden = true;
        this.ui['purchase-status'].textContent = '';
        this.set_busy(false);
        this.update_balance();
        this.ui['purchase-dialog'].showModal();
        this.ui['cancel-purchase'].focus();
    }
    close_purchase() {
        if (!this.busy) this.ui['purchase-dialog'].close();
    }
    set_busy(busy) {
        this.busy = busy;
        for (const id of ['confirm-purchase', 'close-purchase', 'cancel-purchase', 'refresh-balance', 'retry-balance']) this.ui[id].disabled = busy;
        this.ui['purchase-dialog'].setAttribute('aria-busy', String(busy));
        this.ui['confirm-purchase'].textContent = busy ? 'Purchasing…' : 'Confirm Purchase';
        this.ui['retry-balance'].hidden = busy;
    }
    async confirm_purchase() {
        const item = this.activeItem;
        if (this.busy || !item || !['review', 'error'].includes(this.purchaseState) || this.balance == null || this.balance < item.price) return;
        ++this.currencyRequest; // Ignore balance reads started before this purchase.
        this.set_busy(true);
        this.purchaseState = 'pending';
        this.ui['purchase-dialog'].dataset.state = 'pending';
        this.ui['purchase-status'].textContent = 'Purchasing your pack…';
        let refresh = false;
        try {
            const data = await this.post('/shop/buy', {id: item.id, name: item.name, name_id: -1});
            if (data.status === 200) {
                this.purchaseState = 'success';
                this.balance = Number.isFinite(data.currency) && data.currency >= 0 ? data.currency : null;
                refresh = this.balance == null;
                this.ui['purchase-title'].textContent = 'Pack Purchased';
                this.ui['purchase-status'].textContent = item.name + ' Pack was added to Your Packs.';
                this.ui['purchase-actions'].hidden = true;
                this.ui['purchase-result'].hidden = false;
                this.ui['purchase-remaining'].textContent = this.balance == null ? '—' : this.balance.toLocaleString('en-US');
                this.scene?.celebrate();
                this.ui.currency.classList.remove('coins-updated');
                void this.ui.currency.offsetWidth;
                this.ui.currency.classList.add('coins-updated');
            } else if (data.status === 400 && typeof data.message === 'string') {
                this.purchaseState = 'error';
                this.ui['purchase-status'].textContent = data.message === 'Not enough currency' ? 'Not enough coins for this pack.' : data.message;
                refresh = true;
            } else throw new Error('Unrecognized purchase result.');
        } catch (_) {
            this.purchaseState = 'uncertain';
            this.balance = null;
            this.ui['purchase-title'].textContent = 'Check Your Packs';
            this.ui['purchase-status'].textContent = 'The purchase could not be confirmed. Check Your Packs before trying again.';
            this.ui['purchase-actions'].hidden = true;
            this.ui['purchase-result'].hidden = false;
            this.ui['purchase-remaining'].textContent = '—';
            refresh = true;
        } finally {
            this.set_busy(false);
            this.ui['purchase-dialog'].dataset.state = this.purchaseState;
            this.update_balance();
            this.ui['retry-balance'].hidden = ['success', 'uncertain'].includes(this.purchaseState);
            if (['success', 'uncertain'].includes(this.purchaseState)) this.ui['open-packs'].focus();
            // A failed response may already have charged coins; never resend /shop/buy.
            if (refresh) await this.get_currency();
        }
    }
}

const shelf = new Shelf();
shelf.send_request();
shelf.get_currency();

// Rendering stays optional; navigation, selection and purchasing are HTML controls.
const shopMotion = matchMedia('(prefers-reduced-motion: reduce)');
let shopScene, shopFrame = 0, shopLast = 0, shopTime = 0, shopDisposed = false;
let shopFocused = document.hasFocus(), shopHidden = document.hidden;
function renderShop(dt = 0) {
    if (!shopDisposed && !shopHidden && shopFocused) shopScene?.render(shopTime, dt, shelf.reduced);
}
function stopShop() {
    cancelAnimationFrame(shopFrame); shopFrame = 0; shopLast = 0;
    shelf.ui['shop-stage'].dataset.animating = 'false';
}
function tickShop(now) {
    shopFrame = 0;
    if (shopDisposed || shopHidden || !shopFocused || shelf.reduced || !shopScene) return;
    if (!shopLast || now - shopLast >= 32) {
        const dt = shopLast ? Math.min((now - shopLast) / 1000, .06) : 0;
        shopLast = now; shopTime += dt; renderShop(dt);
    }
    shopFrame = requestAnimationFrame(tickShop);
}
function resumeShop() {
    document.body.classList.toggle('motion-paused', shopHidden || !shopFocused);
    if (shopDisposed || shopHidden || !shopFocused || shelf.reduced || !shopScene) { stopShop(); renderShop(); }
    else if (!shopFrame) { shelf.ui['shop-stage'].dataset.animating = 'true'; shopFrame = requestAnimationFrame(tickShop); }
}
function shopPreference() {
    let stored = false;
    try { stored = localStorage.getItem('lobby-reduced-motion') === 'true'; } catch (_) {}
    shelf.reduced = shopMotion.matches || stored;
    document.body.classList.toggle('motion-reduced', shelf.reduced);
    resumeShop();
}
function shopFallback() {
    stopShop(); shopScene?.dispose(); shopScene = shelf.scene = null;
    shelf.ui['shop-stage'].dataset.renderer = 'fallback';
    shelf.ui['rotate-pack'].hidden = true;
}
const shopObserver = new ResizeObserver(() => { shopScene?.resize(); renderShop(); });
shopObserver.observe(shelf.ui['shop-stage']);
shopMotion.addEventListener('change', shopPreference);
window.addEventListener('storage', event => { if (event.key === 'lobby-reduced-motion') shopPreference(); });
window.addEventListener('blur', () => { shopFocused = false; resumeShop(); });
window.addEventListener('focus', () => { shopFocused = true; resumeShop(); });
document.addEventListener('visibilitychange', () => { shopHidden = document.hidden; resumeShop(); });
window.addEventListener('pagehide', event => {
    shopHidden = true; resumeShop();
    if (!event.persisted) { shopDisposed = true; shopObserver.disconnect(); shopScene?.dispose(); }
});
window.addEventListener('pageshow', event => {
    shopHidden = document.hidden; shopFocused = document.hasFocus(); resumeShop();
    if (event.persisted) shelf.get_currency();
});
shopPreference();
import('./shop-scene.js').then(({ShopScene}) => {
    if (shopDisposed) return;
    shopScene = new ShopScene(shelf.ui['shop-canvas'], shelf.ui['shop-stage'], renderShop, shopFallback);
    shelf.scene = shopScene;
    shopScene.resize(); shopScene.select(shelf.selected);
    shelf.ui['shop-stage'].dataset.renderer = 'three';
    shelf.ui['rotate-pack'].hidden = !shelf.selected;
    resumeShop();
}).catch(shopFallback);
