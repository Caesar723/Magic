(() => {
    const ui = Object.fromEntries([...document.querySelectorAll('[id]')].map(element => [element.id, element]));
    const motion = matchMedia('(prefers-reduced-motion: reduce)');
    let cards = [], cardIndex = 0;
    let reduced = false;
    try {
        const saved = localStorage.getItem('login-reduced-motion');
        reduced = saved === null ? localStorage.getItem('lobby-reduced-motion') === 'true' : saved === 'true';
    } catch (_) {}


    let scene, frame = 0, lastTime = 0, time = 0, reveal = null, changing = false, pendingIndex = 0;
    let disposed = false, inView = true, paused = document.hidden || !document.hasFocus();
    const images = new Map();
    const isReduced = () => reduced || motion.matches;
    function galleryControls() {
        const blocked = changing || cards.length < 2;
        for (const button of [ui.steleNext, ui.previousCard, ui.nextCard]) {
            button.disabled = cards.length < 2;
            button.setAttribute('aria-disabled', String(blocked));
        }
        ui.steleStage.setAttribute('aria-busy', String(changing));
    }
    function fitInscription() {
        let size = 20;
        ui.stoneStory.style.fontSize = size + 'px';
        while (size > 14 && ui.stoneStory.offsetHeight > ui.stoneStory.parentElement.clientHeight - 3) ui.stoneStory.style.fontSize = --size + 'px';
    }
    function commit(card, image, index) {
        cardIndex = index;
        ui.stoneImage.src = image.src;
        ui.stoneStory.textContent = card.story || 'No inscription is available for this card.';
        ui.cardCount.textContent = `${String(index + 1).padStart(2, '0')} / ${String(cards.length).padStart(2, '0')}`;
        fitInscription();
    }
    function loadImage(card) {
        if (!images.has(card.url)) {
            const image = new Image(); image.src = card.url;
            const promise = image.decode().then(() => image).catch(error => { images.delete(card.url); throw error; });
            images.set(card.url, promise);
        }
        return images.get(card.url);
    }
    async function showCard(index, initial = false) {
        if (changing || !cards.length || disposed) return;
        pendingIndex = (index + cards.length) % cards.length;
        const card = cards[pendingIndex];
        changing = true; galleryControls(); ui.retryCards.hidden = true; ui.galleryStatus.textContent = 'Loading carving…';
        try {
            const image = await loadImage(card);
            if (disposed) return;
            ui.galleryStatus.textContent = '';
            if (initial || isReduced()) {
                commit(card, image, pendingIndex); changing = false; galleryControls();
            } else {
                reveal = {elapsed: 0, card, image, index: pendingIndex, committed: false};
                ui.steleStage.dataset.revealing = 'true'; requestFrame();
            }
        } catch (_) {
            if (disposed) return;
            changing = false; galleryControls();
            ui.galleryStatus.textContent = 'This carving could not be loaded. Please try again.';
            ui.retryCards.hidden = false;
        }
    }
    async function loadCarousel() {
        if (changing || disposed) return;
        changing = true; galleryControls(); ui.retryCards.hidden = true; ui.galleryStatus.textContent = 'Loading carvings…';
        try {
            const response = await fetch('/login/cards_show', {method: 'POST', signal: AbortSignal.timeout(20000)});
            if (!response.ok) throw new Error('Request failed.');
            const {image_url: urls, image_story: stories} = await response.json();
            if (disposed) return;
            if (!Array.isArray(urls) || !urls.length || !Array.isArray(stories)) throw new Error('No cards.');
            cards = urls.map((url, index) => ({url: '/get-images/' + encodeURIComponent(url), story: typeof stories[index] === 'string' ? stories[index] : ''}));
            changing = false; await showCard(0, true);
        } catch (_) {
            if (disposed) return;
            changing = false; galleryControls();
            ui.galleryStatus.textContent = 'Carvings are unavailable. Please try again.';
            ui.retryCards.hidden = false;
        }
    }
    ui.steleNext.addEventListener('click', () => showCard(cardIndex + 1));
    ui.previousCard.addEventListener('click', () => showCard(cardIndex - 1));
    ui.nextCard.addEventListener('click', () => showCard(cardIndex + 1));
    ui.retryCards.addEventListener('click', () => cards.length ? showCard(pendingIndex, true) : loadCarousel());
    document.querySelector('.stele-showcase').addEventListener('keydown', event => {
        if (!['ArrowLeft', 'ArrowRight'].includes(event.key)) return;
        event.preventDefault(); showCard(cardIndex + (event.key === 'ArrowLeft' ? -1 : 1));
    });
    function finishReveal() {
        if (reveal && !reveal.committed) commit(reveal.card, reveal.image, reveal.index);
        reveal = null; changing = false; galleryControls();
        delete ui.steleStage.dataset.revealing;
        ui.steleFlash.style.opacity = ui.steleHalo.style.opacity = '0';
        ui.steleStage.style.setProperty('--flare', '0');
        for (const spark of ui.fallbackSparks.children) spark.style.opacity = '0';
    }
    function renderEffects(elapsed) {
        const ease = value => { const t = Math.max(0, Math.min(1, value)); return t * t * (3 - 2 * t); };
        const light = elapsed < .68 ? ease(elapsed / .42) : 1 - ease((elapsed - .68) / .87);
        ui.steleFlash.style.opacity = light; ui.steleHalo.style.opacity = light * .82;
        ui.steleStage.style.setProperty('--flare', light * .9);
        if (!scene) {
            const progress = Math.max(0, Math.min(1, (elapsed - .56) / 1.34));
            [...ui.fallbackSparks.children].forEach((spark, index) => {
                const angle = index * 2.39996, distance = progress * (100 + index % 5 * 25);
                spark.style.transform = `translate(${Math.cos(angle) * distance}px, ${Math.sin(angle) * distance - progress * progress * 20}px) rotate(${index * 37 + progress * 90}deg)`;
                spark.style.opacity = progress > 0 ? 1 - progress : 0;
            });
        }
    }
    function tick(stamp) {
        frame = 0;
        if (disposed || paused) return;
        const dt = lastTime ? Math.min((stamp - lastTime) / 1000, .05) : 0;
        lastTime = stamp; time += dt;
        let elapsed = -1;
        if (reveal) {
            reveal.elapsed += dt; elapsed = reveal.elapsed;
            renderEffects(elapsed);
            if (elapsed >= .5 && !reveal.committed) { commit(reveal.card, reveal.image, reveal.index); reveal.committed = true; }
            if (elapsed >= 1.9) finishReveal();
        }
        scene?.render(time, dt, isReduced(), elapsed);
        if (reveal || (scene && inView && !isReduced())) requestFrame();
        else lastTime = 0;
    }
    function requestFrame() { if (!frame && !disposed && !paused) frame = requestAnimationFrame(tick); }
    function applyMotion() {
        const off = isReduced();
        document.body.classList.toggle('motion-reduced', off);
        ui.motionToggle.textContent = off ? 'Motion: Off' : 'Motion: On';
        ui.motionToggle.setAttribute('aria-pressed', String(off)); ui.motionToggle.disabled = motion.matches;
        if (off && reveal) finishReveal();
        if (off) scene?.pointer.set(0, 0);
        requestFrame();
    }
    function pauseMotion(force) {
        paused = force === true || document.hidden || !document.hasFocus();
        document.body.classList.toggle('motion-paused', paused);
        if (paused) { cancelAnimationFrame(frame); frame = 0; lastTime = 0; scene?.pointer.set(0, 0); }
        else requestFrame();
    }
    for (let index = 0; index < 12; index++) {
        const mote = document.createElement('i'); mote.className = 'mote';
        mote.style.setProperty('--x', ((index * 37) % 100) + '%');
        mote.style.setProperty('--duration', (17 + index % 5 * 3) + 's');
        mote.style.setProperty('--delay', (-index * 3.7) + 's'); ui.motes.append(mote);
    }
    for (let index = 0; index < 24; index++) ui.fallbackSparks.append(document.createElement('i'));
    ui.steleStage.addEventListener('pointermove', event => {
        if (!scene || event.pointerType !== 'mouse' || isReduced() || paused) return;
        const box = ui.steleStage.getBoundingClientRect();
        scene.pointer.set((event.clientX - box.left) / box.width - .5, (event.clientY - box.top) / box.height - .5);
    });
    ui.steleStage.addEventListener('pointerleave', () => scene?.pointer.set(0, 0));
    ui.motionToggle.addEventListener('click', () => {
        reduced = !reduced;
        try { localStorage.setItem('login-reduced-motion', String(reduced)); } catch (_) {}
        applyMotion();
    });
    motion.addEventListener('change', applyMotion);
    document.addEventListener('visibilitychange', () => pauseMotion());
    window.addEventListener('blur', () => pauseMotion(true));
    window.addEventListener('focus', () => pauseMotion());
    const resize = new ResizeObserver(() => { scene?.resize(); fitInscription(); requestFrame(); });
    resize.observe(ui.steleStage);
    const visibility = new IntersectionObserver(entries => { inView = entries[0].isIntersecting; if (inView) requestFrame(); }, {rootMargin: '80px'});
    visibility.observe(ui.steleStage);
    function fallback() {
        scene?.dispose(); scene = null;
        ui.steleStage.dataset.renderer = 'fallback'; ui.stelePlane.style.removeProperty('transform');
        requestFrame();
    }
    window.addEventListener('pagehide', event => {
        pauseMotion(true);
        if (!event.persisted) { disposed = true; resize.disconnect(); visibility.disconnect(); scene?.dispose(); images.clear(); }
    });
    window.addEventListener('pageshow', () => pauseMotion());
    applyMotion(); pauseMotion(); loadCarousel();
    import('./login-scene.js').then(({LoginScene}) => {
        if (disposed) return;
        scene = new LoginScene(ui.steleCanvas, ui.steleStage, ui.stelePlane, fallback);
        scene.resize(); scene.render(0, 0, isReduced());
        ui.steleStage.dataset.renderer = 'three'; requestFrame();
    }).catch(fallback);
})();
