import * as THREE from './homepage/vendor/three.module.min.js';

const INK = '#24363b';

// Shared geometry keeps shop previews identical to the packs opened in Draw Cards.
export class PackModel extends THREE.Group {
    constructor(style, texture, solid, ring) {
        super();
        this.solid = solid;
        this.ring = ring;
        this.build(style, texture);
    }
    profile(shape) {
        const lower = [[-.5, .08], [-.42, 0], [.42, 0], [.5, .08], [.5, .76]];
        const tops = {
            folio: [[.48, .97], [.4, 1], [-.4, 1], [-.5, .94]],
            crown: [[.5, .88], [.32, .88], [.23, 1], [-.23, 1], [-.32, .88], [-.5, .88]],
            slab: [[.5, .94], [.43, 1], [-.43, 1], [-.5, .94]],
            spire: [[.44, .86], [0, 1], [-.44, .86]],
            leaf: [[.42, .87], [.15, 1], [-.15, .98], [-.43, .87]],
            arch: [[.46, .9], [.3, .98], [0, 1], [-.3, .98], [-.46, .9]],
            octagon: [[.5, .82], [.28, 1], [-.28, 1], [-.5, .82]],
            wing: [[.5, .99], [.24, .91], [0, 1], [-.24, .91], [-.5, .99]]
        };
        return {bottom: [...lower, [-.5, .76]], top: [[-.5, .76], [.5, .76], ...(tops[shape] || tops.folio)]};
    }
    packPart(points, style, texture, parent, hinge = false) {
        const width = 2.05, height = 3.05, seam = height * .76;
        const shape = new THREE.Shape(points.map(([x, y]) => new THREE.Vector2(x * width, y * height)));
        const geometry = new THREE.ExtrudeGeometry(shape, {depth: style.depth, bevelEnabled: true, bevelSize: .035, bevelThickness: .035, bevelSegments: 1, steps: 1});
        geometry.translate(0, 0, -style.depth / 2);
        const mesh = this.solid(geometry, style.color, parent);
        const faceGeometry = new THREE.ShapeGeometry(shape);
        const positions = faceGeometry.attributes.position;
        const uv = faceGeometry.attributes.uv;
        for (let i = 0; i < uv.count; i++) uv.setXY(i, positions.getX(i) / width + .5, positions.getY(i) / height);
        const face = new THREE.Mesh(faceGeometry, new THREE.MeshBasicMaterial({map: texture, color: '#ffffff'}));
        face.position.z = style.depth / 2 + .039;
        mesh.add(face);
        if (hinge) mesh.position.set(0, -seam, style.depth / 2);
        return mesh;
    }
    build(style, texture) {
        const profile = this.profile(style.shape);
        this.packPart(profile.bottom, style, texture, this);
        this.lid = new THREE.Group();
        this.lid.position.set(0, 3.05 * .76, -style.depth / 2);
        this.add(this.lid);
        this.packPart(profile.top, style, texture, this.lid, true);
        // The dark recessed slot stays behind the moving lid.
        const slot = this.solid(new THREE.BoxGeometry(1.86, .035, style.depth * .72), '#263c42', this, false);
        slot.position.set(0, 3.05 * .76 + .008, 0);
        this.seal = new THREE.Group();
        this.add(this.seal);
        const seal = this.solid(new THREE.CylinderGeometry(.17, .19, .09, 10), style.trim, this.seal);
        seal.rotation.x = Math.PI / 2;
        const star = this.solid(new THREE.OctahedronGeometry(.13), INK, this.seal, false);
        star.scale.set(.65, 1.1, .15); star.position.z = .065;
        this.seal.position.set(0, 2.32, style.depth / 2 + .11);
        // Raised bindings continue over the actual sides and back.
        for (const x of [-1.047, 1.047]) {
            for (const y of [.2, 1.96]) {
                const binding = this.solid(new THREE.BoxGeometry(.06, .12, style.depth + .08), style.trim, this);
                binding.position.set(x, y, 0);
            }
        }
        const backRing = this.ring(.59, .028, style.trim, this);
        backRing.position.set(0, 1.2, -style.depth / 2 - .06);
        const backStar = this.solid(new THREE.OctahedronGeometry(.48), style.trim, this);
        backStar.scale.set(.7, 1, .08); backStar.position.set(0, 1.2, -style.depth / 2 - .07);
    }
}
