from panspace import version as VERSION
# -----------------------------
# 3D Swarming Bacteria Sphere
# -----------------------------
html_swarm_sphere = """
<div id="container"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({alpha: true, antialias:true});
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Particle system
const particleCount = 500;
const particles = new THREE.BufferGeometry();
const positions = [];
const velocities = [];

for (let i = 0; i < particleCount; i++) {
    const theta = Math.random() * 2 * Math.PI;
    const phi = Math.acos(2 * Math.random() - 1);
    const r = 2 + Math.random() * 0.5;  // radius around sphere

    const x = r * Math.sin(phi) * Math.cos(theta);
    const y = r * Math.sin(phi) * Math.sin(theta);
    const z = r * Math.cos(phi);
    positions.push(x, y, z);

    // random velocities for swarming
    velocities.push((Math.random()-0.5)*0.01, (Math.random()-0.5)*0.01, (Math.random()-0.5)*0.01);
}

particles.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));

const material = new THREE.PointsMaterial({color: 0x00ffcc, size: 0.05});
const pointCloud = new THREE.Points(particles, material);
scene.add(pointCloud);

camera.position.z = 6;

// Animate swarming particles
function animate() {
    requestAnimationFrame(animate);
    const positions = pointCloud.geometry.attributes.position.array;
    for (let i = 0; i < particleCount; i++) {
        positions[3*i] += velocities[3*i];
        positions[3*i+1] += velocities[3*i+1];
        positions[3*i+2] += velocities[3*i+2];

        // simple spherical constraint
        const r = Math.sqrt(positions[3*i]**2 + positions[3*i+1]**2 + positions[3*i+2]**2);
        const factor = 2 / r; // sphere radius = 2
        positions[3*i] *= factor;
        positions[3*i+1] *= factor;
        positions[3*i+2] *= factor;
    }
    pointCloud.geometry.attributes.position.needsUpdate = true;
    pointCloud.rotation.y += 0.001;  // slow rotation
    renderer.render(scene, camera);
}

animate();
</script>
"""


html_3d_sphere_logo = """
<div id="container"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://threejs.org/examples/js/loaders/FontLoader.js"></script>
<script src="https://threejs.org/examples/js/geometries/TextGeometry.js"></script>

<script>
// Scene setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({alpha: true, antialias: true});
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Particle system
const particleCount = 500;
const geometry = new THREE.BufferGeometry();
const positions = [];
const colorArray = [];
const velocities = [];

// Colors sampled from your logo (replace with actual colors)
const colors = [0x195b6a, 0x718363, 0x428e97, 0x58867b, 0x58867b];

for (let i = 0; i < particleCount; i++) {
    const theta = Math.random() * 2 * Math.PI;
    const phi = Math.acos(2 * Math.random() - 1);
    const r = 2 + Math.random() * 0.5;

    const x = r * Math.sin(phi) * Math.cos(theta);
    const y = r * Math.sin(phi) * Math.sin(theta);
    const z = r * Math.cos(phi);
    positions.push(x, y, z);

    // Particle color
    const color = new THREE.Color(colors[Math.floor(Math.random()*colors.length)]);
    colorArray.push(color.r, color.g, color.b);

    // Random velocities
    velocities.push((Math.random()-0.5)*0.01, (Math.random()-0.5)*0.01, (Math.random()-0.5)*0.01);
}

geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
geometry.setAttribute('color', new THREE.Float32BufferAttribute(colorArray, 3));

const material = new THREE.PointsMaterial({size:0.05, vertexColors:true});
const pointCloud = new THREE.Points(geometry, material);
scene.add(pointCloud);

camera.position.z = 4;

// Add "Panspace" text in the center
const loader = new THREE.FontLoader();
loader.load('https://threejs.org/examples/fonts/helvetiker_regular.typeface.json', function(font) {
    const textGeometry = new THREE.TextGeometry('panspace', {
        font: font,
        size: 0.5,
        height: 0.1,
    });
    const textMaterial = new THREE.MeshBasicMaterial({color: 0xffffff});
    const mesh = new THREE.Mesh(textGeometry, textMaterial);
    mesh.position.set(-1.5, -0.25, 0); // adjust center
    scene.add(mesh);
});

// Animate particles
function animate() {
    requestAnimationFrame(animate);
    const positions = pointCloud.geometry.attributes.position.array;
    for (let i = 0; i < particleCount; i++) {
        positions[3*i] += velocities[3*i];
        positions[3*i+1] += velocities[3*i+1];
        positions[3*i+2] += velocities[3*i+2];

        // keep particles near sphere radius = 2
        const r = Math.sqrt(positions[3*i]**2 + positions[3*i+1]**2 + positions[3*i+2]**2);
        const factor = 2 / r;
        positions[3*i] *= factor;
        positions[3*i+1] *= factor;
        positions[3*i+2] *= factor;
    }
    pointCloud.geometry.attributes.position.needsUpdate = true;
    pointCloud.rotation.y += 0.001; // slow rotation
    renderer.render(scene, camera);
}

animate();
</script>
"""
