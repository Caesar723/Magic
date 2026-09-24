// Enhance the existing HTML controls; WebGL never owns navigation or deck state.
const stage = document.getElementById('lobby-stage');
const canvas = document.getElementById('lobby-canvas');
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
const textures = new Map();
const objects = new Map();
const listeners = [];
let renderer, scene, camera, resizeObserver, renderFrame;
let width = 0, height = 0, raf = 0, last = 0, elapsed = 0;
let disposed = false, focused = document.hasFocus();
const isReduced = () => reduced.matches || document.body.classList.contains('motion-reduced');
const on = (element, event, handler) => {
    element.addEventListener(event, handler);
    listeners.push(() => element.removeEventListener(event, handler));
};

function stop() {
    cancelAnimationFrame(raf);
    raf = 0;
    last = 0;
    stage.dataset.animating = 'false';
}
function requestFrame() {
    if (disposed || !renderer || document.hidden || !focused) return;
    if (isReduced()) {
        stop();
        renderFrame?.(0);
    } else if (!raf) {
        raf = requestAnimationFrame(tick);
    }
}
function tick(now) {
    raf = 0;
    if (disposed || document.hidden || !focused || isReduced()) return;
    if (!last || now - last >= 32) {
        const dt = last ? Math.min((now - last) / 1000, .06) : .033;
        last = now;
        elapsed += dt;
        renderFrame(dt);
    }
    stage.dataset.animating = 'true';
    raf = requestAnimationFrame(tick);
}
function fallback(reason) {
    stop();
    disposed = true;
    stage.classList.remove('webgl-ready');
    stage.dataset.renderer = 'fallback';
    stage.dataset.fallbackReason = reason;
    resizeObserver?.disconnect();
    listeners.splice(0).forEach(remove => remove());
    scene?.traverse(object => {
        object.geometry?.dispose();
        object.material?.dispose();
    });
    textures.forEach(texture => texture.dispose());
    renderer?.dispose();
}

