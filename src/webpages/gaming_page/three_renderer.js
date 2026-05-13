// Three.js rendering scaffold for the gaming page.
//
// Purpose: render desktop, cards, life rings, timers, decks and particles as
// real Three.js meshes while keeping all gameplay logic, animation state and
// hit-testing (`position_in_screen`) intact. UI elements (buttons,
// action bar, selection page, win/lose, mana bar, etc.) are drawn into a
// transparent 2D overlay canvas which is composed on top of the WebGL
// canvas every frame.
//
// All gameplay objects only need to:
//   1) keep computing `arr_poses` and `position_in_screen` as before;
//   2) replace `draw()` with a Three mesh update.

class ThreeStage {
    constructor(displayCanvas, width, height, originalCamera) {
        if (typeof THREE === "undefined") {
            throw new Error("Three.js must be loaded before ThreeStage.");
        }
        this.displayCanvas = displayCanvas;
        this.width = width;
        this.height = height;
        this.origCamera = originalCamera;

        this.renderer = new THREE.WebGLRenderer({
            canvas: displayCanvas,
            antialias: true,
            alpha: false,
            preserveDrawingBuffer: false,
        });
        // Lock pixel ratio to 1: the existing mouse handling reads
        // `canvas.width` to derive logical pixel coordinates, so changing
        // the backing-store size would offset every hit test.
        this.renderer.setPixelRatio(1);
        this.renderer.setSize(width, height, false);
        this.renderer.setClearColor(0x000000, 1);
        if (THREE.sRGBEncoding) {
            this.renderer.outputEncoding = THREE.sRGBEncoding;
        }
        this.renderer.autoClear = false;

        this.scene3d = new THREE.Scene();
        // World-space VFX (magic missile discs, etc.): drawn after the main
        // battlefield scene with a cleared depth buffer so they are never
        // occluded by card depth writes, regardless of renderOrder ties.
        this.sceneVfx = new THREE.Scene();
        const fovY = 2 * Math.atan((height / 2) / 900) * 180 / Math.PI;
        this.camera3d = new THREE.PerspectiveCamera(fovY, width / height, 0.1, 100000);

        this.overlayCanvas = document.createElement("canvas");
        this.overlayCanvas.width = width;
        this.overlayCanvas.height = height;
        this.overlayCtx = this.overlayCanvas.getContext("2d");

        this.sceneOverlay = new THREE.Scene();
        this.cameraOverlay = new THREE.OrthographicCamera(
            -width / 2, width / 2, height / 2, -height / 2, -10, 10
        );

        this.overlayTexture = new THREE.CanvasTexture(this.overlayCanvas);
        this.overlayTexture.minFilter = THREE.LinearFilter;
        this.overlayTexture.magFilter = THREE.LinearFilter;
        this.overlayTexture.generateMipmaps = false;
        if (THREE.sRGBEncoding) {
            this.overlayTexture.encoding = THREE.sRGBEncoding;
        }
        const overlayMat = new THREE.MeshBasicMaterial({
            map: this.overlayTexture,
            transparent: true,
            depthTest: false,
            depthWrite: false,
        });
        const overlayMesh = new THREE.Mesh(
            new THREE.PlaneGeometry(width, height),
            overlayMat
        );
        this.sceneOverlay.add(overlayMesh);

        // Auxiliary scenes drawn between the main 3D scene and the 2D
        // overlay - each one has its own camera mirroring an original
        // project Camera (e.g. Self / Opponent hand cameras). The depth
        // buffer is cleared between scenes so each scene has its own
        // depth space and never z-fights with the table.
        this._auxScenes = []; // [{ origCamera, threeCamera, scene }]
    }

    // Returns (creating on demand) a Three Scene + PerspectiveCamera pair
    // synced to `origCamera`. Use this for renderers that need their own
    // camera (e.g. hand cards, which use Self/Opponent's private camera).
    getOrCreateAuxScene(origCamera) {
        for (const aux of this._auxScenes) {
            if (aux.origCamera === origCamera) return aux;
        }
        const fovY = 2 * Math.atan((this.height / 2) / 900) * 180 / Math.PI;
        const cam = new THREE.PerspectiveCamera(fovY, this.width / this.height, 0.1, 100000);
        const aux = {
            origCamera: origCamera,
            threeCamera: cam,
            scene: new THREE.Scene(),
        };
        this._auxScenes.push(aux);
        return aux;
    }

