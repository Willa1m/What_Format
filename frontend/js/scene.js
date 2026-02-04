/**
 * WhatFormat - 3D Document Preview Scene
 * High-fidelity template visualization based on actual samples
 */

import * as THREE from 'three';

// ============================================
// Template Texture Generator - High Fidelity
// ============================================
class TemplateTextureGenerator {
    constructor() {
        this.width = 800;
        this.height = 1040;
    }

    _createCanvas() {
        const canvas = document.createElement('canvas');
        canvas.width = this.width;
        canvas.height = this.height;
        return canvas;
    }

    generateResumeTexture() {
        const canvas = this._createCanvas();
        const ctx = canvas.getContext('2d');
        const w = canvas.width;
        const h = canvas.height;
        
        // Background - crisp white paper
        ctx.fillStyle = '#FFFFFF';
        ctx.fillRect(0, 0, w, h);

        // Margins
        const marginLeft = 50;
        const marginRight = 50;
        const contentWidth = w - marginLeft - marginRight;
        let y = 50;

        // === Header: Name ===
        ctx.fillStyle = '#1a1a1a';
        ctx.font = 'bold 42px Georgia, serif';
        ctx.fillText('FIRSTNAME M. LASTNAME', marginLeft, y);
        y += 28;

        // Contact info (blue links)
        ctx.font = '13px Arial, sans-serif';
        ctx.fillStyle = '#0066cc';
        ctx.fillText('email@bu.com', marginLeft, y);
        ctx.fillStyle = '#333';
        ctx.fillText(' | 617-555-1234 | Boston, MA', marginLeft + 85, y);
        y += 18;
        ctx.fillStyle = '#0066cc';
        ctx.fillText('www.linkedin.com/in/sample', marginLeft, y);
        ctx.fillStyle = '#cc6600';
        ctx.fillText(' | github.com/sample', marginLeft + 175, y);
        y += 35;

        // === Section: EDUCATION ===
        this._drawSectionHeader(ctx, 'EDUCATION', marginLeft, y, contentWidth);
        y += 28;
        
        ctx.font = 'bold 13px Arial';
        ctx.fillStyle = '#333';
        ctx.fillText('Boston University | Boston, MA', marginLeft, y);
        ctx.font = '13px Arial';
        ctx.fillStyle = '#666';
        ctx.fillText('Expected December 20XX', w - marginRight - 140, y);
        y += 18;
        ctx.font = '13px Arial';
        ctx.fillStyle = '#333';
        ctx.fillText('Bachelor of Arts in Computer Science, GPA: 3.25', marginLeft, y);
        y += 18;
        ctx.font = 'italic 12px Arial';
        ctx.fillStyle = '#555';
        ctx.fillText('Relevant Coursework: Data Structures, Analysis of Algorithms, Software Engineering...', marginLeft, y);
        y += 35;

        // === Section: SKILLS ===
        this._drawSectionHeader(ctx, 'SKILLS', marginLeft, y, contentWidth);
        y += 28;
        
        ctx.font = '12px Arial';
        ctx.fillStyle = '#333';
        ctx.font = 'italic 12px Arial';
        ctx.fillText('Programming:', marginLeft, y);
        ctx.font = '12px Arial';
        ctx.fillText(' proficient in Python, Java, C#, SQL, JavaScript, XML, HTML', marginLeft + 80, y);
        y += 18;
        ctx.font = 'italic 12px Arial';
        ctx.fillText('Tools:', marginLeft, y);
        ctx.font = '12px Arial';
        ctx.fillText(' Proficient in MongoDB, PyMongo, Git, MySQL, JSON, Flask, Jinja2, Firebase', marginLeft + 38, y);
        y += 35;

        // === Section: PROJECT EXPERIENCE ===
        this._drawSectionHeader(ctx, 'PROJECT EXPERIENCE', marginLeft, y, contentWidth);
        y += 28;
        
        ctx.font = 'bold 12px Arial';
        ctx.fillStyle = '#0066cc';
        ctx.fillText('Computing Bike-friendly Neighborhoods', marginLeft, y);
        ctx.fillStyle = '#333';
        ctx.fillText(' | Boston University', marginLeft + 235, y);
        ctx.font = '12px Arial';
        ctx.fillStyle = '#666';
        ctx.fillText('Sep 20XX – Present', w - marginRight - 110, y);
        y += 18;
        ctx.fillStyle = '#444';
        ctx.fillText('• Co-developing web service using Python, PyMongo, MongoDB, JSON to measure bike friendliness...', marginLeft, y);
        y += 28;

        ctx.font = 'bold 12px Arial';
        ctx.fillStyle = '#0066cc';
        ctx.fillText('Qizmet', marginLeft, y);
        ctx.fillStyle = '#333';
        ctx.fillText(' | Boston University', marginLeft + 50, y);
        ctx.font = '12px Arial';
        ctx.fillStyle = '#666';
        ctx.fillText('Jan – May 20XX', w - marginRight - 95, y);
        y += 18;
        ctx.fillStyle = '#444';
        ctx.fillText('• Built quiz website using Flask framework with team of four; used Python to parse XML files...', marginLeft, y);
        y += 28;

        ctx.font = 'bold 12px Arial';
        ctx.fillStyle = '#0066cc';
        ctx.fillText('Text and Content Similarity Tool', marginLeft, y);
        ctx.fillStyle = '#333';
        ctx.fillText(' | Boston University', marginLeft + 200, y);
        ctx.font = '12px Arial';
        ctx.fillStyle = '#666';
        ctx.fillText('Sep – Dec 20XX', w - marginRight - 95, y);
        y += 18;
        ctx.fillStyle = '#444';
        ctx.fillText('• Developed algorithm coded in Python to compare multiple sources of written content...', marginLeft, y);
        y += 35;

        // === Section: RELEVANT EXPERIENCE ===
        this._drawSectionHeader(ctx, 'RELEVANT EXPERIENCE', marginLeft, y, contentWidth);
        y += 28;

        ctx.font = 'bold 12px Arial';
        ctx.fillStyle = '#0066cc';
        ctx.fillText('Tamarin', marginLeft, y);
        ctx.fillStyle = '#333';
        ctx.fillText(' | Boston, MA', marginLeft + 55, y);
        y += 18;
        ctx.font = 'italic 12px Arial';
        ctx.fillStyle = '#333';
        ctx.fillText('Customer Support Engineer Intern', marginLeft, y);
        ctx.font = '12px Arial';
        ctx.fillStyle = '#666';
        ctx.fillText('Jun – Aug 20XX', w - marginRight - 95, y);
        y += 18;
        ctx.fillStyle = '#444';
        ctx.fillText('• Debugged apps for customers created with the Tamarin platform in C#.', marginLeft, y);
        y += 18;
        ctx.fillText('• Found and reported bugs in Tamarin products by writing apps in Android Studio...', marginLeft, y);
        y += 28;

        ctx.font = 'bold 12px Arial';
        ctx.fillStyle = '#0066cc';
        ctx.fillText('Global App Initiative', marginLeft, y);
        ctx.fillStyle = '#333';
        ctx.fillText(' | Boston University', marginLeft + 125, y);
        y += 18;
        ctx.font = 'italic 12px Arial';
        ctx.fillStyle = '#333';
        ctx.fillText('Android Development Intern', marginLeft, y);
        ctx.font = '12px Arial';
        ctx.fillStyle = '#666';
        ctx.fillText('Oct 20XX – May 20XX', w - marginRight - 125, y);
        y += 18;
        ctx.fillStyle = '#444';
        ctx.fillText('• Used Android Studio with Java and XML to program app enabling users to submit questions...', marginLeft, y);
        y += 35;

        // === Section: LEADERSHIP EXPERIENCE ===
        this._drawSectionHeader(ctx, 'LEADERSHIP EXPERIENCE', marginLeft, y, contentWidth);
        y += 28;

        ctx.font = 'bold 12px Arial';
        ctx.fillStyle = '#0066cc';
        ctx.fillText('B.U. Learning Resource Network', marginLeft, y);
        ctx.fillStyle = '#333';
        ctx.fillText(' | Boston University', marginLeft + 200, y);
        y += 18;
        ctx.font = 'italic 12px Arial';
        ctx.fillStyle = '#333';
        ctx.fillText('Artemis Project Coordinator', marginLeft, y);
        ctx.font = '12px Arial';
        ctx.fillStyle = '#666';
        ctx.fillText('Jun – Aug 20XX', w - marginRight - 95, y);
        y += 18;
        ctx.fillStyle = '#444';
        ctx.fillText('• Designed lesson plan with three coordinators for 5-week summer program to teach and mentor...', marginLeft, y);

        // Subtle paper edge shadow
        this._addPaperEdge(ctx, w, h);

        return new THREE.CanvasTexture(canvas);
    }

