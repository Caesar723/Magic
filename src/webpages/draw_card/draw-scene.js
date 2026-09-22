import * as THREE from '../homepage/vendor/three.module.min.js';
import {PackModel} from '../pack-model.js';

const INK = '#24363b';
const clamp = THREE.MathUtils.clamp;
const ease = value => { const t = clamp(value, 0, 1); return t * t * (3 - 2 * t); };
const mix = THREE.MathUtils.lerp;

// A page-local renderer: it never fetches inventory, chooses cards, or consumes packs.
export class DrawScene {
    constructor(canvas, stage, invalidate, fallback) {
        this.stage = stage;
        this.invalidate = invalidate;
        this.renderer = new THREE.WebGLRenderer({canvas, alpha: true, antialias: true, powerPreference: 'low-power'});
        this.renderer.outputColorSpace = THREE.SRGBColorSpace;
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(34, 1, .1, 80);
        this.camera.position.set(0, 4.3, 13.5);
        this.camera.lookAt(0, 1.05, 0);
        this.textures = new Map();
        this.loader = new THREE.TextureLoader();
        this.listeners = [];
        this.cards = [];
        this.targets = [];
        this.bursts = [];
        this.pointer = new THREE.Vector2();
        this.turn = 0;
        this.angle = 0;
        this.time = 0;
        const grain = new Uint8Array(128 * 128 * 4);
        for (let i = 0; i < grain.length; i += 4) {
            const shade = 224 + Math.floor((Math.sin(i * 12.9898) * 43758.5453 % 1 + 1) * 12);
            grain[i] = grain[i + 1] = grain[i + 2] = shade;
            grain[i + 3] = 255;
        }
        this.grain = new THREE.DataTexture(grain, 128, 128);
        this.grain.wrapS = this.grain.wrapT = THREE.RepeatWrapping;
        this.grain.repeat.set(3, 3);
        this.grain.needsUpdate = true;
        this.scene.add(new THREE.HemisphereLight('#fff1d1', '#405761', 2.5));
        const light = new THREE.DirectionalLight('#fff3d5', 2.1);
        light.position.set(-4, 8, 6);
        this.scene.add(light);
        this.buildStage();
        this.buildParticles();
        this.listen(canvas, 'webglcontextlost', event => { event.preventDefault(); fallback(); });
        this.listen(stage, 'pointermove', event => {
            if (event.target.closest('button, a') || this.model?.reduced) return;
            const box = stage.getBoundingClientRect();
            this.pointer.set((event.clientX - box.left) / box.width - .5, (event.clientY - box.top) / box.height - .5);
            if (this.drag && this.model?.state === 'ready') {
                this.turn += (event.clientX - this.drag.x) * .012;
                this.drag.x = event.clientX;
            }
        });
        this.listen(stage, 'pointerdown', event => {
            if (event.target !== canvas || this.model?.state !== 'ready') return;
            this.drag = {x: event.clientX};
            canvas.setPointerCapture(event.pointerId);
        });
        this.listen(stage, 'pointerup', () => { this.drag = null; });
        this.listen(stage, 'pointercancel', () => { this.drag = null; });
        this.listen(stage, 'lostpointercapture', () => { this.drag = null; });
        this.listen(stage, 'pointerleave', () => { this.pointer.set(0, 0); });
    }
    listen(target, event, handler) {
        target.addEventListener(event, handler);
        this.listeners.push(() => target.removeEventListener(event, handler));
    }
    texture(path, fallback) {
        if (this.textures.has(path)) return this.textures.get(path);
        const texture = this.loader.load(path, () => {
            if (!this.disposed) this.invalidate();
        }, undefined, () => {
            if (!fallback || this.disposed) return;
            this.loader.load(fallback, source => {
                if (this.disposed) { source.dispose(); return; }
                texture.image = source.image;
                texture.needsUpdate = true;
                source.dispose();
                this.invalidate();
            }, undefined, () => {});
        });
        texture.colorSpace = THREE.SRGBColorSpace;
        texture.anisotropy = Math.min(4, this.renderer.capabilities.getMaxAnisotropy());
        this.textures.set(path, texture);
        return texture;
    }
    solid(geometry, color, parent, outline = true) {
        const mesh = new THREE.Mesh(geometry, new THREE.MeshToonMaterial({color, map: this.grain}));
        parent.add(mesh);
        if (outline) {
            const shell = new THREE.Mesh(geometry, new THREE.MeshBasicMaterial({color: INK, side: THREE.BackSide}));
            shell.scale.setScalar(1.022);
            mesh.add(shell);
            mesh.add(new THREE.LineSegments(new THREE.EdgesGeometry(geometry, 25), new THREE.LineBasicMaterial({color: INK})));
        }
        return mesh;
    }
    ring(radius, tube, color, parent, arc = Math.PI * 2) {
        return this.solid(new THREE.TorusGeometry(radius, tube, 5, 72, arc), color, parent, false);
    }
    buildStage() {
        this.plinth = new THREE.Group();
        this.scene.add(this.plinth);
        this.plinth.position.y = -.85;
        const base = this.solid(new THREE.CylinderGeometry(2.65, 2.4, .38, 10), '#6e8288', this.plinth);
        base.rotation.y = Math.PI / 10;
        this.solid(new THREE.CylinderGeometry(2.42, 2.48, .14, 10), '#c3b89b', this.plinth).position.y = .26;
        this.solid(new THREE.CylinderGeometry(1.82, 1.94, .18, 10), '#567c7f', this.plinth).position.y = .42;
        this.stageRing = this.ring(1.65, .026, '#b7d2bc', this.plinth);
        this.stageRing.rotation.x = Math.PI / 2;
        this.stageRing.position.y = .53;
        // Raised compass points and interrupted ink cuts keep the stone from looking machined.
        for (let i = 0; i < 8; i++) {
            const a = i * Math.PI / 4;
            const mark = this.solid(new THREE.ConeGeometry(.09, i % 2 ? .4 : .62, 3), '#b6bd9f', this.plinth, false);
            mark.rotation.set(Math.PI / 2, 0, -a);
            mark.position.set(Math.sin(a) * 1.3, .55, Math.cos(a) * 1.3);
        }
        for (let i = 0; i < 10; i++) {
            const a = i * Math.PI / 5;
            const notch = this.solid(new THREE.BoxGeometry(.08, .045, .25), INK, this.plinth, false);
            notch.position.set(Math.sin(a) * 2.18, .36, Math.cos(a) * 2.18);
            notch.rotation.y = a;
            const rock = this.solid(new THREE.ConeGeometry(.34 + i % 3 * .1, .55 + i % 3 * .28, 4), '#536c78', this.plinth);
            rock.rotation.z = Math.PI;
            rock.position.set(Math.sin(a) * 2.05, -.43, Math.cos(a) * 2.05);
        }
        this.orbits = new THREE.Group();
        this.scene.add(this.orbits);
        this.orbits.position.set(0, 1.3, -1.3);
        const outer = this.ring(2.7, .035, '#9eae9c', this.orbits, Math.PI * 1.8);
        outer.rotation.set(.18, -.35, .1);
        const inner = this.ring(2.5, .023, '#6a9190', this.orbits, Math.PI * 1.65);
        inner.rotation.set(-.24, .5, 2.1);
        this.crystals = [];
        for (let i = 0; i < 3; i++) {
            const group = new THREE.Group();
            const rock = this.solid(new THREE.OctahedronGeometry(.24), '#95bcae', group);
            rock.scale.y = 1.9;
            this.scene.add(group);
            this.crystals.push(group);
        }
        this.ribbons = Array.from({length: 3}, (_, i) => {
            const geometry = new THREE.BufferGeometry();
            geometry.setAttribute('position', new THREE.BufferAttribute(new Float32Array(64 * 3), 3));
            const line = new THREE.Line(geometry, new THREE.LineBasicMaterial({color: i === 1 ? '#e6cf9d' : '#a3d0bc', transparent: true, opacity: .75}));
            line.visible = false;
            this.scene.add(line);
            return line;
        });
        this.shockwaves = Array.from({length: 2}, (_, i) => {
            const ring = new THREE.Mesh(new THREE.RingGeometry(.98, 1.015, 80), new THREE.MeshBasicMaterial({color: i ? '#deceaa' : '#a7d2c0', side: THREE.DoubleSide, transparent: true, opacity: 0, depthWrite: false}));
            ring.position.y = 2.5;
            ring.rotation.x = i ? .35 : Math.PI / 2;
            this.scene.add(ring);
            return ring;
        });
    }
    buildPack(pack, style) {
        if (this.pack) { this.scene.remove(this.pack); this.disposeObject(this.pack); }
        this.turn = 0; this.angle = -.38;
        this.pack = pack ? new PackModel(style, this.texture(style.image, style.fallback), this.solid.bind(this), this.ring.bind(this)) : new THREE.Group();
        this.pack.visible = Boolean(pack);
        this.lid = this.pack.lid;
        this.seal = this.pack.seal;
        this.scene.add(this.pack);
    }
    buildCards(data) {
        this.cards.forEach(card => { this.scene.remove(card); this.disposeObject(card); });
        const texture = this.texture('/webpages/image_source/card/back.png?v=compass');
        this.cards = data.map(() => {
            const group = new THREE.Group();
            this.solid(new THREE.BoxGeometry(1, 1.4, .022), '#d9c7a3', group, false);
            for (const direction of [-1, 1]) {
                const face = new THREE.Mesh(new THREE.PlaneGeometry(1, 1.4), new THREE.MeshBasicMaterial({map: texture}));
                face.position.z = direction * .015;
                face.rotation.y = direction < 0 ? Math.PI : 0;
                group.add(face);
            }
            group.visible = false;
            this.scene.add(group);
            return group;
        });
        this.layoutCards();
    }
    layoutCards() {
        const bounds = this.stage.getBoundingClientRect();
        this.camera.updateMatrixWorld();
        this.targets = [...this.stage.querySelectorAll('.reveal-card')].map(button => {
            const box = button.getBoundingClientRect();
            const ray = new THREE.Vector3((box.left + box.width / 2 - bounds.left) / bounds.width * 2 - 1, 1 - (box.top + box.height / 2 - bounds.top) / bounds.height * 2, .5).unproject(this.camera).sub(this.camera.position).normalize();
            const distance = 9;
            const forward = this.camera.getWorldDirection(new THREE.Vector3());
            const position = this.camera.position.clone().addScaledVector(ray, distance / ray.dot(forward));
            const scale = 2 * Math.tan(THREE.MathUtils.degToRad(this.camera.fov / 2)) * distance * box.height / bounds.height / 1.4;
            return {position, scale};
        });
    }
    buildParticles() {
        this.particles = new THREE.InstancedMesh(new THREE.OctahedronGeometry(1), new THREE.MeshBasicMaterial({color: '#c2d8bc', transparent: true, opacity: .75}), 192);
        this.particles.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
        this.particles.frustumCulled = false;
        this.scene.add(this.particles);
        this.dummy = new THREE.Object3D();
        this.sparkColor = new THREE.Color();
        for (let i = 0; i < 192; i++) this.particles.setColorAt(i, this.sparkColor.set(i % 4 ? '#b1cbbb' : '#ddc29a'));
    }
    reveal(index, rarity) {
        const target = this.targets[index];
        if (target && !this.model?.reduced) this.bursts.push({position: target.position.clone(), time: this.time, rare: /rare/i.test(rarity)});
        if (this.bursts.length > 6) this.bursts.shift();
    }
    rotate() {
        this.turn += Math.PI * .5;
        this.invalidate();
    }
    resize() {
        const {width, height} = this.stage.getBoundingClientRect();
        const dpr = Math.min(devicePixelRatio || 1, 1.5, Math.sqrt(2500000 / Math.max(1, width * height)));
        this.renderer.setPixelRatio(dpr);
        this.renderer.setSize(width, height, false);
        this.camera.aspect = width / height;
        // Keep the pack and its plinth inside the narrowest viewport.
        this.camera.fov = width < 620 ? 46 : 34;
        this.camera.position.z = width < 620 ? Math.max(13.5, 5.6 / this.camera.aspect) : 13.5;
        this.camera.lookAt(0, 1.05, 0);
        this.camera.updateProjectionMatrix();
        this.layoutCards();
    }
    render(model, time, dt = 0) {
        if (this.disposed) return;
        this.model = model;
        this.time = time;
        if (this.selected !== model.moving_mouse_obj) {
            this.selected = model.moving_mouse_obj;
            this.buildPack(this.selected, this.selected ? model.style_for(this.selected) : null);
        }
        if (this.data !== model.card_in_pack) { this.data = model.card_in_pack; this.buildCards(this.data); }
        const opening = model.state === 'opening';
        const result = ['reveal', 'complete'].includes(model.state);
        const phase = opening ? model.phase : 0;
        const motion = model.reduced ? 0 : time;
        const activation = opening ? ease(phase / 1.2) * (1 - ease((phase - 5) / 1.5)) : model.state === 'requesting' ? .25 : 0;
        this.plinth.position.y = -.85 + Math.sin(motion * .7) * .045;
        this.orbits.rotation.z = motion * .045 + activation * .6;
        this.orbits.scale.setScalar(1 + activation * .13);
        this.crystals.forEach((crystal, i) => {
            const a = i * Math.PI * 2 / 3 + motion * .16;
            crystal.position.set(Math.cos(a) * 3.2, .5 + Math.sin(motion + i) * .18, Math.sin(a) * 1.6 - .6);
            crystal.rotation.y = motion * .35;
        });
        if (this.pack && this.selected) {
            this.pack.visible = !result && phase < 5.35;
            const lift = ease(phase / 1.5) * .5;
            const exit = ease((phase - 4.1) / 1.25);
            const desired = opening ? -.38 + Math.sin(phase * 3) * .07 : this.turn - .38 + this.pointer.x * .45;
            this.angle = model.reduced ? desired : mix(this.angle, desired, Math.min(1, dt * 7));
            this.pack.rotation.set(.05 + (opening ? 0 : this.pointer.y * .12), this.angle, opening ? Math.sin(phase * 15) * .009 * (1 - ease(phase)) : Math.sin(motion * .5) * .022);
            this.pack.position.set(0, -.04 + Math.sin(motion * 1.1) * .06 + lift - exit * 1.6, exit * -1.5);
            this.pack.scale.setScalar(1 - exit * .98);
            this.lid.rotation.x = -ease((phase - 1.1) / 1.1) * 2.1;
            this.seal.position.z = model.style_for(this.selected).depth / 2 + .11 + ease(phase / .85) * .8;
            this.seal.position.y = 2.32 + ease(phase / 1.2) * .55;
            this.seal.scale.setScalar(1 - ease((phase - .8) / .65));
        }
        this.cards.forEach((card, i) => {
            const progress = clamp((phase - 2 - i * .15) / 1.6, 0, 1);
            card.visible = opening && phase > 2 + i * .15;
            if (!card.visible) return;
            const angle = i * Math.PI * 2 / Math.max(1, this.cards.length) + progress * 3.8;
            const radius = ease(progress) * 2.3;
            card.position.set(Math.cos(angle) * radius, 2.35 + Math.sin(progress * Math.PI) * 2 + Math.sin(angle) * .5, .3 + Math.sin(angle) * radius * .6);
            card.rotation.set(-.18 + Math.sin(progress * Math.PI) * .9, angle + Math.PI * 2 * progress, Math.cos(angle) * .2);
            card.scale.setScalar(.62 + ease(progress) * .25);
            const settle = ease((phase - 4.3 - i * .09) / (1.8 - i * .09));
            const target = this.targets[i];
            if (target && settle > 0) {
                card.position.lerp(target.position, settle);
                card.quaternion.slerp(this.camera.quaternion, settle);
                card.scale.setScalar(mix(.87, target.scale, settle));
            }
        });
        this.ribbons.forEach((ribbon, i) => {
            ribbon.visible = activation > .01 && !model.reduced;
            if (!ribbon.visible) return;
            ribbon.material.opacity = activation * .6;
            const points = ribbon.geometry.attributes.position;
            for (let n = 0; n < points.count; n++) {
                const t = n / (points.count - 1);
                const a = t * Math.PI * 2.6 + i * Math.PI * 2 / 3 + motion * 1.8;
                const radius = (1.3 + t * .85) * activation;
                points.setXYZ(n, Math.cos(a) * radius, -.2 + t * 4.8, Math.sin(a) * radius);
            }
            points.needsUpdate = true;
        });
        this.shockwaves.forEach((ring, i) => {
            const t = (phase - 1.15 - i * .22) / 1.3;
            ring.visible = opening && t > 0 && t < 1 && !model.reduced;
            ring.scale.setScalar(.7 + ease(t) * 4.2);
            ring.material.opacity = (1 - clamp(t, 0, 1)) * .65;
        });
        this.bursts = this.bursts.filter(burst => time - burst.time < 1.2);
        this.particles.visible = !model.reduced;
        if (!model.reduced) {
            for (let i = 0; i < 192; i++) {
                const seed = i * 2.39996;
                const a = seed + motion * (.06 + activation * .5);
                const radius = 1.8 + (i % 23) * .24;
                this.dummy.position.set(Math.cos(a) * radius, ((i * .317 + motion * (.08 + activation * .85)) % 6.8) - 1.4, Math.sin(a) * radius * .6);
                let size = .012 + i % 4 * .006;
                if (opening && phase > 1.2 && phase < 3 && i > 95) {
                    const t = phase - 1.2;
                    this.dummy.position.set(Math.cos(seed) * t * 3, 2.5 + Math.sin(seed) * t * 2 - t * t * .6, Math.sin(seed * 3) * t * 2);
                    size *= 1.5 * (1 - t / 1.8);
                }
                const burst = this.bursts[i % Math.max(1, this.bursts.length)];
                if (burst && i < 96) {
                    const t = time - burst.time;
                    this.dummy.position.set(burst.position.x + Math.cos(seed) * t * 2.2, burst.position.y + Math.sin(seed) * t * 2.2, burst.position.z + .15);
                    size *= (burst.rare ? 2 : 1) * (1 - t / 1.2);
                }
                this.dummy.rotation.set(seed, a, motion);
                this.dummy.scale.setScalar(Math.max(0, size));
                this.dummy.updateMatrix();
                this.particles.setMatrixAt(i, this.dummy.matrix);
            }
            this.particles.instanceMatrix.needsUpdate = true;
        }
        this.renderer.render(this.scene, this.camera);
    }
    disposeObject(object) {
        const geometries = new Set(), materials = new Set();
        object.traverse(child => {
            if (child.geometry) geometries.add(child.geometry);
            if (child.material) materials.add(child.material);
        });
        geometries.forEach(geometry => geometry.dispose());
        materials.forEach(material => material.dispose());
    }
    dispose() {
        this.disposed = true;
        this.listeners.splice(0).forEach(remove => remove());
        this.disposeObject(this.scene);
        this.textures.forEach(texture => texture.dispose());
        this.grain.dispose();
        this.renderer.dispose();
    }
}