    _syncOneCamera(threeCam, cam) {
        const ax = cam.angle_x;
        const ay = cam.angle_y;
        const cx = Math.cos(ax), sx = Math.sin(ax);
        const cy = Math.cos(ay), sy = Math.sin(ay);
        threeCam.position.set(cam.position[0], cam.position[1], cam.position[2]);
        threeCam.up.set(0, -cy, sy);
        threeCam.lookAt(
            cam.position[0] + (-sx),
            cam.position[1] + sy * cx,
            cam.position[2] + cy * cx
        );
    }

    // Mirror the original Camera (block.js) to a Three PerspectiveCamera so
    // that screen positions produced by `Camera.similar_tri/_2` match the
    // pixel positions Three.js renders. The original camera looks toward +z
    // in its local space; Three.js cameras look toward -z. Up is along -y in
    // the original world (y points down).
    syncCamera() {
        this._syncOneCamera(this.camera3d, this.origCamera);
    }

    clearOverlay() {
        this.overlayCtx.setTransform(1, 0, 0, 1, 0, 0);
        this.overlayCtx.clearRect(0, 0, this.width, this.height);
    }

    render() {
        this.syncCamera();
        this.overlayTexture.needsUpdate = true;
        this.renderer.clear(true, true, true);
        this.renderer.render(this.scene3d, this.camera3d);
        this.renderer.clearDepth();
        this.renderer.render(this.sceneVfx, this.camera3d);
        // Aux scenes (e.g. each player's hand) layer on top of the table
        // with their own perspective camera. Depth is cleared between
        // scenes so a card in the hand is never occluded by the desktop
        // even if their world coordinates would otherwise overlap.
        for (const aux of this._auxScenes) {
            this._syncOneCamera(aux.threeCamera, aux.origCamera);
            this.renderer.clearDepth();
            this.renderer.render(aux.scene, aux.threeCamera);
        }
        this.renderer.clearDepth();
        this.renderer.render(this.sceneOverlay, this.cameraOverlay);
    }

    add(obj) { this.scene3d.add(obj); }
    remove(obj) { this.scene3d.remove(obj); }

    addVfx(obj) { this.sceneVfx.add(obj); }
    removeVfx(obj) { this.sceneVfx.remove(obj); }
}

window.THREE_STAGE = null;

// Build a CanvasTexture configured to match the project's coordinate system
// (y-down world, GL flipY off so canvas top maps to screen top).
function makeCanvasTexture(canvasOrImage, flipY) {
    const tex = new THREE.CanvasTexture(canvasOrImage);
    tex.minFilter = THREE.LinearFilter;
    tex.magFilter = THREE.LinearFilter;
    tex.generateMipmaps = false;
    tex.flipY = flipY === true;
    if (THREE.sRGBEncoding) {
        tex.encoding = THREE.sRGBEncoding;
    }
    // Some WebGL drivers skip the first upload unless this is set after the
    // canvas already has pixels; keeps hand/table cards from randomly
    // staying blank until something else touches the texture.
    tex.needsUpdate = true;
    return tex;
}

function makeImageTexture(image, flipY) {
    const tex = new THREE.Texture(image);
    tex.minFilter = THREE.LinearFilter;
    tex.magFilter = THREE.LinearFilter;
    tex.generateMipmaps = false;
    tex.flipY = flipY === true;
    if (THREE.sRGBEncoding) {
        tex.encoding = THREE.sRGBEncoding;
    }
    if (image && image.complete && image.naturalWidth > 0) {
        tex.needsUpdate = true;
    } else if (image) {
        image.addEventListener("load", () => { tex.needsUpdate = true; });
    }
    return tex;
}