async function init() {
    const THREE = await import('./vendor/three.module.min.js');
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'low-power' });
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    scene = new THREE.Scene();
    camera = new THREE.OrthographicCamera(0, 1600, 850, 0, .1, 2000);
    camera.position.z = 1000;
    const loader = new THREE.TextureLoader();
    await Promise.all(['battle-map', 'platform', 'props', 'props-active'].map(async name => {
        const texture = await loader.loadAsync(`/webpages/homepage/art/${name}.png${name.startsWith('props') ? '?v=2' : ''}`);
        if (disposed) { texture.dispose(); return; }
        texture.colorSpace = THREE.SRGBColorSpace;
        texture.anisotropy = Math.min(4, renderer.capabilities.getMaxAnisotropy());
        textures.set(name, texture);
    }));
    if (disposed) return;

    // Crop with UVs, so every prop shares one GPU texture. The SVG viewBox is
    // the single source of crop coordinates for both HTML and WebGL rendering.
    function sprite(element, name, depth) {
        const texture = textures.get(name);
        const crop = element.viewBox?.baseVal;
        const geometry = new THREE.PlaneGeometry(1, 1);
        if (crop) {
            const uv = geometry.attributes.uv;
            const image = element.querySelector('image');
            const sourceWidth = Number(image.getAttribute('width'));
            const sourceHeight = Number(image.getAttribute('height'));
            for (let i = 0; i < uv.count; i++) {
                uv.setXY(i, (crop.x + uv.getX(i) * crop.width) / sourceWidth,
                    1 - (crop.y + (1 - uv.getY(i)) * crop.height) / sourceHeight);
            }
        }
        const mesh = new THREE.Mesh(geometry, new THREE.MeshBasicMaterial({ map: texture, transparent: true, depthWrite: false }));
        mesh.position.z = depth;
        mesh.renderOrder = depth;
        mesh.userData = { element, ratio: crop ? crop.width / crop.height : texture.image.width / texture.image.height };
        scene.add(mesh);
        return mesh;
    }
    function measure(mesh) {
        const { element, ratio } = mesh.userData;
        const bounds = element.getBoundingClientRect();
        const stageBounds = stage.getBoundingClientRect();
        const ew = element.clientWidth, eh = element.clientHeight;
        const w = Math.min(ew, eh * ratio), h = w / ratio;
        mesh.userData.rect = { x: bounds.left - stageBounds.left + bounds.width / 2 - w / 2,
            y: bounds.top - stageBounds.top + bounds.height / 2 - h / 2, w, h };
        place(mesh);
    }
    function place(mesh, lift = 0) {
        const r = mesh.userData.rect;
        mesh.position.x = r.x + r.w / 2;
        mesh.position.y = height - r.y - r.h / 2 + lift;
        mesh.scale.set(r.w, r.h, 1);
        mesh.rotation.z = -Number(mesh.userData.element.dataset.angle || 0) * Math.PI / 180;
    }
    const mapElement = document.querySelector('.map-art');
    const map = sprite(mapElement, 'battle-map', 5);
    const mapEdge = sprite(mapElement, 'battle-map', 4);
    mapEdge.material.color.set(0xb9d7b8);
    mapEdge.material.opacity = 0;
    const platforms = [...document.querySelectorAll('.platform-art')].map(element => sprite(element, 'platform', 2));
    const figures = [...document.querySelectorAll('.hero-sprite')].map((element, index) => sprite(element, 'props', 10 + index));
    objects.set('battle', { value: 0, target: 0, age: 0 });
    document.querySelectorAll('.object-button').forEach(button => {
        const element = button.querySelector('.object-art');
        const base = sprite(element, 'props', 20);
        const activeElement = button.querySelector('.object-active');
        const active = activeElement ? sprite(activeElement, 'props-active', 21) : null;
        if (active) active.material.opacity = 0;
        const shelf = [...document.querySelectorAll('.shelf')].indexOf(button.closest('.shelf'));
        objects.set(button.dataset.object, { base, active, shelf, value: 0, target: 0, age: 0 });
    });
    const brush = sprite(document.querySelector('.studio-brush'), 'props', 23);

    // One draw call for sky dust, portal sparks and the battle-map updraft.
    const ambientCount = 96, portalCount = 36, battleCount = 24;
    const count = ambientCount + portalCount + battleCount;
    const particlePositions = new Float32Array(count * 3);
    const particleSeeds = Float32Array.from({ length: count }, (_, i) => i * 2.399);
    const particleGeometry = new THREE.BufferGeometry();
    particleGeometry.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
    particleGeometry.setAttribute('seed', new THREE.BufferAttribute(particleSeeds, 1));
    const particles = new THREE.Points(particleGeometry, new THREE.ShaderMaterial({
        uniforms: { time: { value: 0 }, pixelRatio: { value: 1 } },
        vertexShader: `attribute float seed; uniform float time; uniform float pixelRatio; varying float glow; varying float tint;
            void main() { glow = .2 + .55 * pow(.5 + .5 * sin(time * 1.4 + seed), 2.);
                tint = step(.45, fract(seed)); gl_PointSize = (2.5 + mod(seed, 4.)) * pixelRatio;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }`,
        fragmentShader: `varying float glow; varying float tint;
            void main() { vec2 p = abs(gl_PointCoord - .5); float d = p.x + p.y;
                float alpha = (1. - smoothstep(.12, .48, d)) * glow;
                gl_FragColor = vec4(mix(vec3(.89, .84, .67), vec3(.60, .85, .76), tint), alpha); }`,
        transparent: true, depthWrite: false
    }));
    particles.frustumCulled = false;
    particles.renderOrder = 25;
    scene.add(particles);
    const portalRing = new THREE.Mesh(new THREE.RingGeometry(.96, 1, 48, 1, 0, Math.PI * 1.65),
        new THREE.MeshBasicMaterial({ color: 0xc4e5ca, transparent: true, opacity: 0, depthWrite: false }));
    portalRing.renderOrder = 24;
    scene.add(portalRing);

    renderFrame = dt => {
        const motion = !isReduced();
        objects.forEach(object => {
            object.value = THREE.MathUtils.lerp(object.value, object.target, 1 - Math.exp(-dt * 10));
            if (object.target) object.age += dt;
        });
        const battle = motion ? objects.get('battle').value : 0;
        const worldScale = Math.min(width / 1200, 1.3);
        const drift = motion ? Math.sin(elapsed * .65) * 3 * worldScale : 0;
        const shelfLift = index => motion ? Math.sin(elapsed * .75 + index * 1.8) * 2.5 * worldScale : 0;
        place(map, drift);
        place(mapEdge, drift);
        platforms.forEach((mesh, index) => place(mesh, shelfLift(index)));
        mapEdge.scale.multiplyScalar(1 + .006 * battle);
        mapEdge.material.opacity = battle * .5;
        figures.forEach((mesh, index) => {
            const card = mesh.userData.element.dataset.part.startsWith('card');
            const float = motion && card ? Math.sin(elapsed * 1.1 + index) * 2 * worldScale : 0;
            place(mesh, drift + float + battle * (card ? 12 : Math.sin(elapsed * 2 + index) * 3) * worldScale);
            if (card && motion) mesh.rotation.z += (.004 + battle * .012) * Math.sin(index + elapsed);
        });
        objects.forEach((object, key) => {
            if (!object.base) return;
            const a = motion ? object.value : object.target;
            const scale = object.base.userData.rect.w / 260;
            let reveal = key === 'tasks' ? a * Math.max(0, Math.min(1, 2.8 - object.age)) : a;
            if (key === 'rogue' && motion) reveal = .18 + .82 * a;
            const lift = shelfLift(object.shelf) + (motion ? a * 3 * scale : 0);
            place(object.base, lift);
            if (object.active) {
                place(object.active, lift);
                object.base.material.opacity = 1 - reveal;
                object.active.material.opacity = reveal;
                if (key === 'guide' && motion) object.active.scale.x *= 1 + a * .025;
                if (key === 'deck' && motion) object.active.rotation.y = a * .04;
            }
            if (key === 'studio') {
                place(brush, lift + (motion ? a * 12 * scale : 0));
                brush.position.x += motion ? a * 4 * scale : 0;
                brush.rotation.z += motion ? a * .21 : 0;
            }
        });
        const portal = objects.get('rogue');
        const r = portal.base.userData.rect;
        const a = motion ? portal.value : 0;
        const cx = r.x + r.w * .51, cy = height - r.y - r.h * .53 + shelfLift(portal.shelf);
        portalRing.position.set(cx, cy, 30);
        portalRing.scale.set(r.w * .23, r.h * .32, 1);
        portalRing.rotation.z = elapsed * (.2 + a * .5);
        portalRing.material.opacity = motion ? .15 + a * .45 : 0;
        particles.visible = motion;
        particles.material.uniforms.time.value = elapsed;
        for (let i = 0; i < ambientCount; i++) {
            const seed = particleSeeds[i];
            particlePositions[i * 3] = (i * 157.7 + elapsed * (2 + i % 3)) % (width + 40) - 20 + Math.sin(elapsed * .3 + seed) * 9;
            particlePositions[i * 3 + 1] = (i * 93.1 + elapsed * (3 + i % 4)) % height;
            particlePositions[i * 3 + 2] = 32;
        }
        for (let i = 0; i < portalCount; i++) {
            const j = (i + ambientCount) * 3;
            const angle = i * 2.399 + elapsed * (.24 + a * .6);
            const radius = (i % 5 + 2) * r.w * .035;
            particlePositions[j] = cx + Math.cos(angle) * radius;
            particlePositions[j + 1] = cy + Math.sin(angle) * radius * 1.5 + ((elapsed * (10 + a * 16) + i * 4) % 60 - 30) * r.h / 250;
            particlePositions[j + 2] = 32;
        }
        const mr = map.userData.rect;
        for (let i = 0; i < battleCount; i++) {
            const j = (i + ambientCount + portalCount) * 3;
            const rise = (elapsed * (.07 + battle * .1) + i / battleCount) % 1;
            particlePositions[j] = mr.x + mr.w * (.2 + (i * .137 % .6)) + Math.sin(elapsed + i) * 7;
            particlePositions[j + 1] = height - mr.y - mr.h * (.8 - rise * .42) + drift;
            particlePositions[j + 2] = 32;
        }
        particleGeometry.attributes.position.needsUpdate = true;
        renderer.render(scene, camera);
    };
    const layout = () => {
        const bounds = stage.getBoundingClientRect();
        width = bounds.width; height = bounds.height;
        renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 1.5, Math.sqrt(2500000 / (width * height))));
        particles.material.uniforms.pixelRatio.value = renderer.getPixelRatio();
        renderer.setSize(width, height, false);
        camera.right = width; camera.top = height; camera.updateProjectionMatrix();
        [map, mapEdge, brush, ...platforms, ...figures].forEach(measure);
        objects.forEach(object => { if (object.base) measure(object.base); if (object.active) measure(object.active); });
        renderFrame(0);
        requestFrame();
    };
    document.querySelectorAll('[data-object]').forEach(button => {
        const object = objects.get(button.dataset.object);
        const enter = () => { object.target = 1; object.age = 0; requestFrame(); };
        const leave = () => { object.target = 0; requestFrame(); };
        on(button, 'pointerenter', enter); on(button, 'pointerleave', leave);
        on(button, 'focus', enter); on(button, 'blur', leave);
    });
    on(window, 'blur', () => { focused = false; objects.forEach(object => object.target = 0); stop(); });
    on(window, 'focus', () => { focused = true; requestFrame(); });
    on(document, 'visibilitychange', () => document.hidden ? stop() : requestFrame());
    on(reduced, 'change', requestFrame);
    on(document, 'lobby:motion-change', requestFrame);
    on(canvas, 'webglcontextlost', event => { event.preventDefault(); fallback('context-lost'); });
    on(window, 'pagehide', () => fallback('page-hidden'));
    resizeObserver = new ResizeObserver(layout);
    resizeObserver.observe(stage);
    layout();
    stage.classList.add('webgl-ready');
    stage.dataset.renderer = 'webgl';
    requestFrame();
}
const lobbyReady = init().catch(error => {
    console.warn('Lobby illustration fallback:', error.message);
    fallback('unavailable');
});

window.PageTransition?.wait(lobbyReady);
