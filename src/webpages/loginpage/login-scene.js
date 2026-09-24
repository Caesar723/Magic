import * as THREE from '../homepage/vendor/three.module.min.js';

// The DOM inscription is projected onto the same plane as the stone's front face.
export class LoginScene {
    constructor(canvas, stage, plane, fallback) {
        this.stage = stage; this.plane = plane;
        this.renderer = new THREE.WebGLRenderer({canvas, alpha: true, antialias: true, powerPreference: 'low-power'});
        this.renderer.outputColorSpace = THREE.SRGBColorSpace;
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(36, 1, .1, 50);
        this.camera.position.z = 11.3;
        this.scene.add(new THREE.HemisphereLight('#e9e6c9', '#405a60', 2.3));
        const light = new THREE.DirectionalLight('#e5e6ca', 1.8);
        light.position.set(-4, 6, 8); this.scene.add(light);
        this.stone = new THREE.Group(); this.scene.add(this.stone);
        this.pointer = new THREE.Vector2();
        this.matrix = new THREE.Matrix4();
        this.screen = new THREE.Matrix4();
        this.surface = new THREE.Matrix4().set(.01, 0, 0, -1.8, 0, -.01, 0, 2.7, 0, 0, 1, .232, 0, 0, 0, 1);
        this.dummy = new THREE.Object3D();
        const shape = new THREE.Shape();
        shape.moveTo(-1.69, -2.7);
        for (const [x, y] of [[1.69, -2.7], [1.8, -2.59], [1.8, 2.59], [1.69, 2.7], [-1.69, 2.7], [-1.8, 2.59], [-1.8, -2.59]]) shape.lineTo(x, y);
        shape.closePath();
        const slab = new THREE.ExtrudeGeometry(shape, {depth: .38, bevelEnabled: true, bevelThickness: .035, bevelSize: .025, bevelSegments: 1, steps: 1});
        slab.translate(0, 0, -.19);
        this.solid(slab, '#8d9d91', this.stone);
        // Shallow side bands give the bevel an inked, carved profile.
        for (const y of [-2.46, 2.46]) {
            const band = this.solid(new THREE.BoxGeometry(3.64, .065, .43), '#647d79', this.stone);
            band.position.y = y;
        }
        const foot = this.solid(new THREE.BoxGeometry(3.76, .24, .7), '#78888a', this.scene);
        foot.position.set(0, -2.88, 0); foot.rotation.y = .27;
        const base = this.solid(new THREE.BoxGeometry(4.08, .14, .94), '#526b72', this.scene);
        base.position.set(0, -3.07, 0); base.rotation.y = .27;
        for (const x of [-1.54, -.65, .9, 1.6]) {
            const cut = this.solid(new THREE.BoxGeometry(.025, .12, .015), '#3d565a', base);
            cut.position.set(x, 0, .48); cut.rotation.z = x * .07;
        }
        const shadow = new THREE.Mesh(new THREE.CircleGeometry(2.15, 40), new THREE.MeshBasicMaterial({color: '#203b42', transparent: true, opacity: .2, depthWrite: false}));
        shadow.rotation.x = -Math.PI / 2; shadow.position.y = -3.21; this.scene.add(shadow);
        this.motes = new THREE.InstancedMesh(new THREE.OctahedronGeometry(1), new THREE.MeshBasicMaterial({color: '#c2d9bb', transparent: true, opacity: .7}), 28);
        this.burst = new THREE.InstancedMesh(new THREE.OctahedronGeometry(1), new THREE.MeshBasicMaterial({color: '#ecf5cf', transparent: true, opacity: 1}), 64);
        for (const particles of [this.motes, this.burst]) { particles.instanceMatrix.setUsage(THREE.DynamicDrawUsage); particles.frustumCulled = false; this.scene.add(particles); }
        this.contextLost = event => { event.preventDefault(); fallback(); };
        canvas.addEventListener('webglcontextlost', this.contextLost);
    }
    solid(geometry, color, parent) {
        const mesh = new THREE.Mesh(geometry, new THREE.MeshToonMaterial({color})); parent.add(mesh);
        const shell = new THREE.Mesh(geometry, new THREE.MeshBasicMaterial({color: '#273d41', side: THREE.BackSide}));
        shell.scale.setScalar(1.012); mesh.add(shell);
        mesh.add(new THREE.LineSegments(new THREE.EdgesGeometry(geometry, 30), new THREE.LineBasicMaterial({color: '#2e4346'})));
        return mesh;
    }
    resize() {
        const {width, height} = this.stage.getBoundingClientRect();
        this.renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 1.5, Math.sqrt(1300000 / Math.max(1, width * height))));
        this.renderer.setSize(width, height, false);
        this.camera.aspect = width / height;
        this.camera.position.z = Math.max(10.8, 7.05 / this.camera.aspect);
        this.camera.updateProjectionMatrix(); this.camera.updateMatrixWorld();
        this.screen.set(width / 2, 0, 0, width / 2, 0, -height / 2, 0, height / 2, 0, 0, 1, 0, 0, 0, 0, 1);
    }
    project() {
        this.stone.updateMatrixWorld();
        this.matrix.copy(this.screen).multiply(this.camera.projectionMatrix).multiply(this.camera.matrixWorldInverse).multiply(this.stone.matrixWorld).multiply(this.surface);
        const m = this.matrix.elements, w = m[15];
        this.plane.style.transform = `matrix3d(${m[0] / w},${m[1] / w},0,${m[3] / w},${m[4] / w},${m[5] / w},0,${m[7] / w},0,0,1,0,${m[12] / w},${m[13] / w},0,1)`;
    }
    render(time, dt, reduced, reveal = -1) {
        if (this.disposed) return;
        const x = -.035 + (reduced ? 0 : this.pointer.y * .09), y = .27 + (reduced ? 0 : this.pointer.x * .16);
        const mix = dt ? Math.min(1, dt * 5) : 1;
        this.stone.rotation.x = THREE.MathUtils.lerp(this.stone.rotation.x, x, mix);
        this.stone.rotation.y = THREE.MathUtils.lerp(this.stone.rotation.y, y, mix);
        this.stone.rotation.z = .045;
        this.stone.position.y = reduced ? .06 : .06 + Math.sin(time * .7) * .025;
        this.project();
        this.motes.visible = !reduced;
        this.burst.visible = !reduced && reveal >= .56 && reveal < 1.9;
        if (!reduced) {
            for (let i = 0; i < this.motes.count; i++) {
                const a = i * 2.39996 + time * .04;
                this.dummy.position.set(Math.cos(a) * (1.9 + i % 5 * .1), (i * .413 + time * .13) % 6.8 - 3.3, Math.sin(a) * .9 - .5);
                this.dummy.rotation.set(a, time * .2, a * 2);
                this.dummy.scale.setScalar(.012 + i % 3 * .006); this.dummy.updateMatrix(); this.motes.setMatrixAt(i, this.dummy.matrix);
            }
            this.motes.instanceMatrix.needsUpdate = true;
            if (this.burst.visible) {
                const progress = (reveal - .56) / 1.34;
                for (let i = 0; i < this.burst.count; i++) {
                    const a = i * 2.39996, x = Math.cos(a), y = Math.sin(a);
                    const edge = Math.min(1.78 / Math.max(.01, Math.abs(x)), 2.64 / Math.max(.01, Math.abs(y)));
                    const distance = edge + progress * (.8 + i % 9 * .16);
                    this.dummy.position.set(x * distance, .08 + y * distance - progress * progress * .55, .6 + Math.sin(i * 8.3) * progress);
                    this.dummy.rotation.set(a + progress * 4, a * 2, progress * 3);
                    const size = (.028 + i % 5 * .012) * (1 - progress);
                    this.dummy.scale.set(size, size * (1.3 + i % 3 * .4), size); this.dummy.updateMatrix(); this.burst.setMatrixAt(i, this.dummy.matrix);
                }
                this.burst.instanceMatrix.needsUpdate = true;
                this.burst.material.opacity = 1 - progress * .75;
            }
        }
        this.renderer.render(this.scene, this.camera);
    }
    dispose() {
        if (this.disposed) return;
        this.disposed = true;
        this.renderer.domElement.removeEventListener('webglcontextlost', this.contextLost);
        const geometries = new Set(), materials = new Set();
        this.scene.traverse(child => { if (child.geometry) geometries.add(child.geometry); if (child.material) materials.add(child.material); });
        geometries.forEach(geometry => geometry.dispose()); materials.forEach(material => material.dispose());
        this.motes.dispose(); this.burst.dispose(); this.renderer.dispose();
    }
}