// Card mesh.
//
// Design: ONE plane mesh per card, with `side = DoubleSide` and a single
// active `map`. The caller is responsible for choosing which texture is
// active each frame via `setFace(showBack)` (mirrors the original
// project's `Card.check_surface()` logic).
//
// Two-mesh / FrontSide+BackSide setups were tried earlier but interact
// badly with `transparent: true` + Three's renderer: depending on the
// renderer pass order one mesh would cull the other and the card would
// disappear entirely. Using a single DoubleSide mesh side-steps all of
// that and matches what the legacy 2D renderer was doing anyway (it
// just drew different bitmaps onto the same quad).
//
// Orientation:
//   - Default plane normal is +Z. We never rotate the geometry.
//   - Hand-card front canvases are produced by `Card_frame.generate_card`
//     with a negative-Y CSS transform, i.e. the canvas pixel rows are
//     already vertically flipped (image bottom -> canvas top). Combined
//     with Three's default `flipY=true` upload that ends up right-side
//     up on the plane.
//   - Card backs (`back_img`) and battle canvases are NOT pre-flipped;
//     they rely entirely on `flipY=true` for upright orientation.
class CardPlane {
    constructor(stage, halfW, halfH, frontSource, backSource, opts) {
        opts = opts || {};
        this.stage = stage;
        this.parent = opts.parent || stage.scene3d;
        this.halfW = halfW;
        this.halfH = halfH;
        this.flat = opts.flat === true;

        this.frontTexture = (frontSource instanceof HTMLCanvasElement)
            ? makeCanvasTexture(frontSource, true)
            : makeImageTexture(frontSource, true);
        // Battle cards never reveal a back, so we don't bother allocating
        // a back texture for them.
        if (!this.flat && backSource) {
            this.backTexture = (backSource instanceof HTMLCanvasElement)
                ? makeCanvasTexture(backSource, true)
                : makeImageTexture(backSource, true);
        }

        this.geometry = new THREE.PlaneGeometry(halfW * 2, halfH * 2);
        // Hand aux scenes: multiple semi-transparent quads overlap. With the
        // default depth buffer, later cards can clip a dragged / enlarged
        // card along its silhouette. `handDepthMode` turns off depth writes
        // (and tests) so draw order is controlled purely by `renderOrder`.
        const handDepthMode = opts.handDepthMode === true;
        this.material = new THREE.MeshBasicMaterial({
            map: this.frontTexture,
            side: THREE.DoubleSide,
            transparent: true,
            depthWrite: handDepthMode ? false : true,
            depthTest: handDepthMode ? false : true,
            polygonOffset: true,
            polygonOffsetFactor: opts.polygonOffsetFactor !== undefined ? opts.polygonOffsetFactor : -1,
            polygonOffsetUnits: opts.polygonOffsetUnits !== undefined ? opts.polygonOffsetUnits : -1,
        });
        // Backwards-compat alias: existing code refers to `frontMaterial`.
        this.frontMaterial = this.material;
        this.mesh = new THREE.Mesh(this.geometry, this.material);
        this.frontMesh = this.mesh;
        this.group = new THREE.Group();
        this.group.add(this.mesh);
        this.group.renderOrder = 0;
        this.parent.add(this.group);

        this._showingBack = false;
    }

    setVisible(v) { this.group.visible = v; }

    setRenderOrder(o) {
        this.group.renderOrder = o;
        this.mesh.renderOrder = o;
    }

    // Battlefield drag: table mesh still depth-tests against the card; turn
    // off depth read/write so renderOrder alone keeps the card fully visible.
    setDepthReadWrite(depthTest, depthWrite) {
        this.material.depthTest = depthTest;
        this.material.depthWrite = depthWrite;
        this.material.needsUpdate = true;
    }

    // Stacked lands: push each copy slightly in depth buffer without huge world-Z.
    setPolygonOffset(factor, units) {
        this.material.polygonOffset = true;
        this.material.polygonOffsetFactor = factor;
        this.material.polygonOffsetUnits = units;
        this.material.needsUpdate = true;
    }

    // Switch which texture is shown. true => card back. false => card front.
    // Cheap (no-op) when state is unchanged. Swapping `material.map` does
    // not require `material.needsUpdate` because the shader signature is
    // unchanged (only the bound texture differs).
    setFace(showBack) {
        const want = (showBack === true) && !!this.backTexture;
        if (want === this._showingBack) return;
        this._showingBack = want;
        this.material.map = want ? this.backTexture : this.frontTexture;
    }

    // pos: [x,y,z] world. angles in radians. Original project applies
    // R = R_x(angle_x) * R_y(angle_y) * R_z(angle_z) to local corners, which
    // matches a Three.js Euler in 'XYZ' (intrinsic) order.
    setTransform(pos, ax, ay, az, scaleX, scaleY) {
        this.group.position.set(pos[0], pos[1], pos[2]);
        this.group.rotation.set(ax, ay, az, "XYZ");
        if (scaleY === undefined) scaleY = scaleX;
        this.group.scale.set(scaleX, scaleY, scaleX);
    }

    markFrontDirty() { if (this.frontTexture) this.frontTexture.needsUpdate = true; }
    markBackDirty() { if (this.backTexture) this.backTexture.needsUpdate = true; }

    dispose() {
        if (this.group.parent) this.group.parent.remove(this.group);
        this.geometry.dispose();
        if (this.material) this.material.dispose();
        if (this.frontTexture) this.frontTexture.dispose();
        if (this.backTexture) this.backTexture.dispose();
    }
}

