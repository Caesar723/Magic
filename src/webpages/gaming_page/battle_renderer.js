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
        this.installBackdrop();
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
        this.renderer = new THREE.WebGLRenderer({canvas: this.surface, alpha: true, antialias: true, depth: false, powerPreference: 'high-performance'});
        // Logical canvas dimensions also define every existing pointer hit test.
        this.renderer.setPixelRatio(1);
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
        this.resize(this.canvas.width, this.canvas.height);
    }

    get active() { return this.ready && this.drawing; }
    get reducedMotion() { return this.motion.matches; }

    installBackdrop() {
        // Full-screen battles share gaming.css; Studio retains its own viewport frame.
        if (this.canvas.parentElement.id !== 'canvasContainer') return;
        const backdrop = document.createElement('div');
        backdrop.className = 'battle-backdrop';
        backdrop.setAttribute('aria-hidden', 'true');
        for (const layer of ['far', 'near']) {
            const cloud = document.createElement('div');
            cloud.className = 'battle-clouds battle-clouds--' + layer;
            backdrop.append(cloud);
        }
        for (const [kind, source] of [['distant', 'tower'], ['distant-right', 'arch'], ['tower', 'tower'], ['arch', 'arch']]) {
            const image = new Image();
            image.alt = '';
            image.className = 'battle-ruin battle-ruin--' + kind;
            image.src = '/webpages/gaming_page/art/sky-' + source + '.webp';
            image.draggable = false;
            backdrop.append(image);
            window.PageTransition?.image(image);
        }
        const dust = document.createElement('div');
        dust.className = 'battle-dust';
        for (let i = 0; i < 24; i++) {
            const mote = document.createElement('i');
            const x = i % 3 === 0 ? 18 + i * 17 % 64 : i % 2 ? 2 + i * 7 % 10 : 88 + i * 3 % 10;
            mote.style.cssText = `--x:${x}%;--y:${8 + i * 29 % 88}%;--size:${2 + i % 2}px;--duration:${9 + i % 7}s;--delay:${-i * 1.7}s;--drift:${12 + i % 5 * 6}px`;
            dust.append(mote);
        }
        backdrop.append(dust);
        this.canvas.before(backdrop);
        const pause = event => backdrop.classList.toggle('is-paused', event?.type === 'blur' || document.hidden || !document.hasFocus());
        window.addEventListener('blur', pause);
        window.addEventListener('focus', pause);
        document.addEventListener('visibilitychange', pause);
        pause();
    }

    resize(width, height) {
        if (!this.ready) return;
        const bounds = this.canvas.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, 2);
        const w = (bounds.width || width) * dpr, h = (bounds.height || height) * dpr;
        const limit = Math.min(4096, this.renderer.capabilities.maxTextureSize);
        const scale = Math.min(1, limit / Math.max(w, h), Math.sqrt(8388608 / (w * h)));
        this.renderer.setSize(Math.max(1, Math.floor(w * scale)), Math.max(1, Math.floor(h * scale)), false);
        this.camera.aspect = width / height;
        this.camera.fov = 2 * Math.atan(height / 1800) * 180 / Math.PI;
        this.camera.updateProjectionMatrix();
        this.viewportStyle = null;
        this.syncViewport();
    }

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

    createTexture(image) {
        const texture = new this.THREE.Texture(image);
        texture.flipY = false;
        texture.colorSpace = this.THREE.SRGBColorSpace;
        const artwork = image instanceof HTMLImageElement;
        texture.minFilter = artwork ? this.THREE.LinearMipmapLinearFilter : this.THREE.LinearFilter;
        texture.magFilter = this.THREE.LinearFilter;
        texture.generateMipmaps = artwork;
        texture.anisotropy = artwork ? Math.min(8, this.renderer.capabilities.getMaxAnisotropy() || 1) : 1;
        return texture;
    }

    texture(image) {
        let entry = this.textures.get(image);
        if (entry && (entry.width !== image.width || entry.height !== image.height)) {
            entry.texture.dispose();
            this.textures.delete(image);
            entry = null;
        }
        if (!entry) {
            entry = {texture: this.createTexture(image), width: image.width, height: image.height};
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

    textTexture(owner, image) {
        // Prefilter text at its projected pixel size, avoiding both undersampling
        // the original and blending overly small mip levels into fine glyphs.
        const p = owner.position_in_screen, sx = this.surface.width / this.canvas.width, sy = this.surface.height / this.canvas.height;
        const edge = (a, b) => Math.hypot((p[a][0] - p[b][0]) * sx, (p[a][1] - p[b][1]) * sy);
        const width = Math.max(1, Math.min(image.width, Math.ceil(Math.max(edge(0, 3), edge(1, 2)) / 4) * 4));
        const height = Math.max(1, Math.min(image.height, Math.ceil(Math.max(edge(0, 1), edge(2, 3)) / 4) * 4));
        let entry = this.textures.get(owner);
        // A small tolerance prevents reallocating textures for subpixel motion.
        if (!entry || entry.image !== image || Math.abs(entry.width - width) > 4 || Math.abs(entry.height - height) > 4) {
            entry?.texture.dispose();
            const canvas = Object.assign(document.createElement('canvas'), {width, height});
            const ctx = canvas.getContext('2d');
            ctx.imageSmoothingQuality = 'high';
            entry = {image, width, height, canvas, ctx, texture: this.createTexture(canvas)};
            // Preserve glyph coverage while interpolating the prefiltered face.
            // The face material decodes sRGB after sampling rather than before it.
            entry.texture.internalFormat = 'RGBA8';
            this.textures.set(owner, entry);
        }
        if (!entry.uploaded || image._renderVersion === undefined || entry.version !== image._renderVersion) {
            entry.ctx.clearRect(0, 0, entry.width, entry.height);
            entry.ctx.drawImage(image, 0, 0, entry.width, entry.height);
            entry.texture.needsUpdate = true;
            entry.version = image._renderVersion;
            entry.uploaded = true;
        }
        entry.frame = this.frame;
        return entry.texture;
    }

    quad(owner, image, points, zOffset = 0, color = 0xffffff, opacity = 1, text = false) {
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
            const textSampling = {value: false};
            if (text) {
                material.onBeforeCompile = shader => {
                    shader.uniforms.battleTextSampling = textSampling;
                    const map = THREE.ShaderChunk.map_fragment.replace('diffuseColor *= sampledDiffuseColor;', 'if (battleTextSampling) sampledDiffuseColor = sRGBTransferEOTF(sampledDiffuseColor);\n\tdiffuseColor *= sampledDiffuseColor;');
                    shader.fragmentShader = 'uniform bool battleTextSampling;\n' + shader.fragmentShader.replace('#include <map_fragment>', map);
                };
            }
            const mesh = new THREE.Mesh(geometry, material);
            mesh.frustumCulled = false;
            this.scene.add(mesh);
            entry = {mesh, textSampling};
            this.meshes.set(owner, entry);
        }
        const mesh = entry.mesh, positions = mesh.geometry.attributes.position;
        for (let i = 0; i < 4; i++) positions.setXYZ(i, points[i][0], points[i][1], points[i][2] - zOffset);
        positions.needsUpdate = true;
        entry.textSampling.value = text && image instanceof HTMLCanvasElement;
        mesh.material.map = image ? (text && image instanceof HTMLCanvasElement ? this.textTexture(owner, image) : this.texture(image)) : null;
        mesh.material.color.setHex(color);
        mesh.material.opacity = opacity;
        mesh.visible = true;
        mesh.renderOrder = ++this.order;
        entry.frame = this.frame;
        owner._battleRenderer = this;
        return true;
    }

    static drawOutline(ctx, points, color) {
        const edge = Math.min(...points.map((p, i) => Math.hypot(p[0] - points[(i + 1) % 4][0], p[1] - points[(i + 1) % 4][1])));
        ctx.save();
        ctx.beginPath();
        points.forEach((p, i) => i ? ctx.lineTo(...p) : ctx.moveTo(...p));
        ctx.closePath();
        ctx.lineJoin = 'round';
        ctx.shadowColor = color;
        ctx.shadowBlur = Math.min(12, edge * .05);
        ctx.lineWidth = Math.max(.75, Math.min(3, edge * .012));
        ctx.strokeStyle = color;
        ctx.globalAlpha *= .95;
        ctx.stroke();
        ctx.stroke();
        ctx.stroke();
        ctx.shadowBlur = 0;
        ctx.strokeStyle = '#e3ffe9';
        ctx.lineWidth *= .4;
        ctx.stroke();
        ctx.restore();
    }

    glow(owner, points, zOffset, color) {
        if (!this.active) return;
        let image = this.glows.get(color);
        if (!image) {
            image = document.createElement('canvas');
            image.width = image.height = 352;
            BattleRenderer.drawOutline(image.getContext('2d'), [[304, 304], [304, 48], [48, 48], [48, 304]], color);
            image._renderVersion = 1;
            this.glows.set(color, image);
        }
        // Transparent padding holds only the fading halo; its bright contour
        // maps back to the card's exact edge, without an enlarged backplate.
        const center = points[0].map((_, axis) => points.reduce((sum, p) => sum + p[axis], 0) / 4);
        const halo = points.map(p => p.map((v, axis) => center[axis] + (v - center[axis]) * (352 / 256)));
        owner._glowOwner ||= {};
        const opacity = this.reducedMotion ? 1 : .96 + Math.sin(performance.now() * .0015) * .04;
        this.quad(owner._glowOwner, image, halo, zOffset, 0xffffff, opacity);
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