    generateCoverLetterTexture() {
        const canvas = this._createCanvas();
        const ctx = canvas.getContext('2d');
        const w = canvas.width;
        const h = canvas.height;
        
        // Background - crisp white paper
        ctx.fillStyle = '#FFFFFF';
        ctx.fillRect(0, 0, w, h);

        const marginLeft = 70;
        const marginRight = 70;
        const contentWidth = w - marginLeft - marginRight;
        const centerX = w / 2;
        let y = 60;

        // === Header: Name (centered, bold) ===
        ctx.fillStyle = '#1a1a1a';
        ctx.font = 'bold 28px Georgia, serif';
        ctx.textAlign = 'center';
        ctx.fillText('Steven Sample', centerX, y);
        y += 24;

        // Contact info (centered)
        ctx.font = '13px Arial, sans-serif';
        ctx.fillStyle = '#333';
        ctx.fillText('Boston, MA', centerX, y);
        y += 18;
        ctx.fillStyle = '#006666';
        ctx.fillText('stevensample@bu.edu | 123-345-5678', centerX, y);
        y += 45;

        // Reset text align to left
        ctx.textAlign = 'left';

        // === Recipient Info ===
        ctx.font = '13px Arial';
        ctx.fillStyle = '#333';
        ctx.fillText('Diane Joly', marginLeft, y);
        y += 18;
        ctx.fillText('Research Manager', marginLeft, y);
        y += 18;
        ctx.fillText('Research Foundation for Mental Hygiene, Inc', marginLeft, y);
        y += 18;
        ctx.fillText('New York, NY', marginLeft, y);
        y += 30;

        // Date
        ctx.fillText('February 17, 20xx', marginLeft, y);
        y += 30;

        // Salutation
        ctx.fillText('Dear Ms. Joly,', marginLeft, y);
        y += 30;

        // === Body Paragraphs ===
        const paragraphs = [
            'The day I was accepted to Boston University, my grandparents cried, telling me that I was "entering through the front door," as they had illegally immigrated to the United States 20 years ago seeking medical treatment. Their hope in coming to the US was that they could obtain the help they needed to treat my grandfather\'s severe depression. Their journey has stayed with me and, since then, I have worked hard to gather the skills necessary to contribute to the field of mental health.',
            'Because this position entails interactions with adolescents, a strong candidate will need to have experience building trusting relationships with this population. Through my years as a camp counselor and, more recently, a patient advocate, I have interacted with hundreds of young people. My current position as a Patient Advocate requires me to have sensitive, confidential conversations with teenagers navigating the world of therapy.',
            'Beyond my skills in relationship building, I also have experience in lab and research settings. My position as a clinical research recruiter exposed me to the importance of accurate data collection and analysis. Since I was responsible for the details of 300 participants, I was careful and exact in my collection. I double checked information regularly and relied on cross referencing paper and computer-based tools.',
            'I not only bring the technical qualifications to be a successful research assistant, but I also bring a commitment to furthering the treatment options available for mental health disorders, especially to the people of New York. I welcome the opportunity to share more about why I think I would be a strong contributor to your team. Thank you for your time and consideration.'
        ];

        ctx.font = '12px Arial';
        ctx.fillStyle = '#333';
        const lineHeight = 18;
        const maxLineWidth = contentWidth;

        for (const para of paragraphs) {
            const lines = this._wrapText(ctx, para, maxLineWidth);
            for (const line of lines) {
                ctx.fillText(line, marginLeft, y);
                y += lineHeight;
            }
            y += 12; // paragraph spacing
        }

        // Closing
        y += 8;
        ctx.fillText('Sincerely,', marginLeft, y);
        y += 24;
        ctx.font = '13px Arial';
        ctx.fillText('Steven Sample', marginLeft, y);

        // Subtle paper edge shadow
        this._addPaperEdge(ctx, w, h);

        return new THREE.CanvasTexture(canvas);
    }

