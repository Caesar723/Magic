if ('serviceWorker' in navigator) navigator.serviceWorker.register('/webpages/service-worker.js').catch(() => {});

const deck = new Deck();
const book = new Book(deck);
const deckMotion = matchMedia('(prefers-reduced-motion: reduce)');
function applyDeckMotion() {
    let stored = false;
    try { stored = localStorage.getItem('lobby-reduced-motion') === 'true'; } catch (_) {}
    const reduced = deckMotion.matches || stored;
    document.body.classList.toggle('motion-reduced', reduced);
    if (reduced) book.pause();
}
function pauseDeckMotion() {
    const paused = document.hidden || !document.hasFocus();
    document.body.classList.toggle('motion-paused', paused);
    if (paused) book.pause();
}
deckMotion.addEventListener('change', applyDeckMotion);
window.addEventListener('storage', event => { if (event.key === 'lobby-reduced-motion') applyDeckMotion(); });
for (const type of ['focus', 'blur']) window.addEventListener(type, pauseDeckMotion);
document.addEventListener('visibilitychange', pauseDeckMotion);
window.addEventListener('pagehide', event => { book.pause(); if (!event.persisted) book.dispose(); });
window.addEventListener('pageshow', () => { applyDeckMotion(); pauseDeckMotion(); });
const motes = document.createDocumentFragment();
for (let i = 0; i < 10; i++) {
    const mote = document.createElement('span'); mote.className = 'mote';
    mote.style.setProperty('--x', ((i * 37 + 2) % 100) + '%');
    mote.style.setProperty('--duration', (16 + i) + 's');
    mote.style.setProperty('--delay', (-i * 2.4) + 's'); motes.append(mote);
}
document.querySelector('.ambient').append(motes);
applyDeckMotion(); pauseDeckMotion();
const collectionReady = book.load_page();
window.PageTransition?.wait(collectionReady);