// Single-sided plane (no back face needed): used for desktop, life ring,
// timer, deck top, etc.
class TexturedPlane {
    constructor(stage, source, opts) {
        opts = opts || {};
        this.stage = stage;
        const flipY = opts.flipY === true;
        this.texture = (source instanceof HTMLCanvasElement)
            ? makeCanvasTexture(source, flipY)
            : makeImageTexture(source, flipY);
        const matOpts = {
            map: this.texture,
            side: opts.side || THREE.DoubleSide,
            transparent: opts.transparent !== false,
            depthWrite: opts.depthWrite === true,
            opacity: opts.opacity !== undefined ? opts.opacity : 1.0,
        };
        if (opts.polygonOffsetFactor !== undefined || opts.polygonOffsetUnits !== undefined) {
            matOpts.polygonOffset = true;
            matOpts.polygonOffsetFactor = opts.polygonOffsetFactor || 0;
            matOpts.polygonOffsetUnits = opts.polygonOffsetUnits || 0;
        }
        this.material = new THREE.MeshBasicMaterial(matOpts);
        this.geometry = new THREE.PlaneGeometry(opts.width || 1, opts.height || 1);
        this.mesh = new THREE.Mesh(this.geometry, this.material);
        this.mesh.renderOrder = opts.renderOrder || 0;
        this.parent = opts.parent || stage.scene3d;
        this.parent.add(this.mesh);
    }

    setSize(width, height) {
        this.geometry.dispose();
        this.geometry = new THREE.PlaneGeometry(width, height);
        this.mesh.geometry = this.geometry;
    }

    setTransform(pos, ax, ay, az, scaleX, scaleY, scaleZ) {
        this.mesh.position.set(pos[0], pos[1], pos[2]);
        this.mesh.rotation.set(ax || 0, ay || 0, az || 0, "XYZ");
        if (scaleY === undefined) scaleY = scaleX;
        if (scaleZ === undefined) scaleZ = scaleX;
        this.mesh.scale.set(scaleX, scaleY, scaleZ);
    }

    setVisible(v) { this.mesh.visible = v; }

    setOpacity(o) { this.material.opacity = o; this.material.transparent = o < 1.0; }

    markDirty() { this.texture.needsUpdate = true; }

    dispose() {
        if (this.mesh.parent) this.mesh.parent.remove(this.mesh);
        this.geometry.dispose();
        this.material.dispose();
        this.texture.dispose();
    }
}

// Battlefield `CardPlane` uses renderOrder up to ~4000 when dragging; magic
// missile / particle discs must paint above all table cards in the same scene.
const EFFECT_PARTICLE_RENDER_ORDER_BASE = 12000;
if (typeof window !== "undefined") {
    window.EFFECT_PARTICLE_RENDER_ORDER_BASE = EFFECT_PARTICLE_RENDER_ORDER_BASE;
}

// A small soft-disc sprite, used for magic missile particles.
class ParticleSprite {
    constructor(stage) {
        this.stage = stage;
        this.material = new THREE.SpriteMaterial({
            map: ParticleSprite.getSharedTexture(),
            color: 0xffffff,
            transparent: true,
            depthWrite: false,
            depthTest: false,
        });
        this.sprite = new THREE.Sprite(this.material);
        this.sprite.renderOrder = EFFECT_PARTICLE_RENDER_ORDER_BASE;
        if (typeof stage.addVfx === "function") stage.addVfx(this.sprite);
        else stage.add(this.sprite);
    }

    static getSharedTexture() {
        if (ParticleSprite._tex) return ParticleSprite._tex;
        const c = document.createElement("canvas");
        c.width = 64;
        c.height = 64;
        const g = c.getContext("2d");
        const grad = g.createRadialGradient(32, 32, 0, 32, 32, 30);
        grad.addColorStop(0.0, "rgba(255,255,255,1)");
        grad.addColorStop(0.4, "rgba(255,255,255,0.7)");
        grad.addColorStop(1.0, "rgba(255,255,255,0)");
        g.fillStyle = grad;
        g.fillRect(0, 0, 64, 64);
        const tex = new THREE.CanvasTexture(c);
        tex.minFilter = THREE.LinearFilter;
        tex.magFilter = THREE.LinearFilter;
        if (THREE.sRGBEncoding) tex.encoding = THREE.sRGBEncoding;
        ParticleSprite._tex = tex;
        return tex;
    }