    _drawSectionHeader(ctx, title, x, y, width) {
        // Section title with underline (like the resume sample)
        ctx.font = 'bold 14px Arial, sans-serif';
        ctx.fillStyle = '#1a1a1a';
        
        // Center the title
        const textWidth = ctx.measureText(title).width;
        const centerX = x + width / 2;
        ctx.textAlign = 'center';
        ctx.fillText(title, centerX, y);
        ctx.textAlign = 'left';

        // Underline
        ctx.strokeStyle = '#cc9900';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(x, y + 6);
        ctx.lineTo(x + width, y + 6);
        ctx.stroke();
    }

    _wrapText(ctx, text, maxWidth) {
        const words = text.split(' ');
        const lines = [];
        let currentLine = '';

        for (const word of words) {
            const testLine = currentLine ? currentLine + ' ' + word : word;
            const metrics = ctx.measureText(testLine);
            
            if (metrics.width > maxWidth && currentLine) {
                lines.push(currentLine);
                currentLine = word;
            } else {
                currentLine = testLine;
            }
        }
        if (currentLine) {
            lines.push(currentLine);
        }
        return lines;
    }

    _addPaperEdge(ctx, w, h) {
        // Subtle right edge shadow for 3D effect
        const gradient = ctx.createLinearGradient(w - 15, 0, w, 0);
        gradient.addColorStop(0, 'rgba(0,0,0,0)');
        gradient.addColorStop(1, 'rgba(0,0,0,0.05)');
        ctx.fillStyle = gradient;
        ctx.fillRect(w - 15, 0, 15, h);

        // Bottom edge
        const gradientBottom = ctx.createLinearGradient(0, h - 15, 0, h);
        gradientBottom.addColorStop(0, 'rgba(0,0,0,0)');
        gradientBottom.addColorStop(1, 'rgba(0,0,0,0.05)');
        ctx.fillStyle = gradientBottom;
        ctx.fillRect(0, h - 15, w, 15);
    }
}


