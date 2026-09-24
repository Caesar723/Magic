(() => {
    const ui = Object.fromEntries([...document.querySelectorAll('[id]')].map(element => [element.id, element]));
    const motion = matchMedia('(prefers-reduced-motion: reduce)');
    const queue = [];
    let current = null, batchPromise = null;
    let reduced = false;
    try {
        const saved = localStorage.getItem('login-reduced-motion');
        reduced = saved === null ? localStorage.getItem('lobby-reduced-motion') === 'true' : saved === 'true';
    } catch (_) {}


    let scene, frame = 0, lastTime = 0, time = 0, reveal = null, changing = false;
    let disposed = false, inView = true, paused = document.hidden || !document.hasFocus();
    const isReduced = () => reduced || motion.matches;
    function galleryControls() {
        ui.steleNext.disabled = !current && changing;
        ui.steleNext.setAttribute('aria-disabled', String(changing));
        ui.steleStage.setAttribute('aria-busy', String(changing));
    }
    function fitInscription() {
        let size = 20;
        ui.stoneStory.style.fontSize = size + 'px';
        while (size > 14 && ui.stoneStory.offsetHeight > ui.stoneStory.parentElement.clientHeight - 3) ui.stoneStory.style.fontSize = --size + 'px';
    }
    function commit(card) {
        current = card;
        ui.stoneImage.src = card.image.src;
        ui.stoneStory.textContent = card.story || 'No inscription is available for this card.';
        fitInscription();
        if (queue.length <= 2) preloadBatch().catch(() => {});
    }
    async function decodeCard(card) {
        const image = new Image(); image.src = card.url;
        let timeout;
        try {
            await Promise.race([image.decode(), new Promise((_, reject) => { timeout = setTimeout(() => reject(new Error('Image timed out.')), 20000); })]);
            return {...card, image};
        } finally { clearTimeout(timeout); }
    }
    function preloadBatch() {
        if (batchPromise) return batchPromise;
        batchPromise = (async () => {
            const response = await fetch('/login/cards_show', {method: 'POST', signal: AbortSignal.timeout(20000)});
            if (!response.ok) throw new Error('Request failed.');
            const {image_url: urls, image_story: stories} = await response.json();
            if (!Array.isArray(urls) || !urls.length || !Array.isArray(stories)) throw new Error('No cards.');
            const loaded = await Promise.allSettled(urls.slice(0, 5).map((url, index) => decodeCard({
                url: '/get-images/' + encodeURIComponent(url), story: typeof stories[index] === 'string' ? stories[index] : ''
            })));
            const cards = loaded.filter(result => result.status === 'fulfilled').map(result => result.value);
            if (!cards.length) throw new Error('No carvings could be loaded.');
            if (!disposed) queue.push(...cards);
        })().finally(() => { batchPromise = null; });
        return batchPromise;
    }
    async function showNext(initial = false) {
        if (changing || disposed) return;
        changing = true; galleryControls(); ui.retryCards.hidden = true;
        if (!queue.length) ui.galleryStatus.textContent = 'Loading carving…';
        try {
            if (!queue.length) await preloadBatch();
            if (disposed) return;
            const card = queue.shift();
            ui.galleryStatus.textContent = '';
            if (initial || isReduced()) {
                commit(card); changing = false; galleryControls();
            } else {
                reveal = {elapsed: 0, card, committed: false};
                ui.steleStage.dataset.revealing = 'true'; requestFrame();
            }
        } catch (_) {
            if (disposed) return;
            changing = false; galleryControls();
            ui.galleryStatus.textContent = 'This carving could not be loaded. Please try again.';
            ui.retryCards.hidden = false;
        }
    }
    ui.steleNext.addEventListener('click', () => showNext(!current));
    ui.retryCards.addEventListener('click', () => showNext(!current));
    function finishReveal() {
        if (reveal && !reveal.committed) commit(reveal.card);
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
            if (elapsed >= .5 && !reveal.committed) { commit(reveal.card); reveal.committed = true; }
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
        if (!event.persisted) { disposed = true; resize.disconnect(); visibility.disconnect(); scene?.dispose(); queue.length = 0; current = null; }
    });
    window.addEventListener('pageshow', () => pauseMotion());
    applyMotion(); pauseMotion();
    const initialCards = showNext(true);
    window.PageTransition?.wait(initialCards);
    const sceneReady = import('./login-scene.js').then(({LoginScene}) => {
        if (disposed) return;
        scene = new LoginScene(ui.steleCanvas, ui.steleStage, ui.stelePlane, fallback);
        scene.resize(); scene.render(0, 0, isReduced());
        ui.steleStage.dataset.renderer = 'three'; requestFrame();
    }).catch(fallback);
    window.PageTransition?.wait(sceneReady);
})();
