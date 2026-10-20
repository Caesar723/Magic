// GPU presentation of the existing camera-space geometry. Gameplay and hit tests
// keep using the same objects and coordinates; the input canvas remains the UI.
class BattleRenderer {
    constructor(canvas, ctx) {
        this.canvas = canvas;
        this.ctx = ctx;
        this.ready = false;
        this.drawing = false;
        this.disposed = false;
        this.frame = 0;
        this.meshes = new Map();
        this.textures = new Map();
        this.glows = new Map();
        this.motion = matchMedia('(prefers-reduced-motion: reduce)');
        ctx.battleRenderer = this;
        canvas.dataset.renderer = 'canvas';
        this.installTouch();
        const loading = BattleRenderer.library.then(THREE => this.initialize(THREE)).catch(() => this.dispose());
        window.PageTransition?.wait(loading);
        window.addEventListener('pagehide', () => this.dispose(), {once: true});
    }

    initialize(THREE) {
        if (this.disposed) return;
        if (!THREE) { this.dispose(); return; }
        this.THREE = THREE;
        this.surface = document.createElement('canvas');
        this.surface.className = 'battle-webgl';
        this.surface.setAttribute('aria-hidden', 'true');
        this.renderer = new THREE.WebGLRenderer({canvas: this.surface, alpha: true, antialias: true, powerPreference: 'high-performance'});
        // Logical canvas dimensions also define every existing pointer hit test.
        this.renderer.setPixelRatio(1);
        this.renderer.setSize(this.canvas.width, this.canvas.height, false);
        this.renderer.setClearColor(0x000000, 0);
        this.renderer.outputColorSpace = THREE.SRGBColorSpace;
        this.scene = new THREE.Scene();
        const fov = 2 * Math.atan(this.canvas.height / (2 * 900)) * 180 / Math.PI;
        this.camera = new THREE.PerspectiveCamera(fov, this.canvas.width / this.canvas.height, .01, 100000);
        this.camera.up.set(0, -1, 0);
        this.camera.lookAt(0, 0, 1);
        this.surface.addEventListener('webglcontextlost', event => {
            event.preventDefault();
            this.dispose();
        });
        this.canvas.before(this.surface);
        this.canvas.style.zIndex = '1';
        this.ready = true;
        this.canvas.dataset.renderer = 'threejs';
        this.syncViewport();
    }

    get active() { return this.ready && this.drawing; }
    get reducedMotion() { return this.motion.matches; }

    syncViewport() {
        const style = this.canvas.style.cssText;
        if (style === this.viewportStyle) return;
        this.viewportStyle = style;
        this.surface.style.cssText = style;
        Object.assign(this.surface.style, {
            position: 'absolute', pointerEvents: 'none', zIndex: '0',
            width: this.canvas.width + 'px', height: this.canvas.height + 'px'
        });
    }

    begin() {
        if (!this.ready) return;
        this.frame++;
        this.order = 0;
        this.filter = 'none';
        this.drawing = true;
        for (const entry of this.meshes.values()) entry.mesh.visible = false;
    }

    texture(image) {
        let entry = this.textures.get(image);
        if (entry && (entry.width !== image.width || entry.height !== image.height)) {
            entry.texture.dispose();
            this.textures.delete(image);
            entry = null;
        }
        if (!entry) {
            const texture = new this.THREE.Texture(image);
            texture.flipY = false;
            texture.colorSpace = this.THREE.SRGBColorSpace;
            texture.minFilter = this.THREE.LinearFilter;
            texture.magFilter = this.THREE.LinearFilter;
            texture.generateMipmaps = false;
            entry = {texture, width: image.width, height: image.height};
            this.textures.set(image, entry);
        }
        const version = image instanceof HTMLImageElement ? image.currentSrc : image._renderVersion;
        if (version === undefined || entry.version !== version || !entry.uploaded) {
            entry.texture.needsUpdate = true;
            entry.version = version;
            entry.uploaded = true;
        }
        entry.frame = this.frame;
        return entry.texture;
    }