// ============================================
// Scene Manager - 3D Document Renderer
// ============================================
export class SceneManager {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error(`Container #${containerId} not found`);
            return;
        }

        this.textureGenerator = new TemplateTextureGenerator();
        this.textures = {
            resume: this.textureGenerator.generateResumeTexture(),
            cover_letter: this.textureGenerator.generateCoverLetterTexture()
        };

        this.init();
        this.createDocument('resume'); // Default to resume
        this.animate();
    }

    init() {
        // Scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x080808);

        // Camera
        const aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera = new THREE.PerspectiveCamera(45, aspect, 0.1, 1000);
        this.camera.position.set(0, 0, 4.5);

        // Renderer
        this.renderer = new THREE.WebGLRenderer({ 
            antialias: true,
            alpha: true 
        });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.container.appendChild(this.renderer.domElement);

        // Lighting
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        this.scene.add(ambientLight);

        const mainLight = new THREE.DirectionalLight(0xffffff, 0.8);
        mainLight.position.set(5, 5, 10);
        mainLight.castShadow = true;
        this.scene.add(mainLight);

        const fillLight = new THREE.DirectionalLight(0xE0D4C5, 0.3);
        fillLight.position.set(-5, 0, 5);
        this.scene.add(fillLight);

        // Mouse tracking
        this.mouse = { x: 0, y: 0 };
        this.targetRotation = { x: 0, y: 0 };
        
        window.addEventListener('mousemove', (e) => {
            this.mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
            this.mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
        });

        window.addEventListener('resize', () => this.onResize());
    }

    createDocument(type) {
        // Remove existing document
        if (this.documentMesh) {
            this.scene.remove(this.documentMesh);
            this.documentMesh.geometry.dispose();
            this.documentMesh.material.dispose();
        }

        // Create paper geometry (A4 proportions: 210mm x 297mm ≈ 1:1.414)
        const width = 2.1;
        const height = 2.97;
        const geometry = new THREE.PlaneGeometry(width, height, 32, 32);

        // Add subtle curve to simulate paper
        const positionAttr = geometry.attributes.position;
        for (let i = 0; i < positionAttr.count; i++) {
            const x = positionAttr.getX(i);
            const y = positionAttr.getY(i);
            // Slight curve on edges
            const z = Math.sin(x * Math.PI * 0.3) * 0.03 + Math.sin(y * Math.PI * 0.2) * 0.02;
            positionAttr.setZ(i, z);
        }
        positionAttr.needsUpdate = true;
        geometry.computeVertexNormals();

        // Material with texture
        const texture = this.textures[type] || this.textures.cover_letter;
        texture.anisotropy = this.renderer.capabilities.getMaxAnisotropy();
        
        const material = new THREE.MeshStandardMaterial({
            map: texture,
            side: THREE.DoubleSide,
            roughness: 0.8,
            metalness: 0.0,
        });

        this.documentMesh = new THREE.Mesh(geometry, material);
        this.documentMesh.castShadow = true;
        this.documentMesh.receiveShadow = true;
        
        // Initial rotation for 3D effect
        this.documentMesh.rotation.y = 0.15;
        this.documentMesh.rotation.x = -0.05;
        
        this.scene.add(this.documentMesh);

        // Animate entrance
        this.documentMesh.scale.set(0.8, 0.8, 0.8);
        this.animateEntrance();
    }

    animateEntrance() {
        const startScale = 0.8;
        const endScale = 1;
        const duration = 600;
        const startTime = Date.now();

        const animate = () => {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Ease out cubic
            const eased = 1 - Math.pow(1 - progress, 3);
            const scale = startScale + (endScale - startScale) * eased;
            
            if (this.documentMesh) {
                this.documentMesh.scale.set(scale, scale, scale);
            }

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        animate();
    }

    updateFormat(type) {
        // Map simple type names
        const typeMap = {
            'resume': 'resume',
            'cover_letter': 'cover_letter',
            'coverLetter': 'cover_letter'
        };
        const mappedType = typeMap[type] || 'cover_letter';
        this.createDocument(mappedType);
    }

    onResize() {
        if (!this.container) return;
        
        const width = this.container.clientWidth;
        const height = this.container.clientHeight;
        
        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
    }

    animate() {
        requestAnimationFrame(() => this.animate());

        if (this.documentMesh) {
            // Smooth mouse follow
            this.targetRotation.y = this.mouse.x * 0.3;
            this.targetRotation.x = this.mouse.y * 0.15;

            // Interpolate current rotation
            this.documentMesh.rotation.y += (this.targetRotation.y - this.documentMesh.rotation.y + 0.15) * 0.05;
            this.documentMesh.rotation.x += (this.targetRotation.x - this.documentMesh.rotation.x - 0.05) * 0.05;

            // Subtle float animation
            const time = Date.now() * 0.001;
            this.documentMesh.position.y = Math.sin(time * 0.5) * 0.05;
        }

        this.renderer.render(this.scene, this.camera);
    }
}
