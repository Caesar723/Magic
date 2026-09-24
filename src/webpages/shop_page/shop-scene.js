import * as THREE from '../homepage/vendor/three.module.min.js';
import {PackModel} from '../pack-model.js';

// Optional display only. All purchasing is handled by the existing page controller.
export class ShopScene {
    constructor(canvas, stage, invalidate, fallback) {
        this.stage = stage;
        this.invalidate = invalidate;
        this.renderer = new THREE.WebGLRenderer({canvas, alpha: true, antialias: true, powerPreference: 'low-power'});
        this.renderer.outputColorSpace = THREE.SRGBColorSpace;
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(35, 1, .1, 40);
        this.camera.position.set(0, 2.9, 8.6);
        this.camera.lookAt(0, 1.25, 0);
        this.loader = new THREE.TextureLoader();
        this.textures = new Map();
        this.listeners = [];
        this.pointer = new THREE.Vector2();
        this.turn = 0;
        this.angle = -.4;
        this.time = 0;
        this.successTime = -10;
        const grain = new Uint8Array(128 * 128 * 4);
        for (let i = 0; i < grain.length; i += 4) {
            grain[i] = grain[i + 1] = grain[i + 2] = 232 + Math.floor((Math.sin(i * 12.9898) % 1 + 1) * 10);
            grain[i + 3] = 255;
        }
        this.grain = new THREE.DataTexture(grain, 128, 128);
        this.grain.wrapS = this.grain.wrapT = THREE.RepeatWrapping;
        this.grain.repeat.set(3, 3);
        this.grain.needsUpdate = true;
        this.scene.add(new THREE.HemisphereLight('#fff1d1', '#405761', 2.5));
        const light = new THREE.DirectionalLight('#fff3d5', 2.1);
        light.position.set(-4, 8, 6); this.scene.add(light);
        this.build_display();
        this.listen(canvas, 'webglcontextlost', event => { event.preventDefault(); fallback(); });
        this.listen(canvas, 'pointermove', event => {
            if (this.reduced) return;
            const bounds = canvas.getBoundingClientRect();
            this.pointer.set((event.clientX - bounds.left) / bounds.width - .5, (event.clientY - bounds.top) / bounds.height - .5);
            if (this.drag) { this.turn += (event.clientX - this.drag.x) * .012; this.drag.x = event.clientX; }
        });
        this.listen(canvas, 'pointerdown', event => { this.drag = {x: event.clientX}; canvas.setPointerCapture(event.pointerId); });
        for (const type of ['pointerup', 'pointercancel', 'lostpointercapture']) this.listen(canvas, type, () => { this.drag = null; });
        this.listen(canvas, 'pointerleave', () => this.pointer.set(0, 0));
    }
    listen(target, event, handler) {
        target.addEventListener(event, handler);
        this.listeners.push(() => target.removeEventListener(event, handler));
    }
    solid(geometry, color, parent, outline = true) {
        const mesh = new THREE.Mesh(geometry, new THREE.MeshToonMaterial({color, map: this.grain}));
        parent.add(mesh);
        if (outline) {
            const shell = new THREE.Mesh(geometry, new THREE.MeshBasicMaterial({color: '#24363b', side: THREE.BackSide}));
            shell.scale.setScalar(1.022); mesh.add(shell);
            mesh.add(new THREE.LineSegments(new THREE.EdgesGeometry(geometry, 25), new THREE.LineBasicMaterial({color: '#24363b'})));
        }
        return mesh;
    }
    ring(radius, tube, color, parent) {
        return this.solid(new THREE.TorusGeometry(radius, tube, 5, 64), color, parent, false);
    }
    build_display() {
        this.stand = new THREE.Group();
        this.scene.add(this.stand);
        this.solid(new THREE.CylinderGeometry(1.9, 1.8, .21, 8), '#a5a58e', this.stand).position.y = -.11;
        this.solid(new THREE.CylinderGeometry(1.65, 1.7, .38, 8), '#6c8287', this.stand).position.y = -.38;
        this.solid(new THREE.CylinderGeometry(1.77, 1.88, .15, 8), '#485f69', this.stand).position.y = -.64;
        for (let i = 0; i < 8; i++) {
            const a = i * Math.PI / 4;
            const mark = this.solid(new THREE.BoxGeometry(.045, .025, .25), '#4c666b', this.stand, false);
            mark.position.set(Math.sin(a) * 1.58, .012, Math.cos(a) * 1.58);
            mark.rotation.y = a;
        }
        this.motes = new THREE.InstancedMesh(new THREE.OctahedronGeometry(1), new THREE.MeshBasicMaterial({color: '#c2d5b5', transparent: true, opacity: .65}), 80);
        this.motes.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
        this.motes.frustumCulled = false;
        this.scene.add(this.motes);
        this.dummy = new THREE.Object3D();
    }
    texture(style) {
        if (this.textures.has(style.image)) return this.textures.get(style.image);
        window.PageTransition?.image(style.image);
        const texture = this.loader.load(style.image, () => { if (!this.disposed) this.invalidate(); }, undefined, () => {
            if (style.image === style.fallback || this.disposed) return;
            window.PageTransition?.image(style.fallback);
            this.loader.load(style.fallback, source => {
                if (!this.disposed) { texture.image = source.image; texture.needsUpdate = true; this.invalidate(); }
                source.dispose();
            }, undefined, () => {});
        });
        texture.colorSpace = THREE.SRGBColorSpace;
        texture.anisotropy = Math.min(4, this.renderer.capabilities.getMaxAnisotropy());
        this.textures.set(style.image, texture);
        return texture;
    }
    select(item) {
        if (this.item === item || this.disposed) return;
        this.item = item;
        if (this.pack) { this.scene.remove(this.pack); this.dispose_object(this.pack); this.pack = null; }
        if (item) {
            this.pack = new PackModel(item.art, this.texture(item.art), this.solid.bind(this), this.ring.bind(this));
            this.scene.add(this.pack);
        }
        this.turn = 0; this.angle = -.4;
        this.selectedTime = this.time;
        this.invalidate();
    }
    rotate() { this.turn += Math.PI / 2; this.invalidate(); }
    celebrate() { this.successTime = this.time; this.invalidate(); }
    resize() {
        const {width, height} = this.stage.getBoundingClientRect();
        this.renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 1.5, Math.sqrt(1800000 / Math.max(1, width * height))));
        this.renderer.setSize(width, height, false);
        this.camera.aspect = width / height;
        this.camera.position.z = Math.max(8.6, 6 / this.camera.aspect);
        this.camera.updateProjectionMatrix();
    }
    render(time, dt = 0, reduced = false) {
        if (this.disposed) return;
        this.time = time; this.reduced = reduced;
        const motion = reduced ? 0 : time;
        if (this.pack) {
            const target = this.turn - .4 + (reduced ? 0 : this.pointer.x * .42);
            this.angle = reduced ? target : THREE.MathUtils.lerp(this.angle, target, Math.min(1, dt * 8));
            const entering = reduced ? 1 : THREE.MathUtils.smoothstep(time - this.selectedTime, 0, .42);
            this.pack.rotation.set(.02 + (reduced ? 0 : this.pointer.y * .13), this.angle, Math.sin(motion * .6) * .015);
            this.pack.position.set(0, .12 + Math.sin(motion * 1.2) * .055 + (1 - entering) * .15, 0);
            this.pack.scale.setScalar(.93 + entering * .07);
        }
        this.motes.visible = !reduced;
        if (!reduced) {
            const burst = time - this.successTime;
            for (let i = 0; i < 80; i++) {
                const seed = i * 2.39996;
                const a = seed + motion * .07;
                const radius = 1.2 + (i % 13) * .18;
                this.dummy.position.set(Math.cos(a) * radius, (i * .287 + motion * .09) % 4.3 - .3, Math.sin(a) * radius * .45 - .2);
                let size = .012 + i % 3 * .008;
                if (burst < 1.5) {
                    this.dummy.position.set(Math.cos(seed) * burst * 2.7, 1.5 + Math.sin(seed) * burst * 2.7 - burst * burst * .35, Math.sin(seed * 2) * burst);
                    size *= 1.8 * (1 - burst / 1.5);
                }
                this.dummy.rotation.set(seed, a, motion * .2);
                this.dummy.scale.setScalar(Math.max(0, size)); this.dummy.updateMatrix();
                this.motes.setMatrixAt(i, this.dummy.matrix);
            }
            this.motes.instanceMatrix.needsUpdate = true;
        }
        this.renderer.render(this.scene, this.camera);
    }
    dispose_object(object) {
        const geometries = new Set(), materials = new Set();
        object.traverse(child => { if (child.geometry) geometries.add(child.geometry); if (child.material) materials.add(child.material); });
        geometries.forEach(geometry => geometry.dispose());
        materials.forEach(material => material.dispose());
    }
    dispose() {
        this.disposed = true;
        this.listeners.splice(0).forEach(remove => remove());
        this.dispose_object(this.scene);
        this.textures.forEach(texture => texture.dispose());
        this.grain.dispose(); this.motes.dispose(); this.renderer.dispose();
    }
}
