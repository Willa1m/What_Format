import * as THREE from 'https://unpkg.com/three@0.160.0/build/three.module.js';

export class HomeBackground {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) return;

        this.scene = new THREE.Scene();
        this.scene.fog = new THREE.FogExp2(0x080808, 0.05); // Deep fog

        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.camera.position.z = 20;

        this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.container.appendChild(this.renderer.domElement);

        // Particles
        this.particles = [];
        this.particleGroup = new THREE.Group();
        this.createParticles();
        this.scene.add(this.particleGroup);

        // Mouse interaction
        this.mouseX = 0;
        this.mouseY = 0;
        this.targetX = 0;
        this.targetY = 0;

        window.addEventListener('mousemove', (e) => this.onMouseMove(e));
        window.addEventListener('resize', () => this.onResize());

        this.animate();
    }

    createParticles() {
        const particleCount = 200; // Reduced from 400 for cleaner look
        // Paper sheet geometry
        const geometry = new THREE.PlaneGeometry(0.4, 0.6); 
        const material = new THREE.MeshBasicMaterial({ 
            color: 0xE0D4C5, 
            side: THREE.DoubleSide,
            transparent: true,
            opacity: 0.4 // Reduced from 0.6 for cleaner look
        });

        for (let i = 0; i < particleCount; i++) {
            const mesh = new THREE.Mesh(geometry, material);
            
            // Random position in a sphere distribution
            const r = 15 + Math.random() * 20;
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos(2 * Math.random() - 1);

            mesh.position.x = r * Math.sin(phi) * Math.cos(theta);
            mesh.position.y = r * Math.sin(phi) * Math.sin(theta);
            mesh.position.z = r * Math.cos(phi);

            // Random rotation
            mesh.rotation.x = Math.random() * Math.PI;
            mesh.rotation.y = Math.random() * Math.PI;

            // Store custom data for animation
            mesh.userData = {
                velocity: Math.random() * 0.02 + 0.01,
                axis: new THREE.Vector3(Math.random(), Math.random(), Math.random()).normalize()
            };

            this.particleGroup.add(mesh);
            this.particles.push(mesh);
        }
    }

    onMouseMove(event) {
        this.mouseX = (event.clientX - window.innerWidth / 2) * 0.001;
        this.mouseY = (event.clientY - window.innerHeight / 2) * 0.001;
    }

    onResize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }

    animate() {
        requestAnimationFrame(this.animate.bind(this));

        // Smooth camera movement based on mouse
        this.targetX = this.mouseX * 5;
        this.targetY = this.mouseY * 5;

        this.camera.position.x += (this.targetX - this.camera.position.x) * 0.05;
        this.camera.position.y += (-this.targetY - this.camera.position.y) * 0.05;
        this.camera.lookAt(this.scene.position);

        // Rotate entire group slowly
        this.particleGroup.rotation.y += 0.002;
        this.particleGroup.rotation.z += 0.001;

        // Animate individual particles
        this.particles.forEach(p => {
            p.rotation.x += 0.01;
            p.rotation.y += 0.01;
        });

        this.renderer.render(this.scene, this.camera);
    }
}