    quad(owner, image, points, zOffset = 0, color = 0xffffff, opacity = 1) {
        if (!this.active) return false;
        if (image && (!image.width || !image.height || (image instanceof HTMLImageElement && (!image.complete || !image.naturalWidth)))) return true;
        let entry = this.meshes.get(owner);
        if (!entry) {
            const THREE = this.THREE;
            const geometry = new THREE.BufferGeometry();
            geometry.setAttribute('position', new THREE.BufferAttribute(new Float32Array(12), 3).setUsage(THREE.DynamicDrawUsage));
            geometry.setAttribute('uv', new THREE.Float32BufferAttribute([1, 1, 1, 0, 0, 0, 0, 1], 2));
            geometry.setIndex([0, 1, 2, 0, 2, 3]);
            // Preserve the game's painter order, including stacked lands and hands
            // with separate cameras. The vertices retain real perspective depth.
            const material = new THREE.MeshBasicMaterial({transparent: true, side: THREE.DoubleSide, depthTest: false, depthWrite: false, toneMapped: false});
            material.forceSinglePass = true;
            const mesh = new THREE.Mesh(geometry, material);
            mesh.frustumCulled = false;
            this.scene.add(mesh);
            entry = {mesh};
            this.meshes.set(owner, entry);
        }
        const mesh = entry.mesh, positions = mesh.geometry.attributes.position;
        for (let i = 0; i < 4; i++) positions.setXYZ(i, points[i][0], points[i][1], points[i][2] - zOffset);
        positions.needsUpdate = true;
        mesh.material.map = image ? this.texture(image) : null;
        mesh.material.color.setHex(color);
        mesh.material.opacity = opacity;
        mesh.visible = true;
        mesh.renderOrder = ++this.order;
        entry.frame = this.frame;
        owner._battleRenderer = this;
        return true;
    }

    glow(owner, points, zOffset, color) {
        if (!this.active) return;
        let image = this.glows.get(color);
        if (!image) {
            image = document.createElement('canvas');
            image.width = image.height = 256;
            const ctx = image.getContext('2d');
            ctx.beginPath();
            if (ctx.roundRect) ctx.roundRect(28, 28, 200, 200, 12);
            else ctx.rect(28, 28, 200, 200);
            ctx.strokeStyle = ctx.shadowColor = color;
            ctx.shadowBlur = 24;
            ctx.lineWidth = 12;
            ctx.stroke();
            ctx.shadowBlur = 0;
            ctx.strokeStyle = '#efffe0';
            ctx.lineWidth = 4;
            ctx.stroke();
            image._renderVersion = 1;
            this.glows.set(color, image);
        }
        const center = points[0].map((_, axis) => points.reduce((sum, p) => sum + p[axis], 0) / 4);
        const expanded = points.map(p => p.map((v, axis) => center[axis] + (v - center[axis]) * 1.28));
        owner._glowOwner ||= {};
        const opacity = this.reducedMotion ? 1 : .9 + Math.sin(performance.now() * .003) * .1;
        this.quad(owner._glowOwner, image, expanded, zOffset, 0xffffff, opacity);
    }

    render() {
        if (!this.ready) return;
        this.drawing = false;
        this.syncViewport();
        this.surface.style.filter = this.filter;
        for (const [owner, entry] of this.meshes) {
            if (entry.frame === this.frame) continue;
            this.scene.remove(entry.mesh);
            entry.mesh.geometry.dispose();
            entry.mesh.material.dispose();
            this.meshes.delete(owner);
        }
        for (const [image, entry] of this.textures) {
            if (this.frame - entry.frame < 60) continue;
            entry.texture.dispose();
            this.textures.delete(image);
        }
        try { this.renderer.render(this.scene, this.camera); }
        catch (_) { this.dispose(); }
    }

    installTouch() {
        let pointer = null;
        this.canvas.style.touchAction = 'none';
        const mouse = (type, event) => this.canvas.dispatchEvent(new MouseEvent(type, {
            clientX: event.clientX, clientY: event.clientY, button: 0,
            buttons: type === 'mouseup' || type === 'mouseleave' ? 0 : 1
        }));
        this.canvas.addEventListener('pointerdown', event => {
            if (event.pointerType === 'mouse' || pointer !== null) return;
            event.preventDefault();
            pointer = event.pointerId;
            this.canvas.setPointerCapture(pointer);
            mouse('mousedown', event);
        });
        this.canvas.addEventListener('pointermove', event => {
            if (event.pointerId !== pointer) return;
            event.preventDefault();
            mouse('mousemove', event);
        });
        const release = event => {
            if (event.pointerId !== pointer) return;
            event.preventDefault();
            mouse(event.type === 'pointercancel' ? 'mouseleave' : 'mouseup', event);
            if (this.canvas.hasPointerCapture(pointer)) this.canvas.releasePointerCapture(pointer);
            pointer = null;
        };
        this.canvas.addEventListener('pointerup', release);
        this.canvas.addEventListener('pointercancel', release);
    }

    dispose() {
        this.ready = this.drawing = false;
        this.disposed = true;
        this.canvas.dataset.renderer = 'canvas';
        for (const {mesh} of this.meshes.values()) {
            mesh.geometry.dispose();
            mesh.material.dispose();
        }
        for (const {texture} of this.textures.values()) texture.dispose();
        this.meshes.clear();
        this.textures.clear();
        this.glows.clear();
        this.scene?.clear();
        this.renderer?.dispose();
        this.surface?.remove();
    }
}

BattleRenderer.library = import('/webpages/homepage/vendor/three.module.min.js').catch(() => null);
