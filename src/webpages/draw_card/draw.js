if ('serviceWorker' in navigator) navigator.serviceWorker.register('/webpages/service-worker.js').catch(() => {});

const canvas = document.getElementById('myCanvas');
const stage = document.getElementById('canvasContainer');
const draw_card_system = new Draw_card();
draw_card_system.set_listener(canvas);
const motionPreference = matchMedia('(prefers-reduced-motion: reduce)');
let scene, frame = 0, last = 0, elapsed = 0;
let focused = document.hasFocus(), hidden = document.hidden;
let disposed = false;

function stopDrawing() {
    cancelAnimationFrame(frame); frame = 0; last = 0;
    stage.dataset.animating = 'false';
}
function render() {
    if (!hidden && focused && !disposed) scene?.render(draw_card_system, elapsed);
}
function draw_picture(now) {
    frame = 0;
    if (hidden || !focused || disposed || draw_card_system.reduced) return;
    if (!last || now - last >= 32) {
        const dt = last ? Math.min((now - last) / 1000, .06) : 0;
        last = now; elapsed += dt;
        draw_card_system.update(dt);
        scene?.render(draw_card_system, elapsed, dt);
    }
    frame = requestAnimationFrame(draw_picture);
}
function resumeDrawing() {
    document.body.classList.toggle('motion-paused', hidden || !focused);
    if (hidden || !focused || disposed || draw_card_system.reduced) { stopDrawing(); render(); }
    else if (!frame) { stage.dataset.animating = 'true'; frame = requestAnimationFrame(draw_picture); }
}
function applyMotion() {
    let preference = false;
    try { preference = localStorage.getItem('lobby-reduced-motion') === 'true'; } catch (_) {}
    draw_card_system.reduced = motionPreference.matches || preference;
    document.body.classList.toggle('motion-reduced', draw_card_system.reduced);
    if (draw_card_system.reduced) draw_card_system.finish_opening();
    resumeDrawing();
}
function fallback() {
    stage.classList.remove('webgl-ready');
    stage.dataset.renderer = 'fallback';
    document.getElementById('rotate-pack').hidden = true;
    scene?.dispose(); scene = null;
    draw_card_system.scene = null;
}
function resize() {
    scene?.resize();
    render();
}
draw_card_system.invalidate = render;
const resizeObserver = new ResizeObserver(resize);
resizeObserver.observe(stage);
motionPreference.addEventListener('change', applyMotion);
window.addEventListener('storage', event => { if (event.key === 'lobby-reduced-motion') applyMotion(); });
window.addEventListener('blur', () => { focused = false; resumeDrawing(); });
window.addEventListener('focus', () => { focused = true; resumeDrawing(); });
document.addEventListener('visibilitychange', () => { hidden = document.hidden; resumeDrawing(); });
window.addEventListener('pagehide', event => {
    hidden = true; resumeDrawing();
    if (!event.persisted) { disposed = true; resizeObserver.disconnect(); draw_card_system.clear_faces(); scene?.dispose(); }
});
window.addEventListener('pageshow', () => { hidden = document.hidden; focused = document.hasFocus(); resumeDrawing(); });
applyMotion();
const packsReady = draw_card_system.send_packs_request();
window.PageTransition?.wait(packsReady);
const drawReady = import('./draw-scene.js').then(({DrawScene}) => {
    if (disposed) return;
    scene = new DrawScene(canvas, stage, render, fallback);
    draw_card_system.scene = scene;
    resize();
    stage.classList.add('webgl-ready');
    stage.dataset.renderer = 'three';
    document.getElementById('rotate-pack').hidden = draw_card_system.state !== 'ready' || !draw_card_system.moving_mouse_obj;
}).catch(fallback);

window.PageTransition?.wait(drawReady);