    // Accepts "rgb(r,g,b)", "rgba(r,g,b,a)", "rgb(r,g,b,a)" (some particles
    // in the project use this non-standard form).
    setColor(cssColor) {
        const m = cssColor.match(/-?\d+(?:\.\d+)?/g);
        if (!m) return;
        const r = parseFloat(m[0]);
        const g = parseFloat(m[1]);
        const b = parseFloat(m[2]);
        const a = m.length >= 4 ? parseFloat(m[3]) : 1.0;
        this.material.color.setRGB(r / 255, g / 255, b / 255);
        this.material.opacity = Math.max(0, Math.min(1, a));
    }

    setTransform(pos, sizeWorld) {
        this.sprite.position.set(pos[0], pos[1], pos[2]);
        this.sprite.scale.set(sizeWorld, sizeWorld, sizeWorld);
    }

    dispose() {
        if (typeof this.stage.removeVfx === "function") this.stage.removeVfx(this.sprite);
        else this.stage.remove(this.sprite);
        this.material.dispose();
    }
}

// Translucent quad of arbitrary world-space corners. Used for the cast
// shadow under a battle card, where the four corners are computed by the
// project's existing shadow projection math. Three.js reconstructs the quad
// via a BufferGeometry rebuilt every frame.
class ShadowQuad {
    constructor(stage) {
        this.stage = stage;
        this.geometry = new THREE.BufferGeometry();
        this.positions = new Float32Array(12);
        this.indices = new Uint16Array([0, 1, 2, 0, 2, 3]);
        this.geometry.setAttribute("position", new THREE.BufferAttribute(this.positions, 3));
        this.geometry.setIndex(new THREE.BufferAttribute(this.indices, 1));
        this.material = new THREE.MeshBasicMaterial({
            color: 0x171717,
            transparent: true,
            opacity: 0.6,
            depthWrite: false,
            side: THREE.DoubleSide,
        });
        this.mesh = new THREE.Mesh(this.geometry, this.material);
        this.mesh.renderOrder = -1;
        stage.add(this.mesh);
    }

    setCorners(corners4) {
        for (let i = 0; i < 4; i++) {
            this.positions[i * 3 + 0] = corners4[i][0];
            this.positions[i * 3 + 1] = corners4[i][1];
            this.positions[i * 3 + 2] = corners4[i][2];
        }
        this.geometry.attributes.position.needsUpdate = true;
        this.geometry.computeBoundingSphere();
    }

    setVisible(v) { this.mesh.visible = v; }

    dispose() {
        this.stage.remove(this.mesh);
        this.geometry.dispose();
        this.material.dispose();
    }
}

// Helper used by every object's `draw()` to compute screen-space corners of
// its rectangle for hit testing. Mirrors the original projection so existing
// `position_in_screen` based code still works.
function project_quad_to_screen(arr_poses_cam_space, camera, canvasWidth, canvasHeight) {
    const cx = canvasWidth / 2;
    const cy = canvasHeight / 2;
    const out = [];
    const zs = [];
    for (let i = 0; i < arr_poses_cam_space.length; i++) {
        const x = arr_poses_cam_space[i][0];
        const y = arr_poses_cam_space[i][1];
        const z = arr_poses_cam_space[i][2];
        out.push([cx + camera.similar_tri_2(x, z), cy + camera.similar_tri_2(y, z)]);
        zs.push(z);
    }
    return [out, zs];
}

function project_quad_to_screen_world(arr_poses_world, camera, canvasWidth, canvasHeight) {
    const cx = canvasWidth / 2;
    const cy = canvasHeight / 2;
    const out = [];
    const zs = [];
    for (let i = 0; i < arr_poses_world.length; i++) {
        const x = arr_poses_world[i][0];
        const y = arr_poses_world[i][1];
        const z = arr_poses_world[i][2];
        out.push([cx + camera.similar_tri(x, z), cy + camera.similar_tri(y, z)]);
        zs.push(z);
    }
    return [out, zs];
}

window.ThreeStage = ThreeStage;
window.CardPlane = CardPlane;
window.TexturedPlane = TexturedPlane;
window.ParticleSprite = ParticleSprite;
window.ShadowQuad = ShadowQuad;
window.project_quad_to_screen = project_quad_to_screen;
window.project_quad_to_screen_world = project_quad_to_screen_world;
window.makeCanvasTexture = makeCanvasTexture;
window.makeImageTexture = makeImageTexture;

console.log("[three_renderer.js] loaded. THREE =", typeof THREE !== "undefined" ? THREE.REVISION : "undefined");
