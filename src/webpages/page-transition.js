(() => {
    const root = document.documentElement, pending = new Set(), images = new Map();
    let overlay, status, actions, finished = false, leaving = false, slowTimer, closeTimer;
    const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
    const reduced = () => matchMedia('(prefers-reduced-motion: reduce)').matches || document.body?.classList.contains('motion-reduced');
    root.classList.add('page-booting');

    function wait(promise) {
        if (finished || !promise?.then) return promise;
        const task = Promise.resolve(promise).catch(() => {}).finally(() => pending.delete(task));
        pending.add(task);
        return promise;
    }
    function image(source) {
        if (finished) return Promise.resolve();
        const url = typeof source === 'string' ? new URL(source, document.baseURI).href : source.currentSrc || source.src;
        if (!url) return Promise.resolve();
        if (!images.has(url)) {
            const picture = typeof source === 'string' ? new Image() : source;
            if (typeof source === 'string') picture.src = url;
            const task = picture.decode().catch(() => {});
            images.set(url, task); wait(task);
        }
        return images.get(url);
    }
    function visible(element) {
        const rect = element.getBoundingClientRect();
        return rect.width > 0 && rect.height > 0 && rect.bottom >= 0 && rect.top <= innerHeight && rect.right >= 0 && rect.left <= innerWidth;
    }
    function collectArtwork() {
        for (const picture of document.images) {
            if (picture.closest('#page-loader') || (!visible(picture) && picture.loading === 'lazy')) continue;
            if (picture.loading === 'lazy') picture.loading = 'eager';
            image(picture);
        }
        for (const element of [root, document.body, ...document.body.querySelectorAll('*')]) {
            if (element.closest('#page-loader') || !visible(element)) continue;
            if (element.tagName.toLowerCase() === 'image') {
                const href = element.getAttribute('href') || element.getAttribute('xlink:href');
                if (href && !href.startsWith('#')) image(href);
            }
            for (const pseudo of [null, '::before', '::after']) {
                const style = getComputedStyle(element, pseudo);
                for (const match of style.backgroundImage.matchAll(/url\((?:"([^"]*)"|'([^']*)'|([^)]*))\)/g)) image(match[1] || match[2] || match[3]);
            }
        }
    }
    function mount() {
        if (overlay) return;
        overlay = document.createElement('dialog'); overlay.id = 'page-loader';
        overlay.setAttribute('aria-label', 'Loading page');
        overlay.innerHTML = '<div class="page-loader-mark" aria-hidden="true"><svg viewBox="0 0 48 48"><circle cx="24" cy="24" r="16"/><path d="m24 3 5 16 16 5-16 5-5 16-5-16L3 24l16-5Z"/></svg></div><p role="status" aria-live="polite">Loading…</p><div class="page-loader-actions" hidden><button type="button" data-continue>Continue</button><button type="button" data-reload>Reload</button></div>';
        status = overlay.querySelector('p'); actions = overlay.querySelector('.page-loader-actions');
        overlay.addEventListener('cancel', event => event.preventDefault());
        overlay.querySelector('[data-continue]').addEventListener('click', reveal);
        overlay.querySelector('[data-reload]').addEventListener('click', () => location.reload());
        document.body.append(overlay);
    }
    function show() {
        mount(); clearTimeout(closeTimer); clearTimeout(slowTimer);
        overlay.dataset.clear = 'false'; actions.hidden = true; status.textContent = 'Loading…';
        if (!overlay.open) overlay.showModal();
        root.classList.remove('page-booting');
        slowTimer = setTimeout(() => { status.textContent = 'Taking longer than usual…'; actions.hidden = false; }, 12000);
    }
    function reveal() {
        finished = true; leaving = false; clearTimeout(slowTimer);
        root.classList.remove('page-booting');
        if (!overlay) return;
        overlay.dataset.clear = 'true';
        closeTimer = setTimeout(() => { overlay.close(); images.clear(); }, reduced() ? 0 : 400);
    }
    async function ready() {
        show();
        wait(document.fonts?.ready);
        // Page owners register their first data/scene render; only visible lazy art is decoded.
        while (!finished) {
            await Promise.all([...pending]);
            const count = images.size; collectArtwork();
            await Promise.all([...pending]);
            await delay(60);
            collectArtwork();
            if (!pending.size && count === images.size) break;
        }
        if (!finished) reveal();
    }
    async function navigate(path) {
        if (leaving) return;
        leaving = true; show();
        // Cover the old page before starting the next document's request.
        if (!reduced()) {
            overlay.animate([{opacity: 0}, {opacity: 1}], {duration: 220});
            await delay(220);
        }
        location.assign(path);
    }
    window.PageTransition = {wait, image, navigate};
    document.addEventListener('click', event => {
        const anchor = event.target.closest?.('a[href]');
        if (!anchor || event.defaultPrevented || event.button || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || anchor.hasAttribute('download') || (anchor.target && anchor.target !== '_self')) return;
        const url = new URL(anchor.href, location.href);
        if (url.origin !== location.origin || !['http:', 'https:'].includes(url.protocol) || (url.pathname === location.pathname && url.search === location.search)) return;
        event.preventDefault(); navigate(url.href);
    });
    const pause = (force = false) => overlay?.classList.toggle('page-loader-paused', force === true || document.hidden || !document.hasFocus());
    document.addEventListener('visibilitychange', () => pause());
    window.addEventListener('blur', () => pause(true)); window.addEventListener('focus', () => pause());
    window.addEventListener('pageshow', event => { if (event.persisted) reveal(); });
    document.addEventListener('DOMContentLoaded', () => { ready().catch(reveal); pause(); }, {once: true});
})();
