import { useEffect, useRef } from 'react';
import * as THREE from 'three';

export default function CornerGlobe() {
    const containerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (!containerRef.current) return;

        const globeWidth = 1400;
        const globeHeight = 1400;

        // Scene setup
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(
            75,
            globeWidth / globeHeight,
            0.1,
            1000
        );
        camera.position.z = 2.5;

        const renderer = new THREE.WebGLRenderer({
            antialias: true,
            alpha: true,
            precision: 'lowp'
        });
        renderer.setSize(globeWidth, globeHeight);
        renderer.setClearColor(0x000000, 0);
        containerRef.current.appendChild(renderer.domElement);

        // Create globe
        const geometry = new THREE.IcosahedronGeometry(1, 64);

        // Create canvas texture for the globe
        const canvas = document.createElement('canvas');
        canvas.width = 2048;
        canvas.height = 1024;
        const ctx = canvas.getContext('2d');
        if (ctx) {
            // Blue background for water
            ctx.fillStyle = '#1e3a8a';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Land masses - more realistic country/continent shapes
            ctx.fillStyle = '#0ea5e9';

            // North America
            ctx.beginPath();
            ctx.moveTo(200, 250);
            ctx.bezierCurveTo(250, 200, 320, 220, 350, 280);
            ctx.bezierCurveTo(380, 320, 360, 400, 320, 420);
            ctx.bezierCurveTo(280, 410, 220, 380, 190, 330);
            ctx.bezierCurveTo(170, 300, 180, 270, 200, 250);
            ctx.fill();

            // South America
            ctx.beginPath();
            ctx.moveTo(280, 420);
            ctx.bezierCurveTo(320, 430, 340, 480, 330, 550);
            ctx.bezierCurveTo(315, 620, 280, 680, 250, 700);
            ctx.bezierCurveTo(240, 650, 250, 550, 270, 480);
            ctx.bezierCurveTo(280, 450, 285, 430, 280, 420);
            ctx.fill();

            // Europe & Africa
            ctx.beginPath();
            ctx.moveTo(900, 180);
            ctx.bezierCurveTo(950, 170, 1000, 190, 1020, 250);
            ctx.bezierCurveTo(1040, 320, 1030, 400, 1000, 480);
            ctx.bezierCurveTo(980, 540, 920, 580, 880, 600);
            ctx.bezierCurveTo(850, 620, 800, 610, 800, 550);
            ctx.bezierCurveTo(800, 480, 820, 400, 850, 320);
            ctx.bezierCurveTo(880, 240, 920, 190, 900, 180);
            ctx.fill();

            // Asia
            ctx.beginPath();
            ctx.moveTo(1200, 150);
            ctx.bezierCurveTo(1300, 140, 1400, 180, 1450, 250);
            ctx.bezierCurveTo(1480, 320, 1470, 400, 1420, 450);
            ctx.bezierCurveTo(1350, 480, 1250, 450, 1210, 380);
            ctx.bezierCurveTo(1190, 300, 1200, 200, 1200, 150);
            ctx.fill();

            // Australia
            ctx.beginPath();
            ctx.moveTo(1600, 480);
            ctx.bezierCurveTo(1650, 470, 1700, 490, 1720, 540);
            ctx.bezierCurveTo(1730, 600, 1700, 650, 1650, 670);
            ctx.bezierCurveTo(1600, 660, 1580, 600, 1590, 530);
            ctx.bezierCurveTo(1595, 500, 1600, 480, 1600, 480);
            ctx.fill();

            // Greenland
            ctx.beginPath();
            ctx.arc(450, 150, 40, 0, Math.PI * 2);
            ctx.fill();

            // New Zealand
            ctx.beginPath();
            ctx.ellipse(1750, 650, 20, 35, 0.3, 0, Math.PI * 2);
            ctx.fill();

            // Philippines (cyan)
            ctx.fillStyle = '#06b6d4';
            ctx.beginPath();
            ctx.ellipse(1580, 380, 35, 60, 0.2, 0, Math.PI * 2);
            ctx.fill();

            // Iceland (emerald)
            ctx.fillStyle = '#10b981';
            ctx.beginPath();
            ctx.arc(520, 100, 35, 0, Math.PI * 2);
            ctx.fill();

            // Caribbean islands (cyan)
            ctx.fillStyle = '#06b6d4';
            for (let i = 0; i < 5; i++) {
                ctx.beginPath();
                ctx.arc(380 + i * 25, 380 + Math.random() * 50, 12, 0, Math.PI * 2);
                ctx.fill();
            }

            // Southeast Asian islands (emerald)
            ctx.fillStyle = '#10b981';
            for (let i = 0; i < 8; i++) {
                const x = 1450 + Math.random() * 150;
                const y = 420 + Math.random() * 100;
                const size = Math.random() * 20 + 8;
                ctx.beginPath();
                ctx.arc(x, y, size, 0, Math.PI * 2);
                ctx.fill();
            }

            // Mediterranean (violet)
            ctx.fillStyle = '#a78bfa';
            ctx.beginPath();
            ctx.ellipse(1000, 300, 40, 25, 0, 0, Math.PI * 2);
            ctx.fill();

            // Scandinavia details (blue)
            ctx.fillStyle = '#3b82f6';
            ctx.beginPath();
            ctx.ellipse(930, 140, 35, 50, 0.1, 0, Math.PI * 2);
            ctx.fill();

            // Add coastal detail with lighter shade
            ctx.fillStyle = '#06b6d4';
            ctx.globalAlpha = 0.6;

            // Coastal details
            const coastalPoints = [
                { x: 320, y: 280 },
                { x: 1020, y: 250 },
                { x: 1450, y: 250 },
                { x: 1720, y: 540 },
                { x: 330, y: 550 },
            ];

            coastalPoints.forEach(point => {
                ctx.beginPath();
                ctx.arc(point.x, point.y, 30, 0, Math.PI * 2);
                ctx.fill();
            });

            ctx.globalAlpha = 1;

            // Add more colorful island details with varied colors
            const islandColors = ['#0ea5e9', '#06b6d4', '#10b981', '#3b82f6', '#a78bfa', '#ec4899'];
            for (let i = 0; i < 60; i++) {
                const x = Math.random() * canvas.width;
                const y = Math.random() * canvas.height;
                const size = Math.random() * 20 + 5;
                const colorIndex = Math.floor(Math.random() * islandColors.length);
                ctx.fillStyle = islandColors[colorIndex];
                ctx.globalAlpha = 0.7 + Math.random() * 0.3;
                ctx.beginPath();
                ctx.arc(x, y, size, 0, Math.PI * 2);
                ctx.fill();
            }
            ctx.globalAlpha = 1;
        }

        const texture = new THREE.CanvasTexture(canvas);
        const material = new THREE.MeshPhongMaterial({
            map: texture,
            emissive: 0x0ea5e9,
            emissiveIntensity: 0.2,
            shininess: 5,
        });

        const globe = new THREE.Mesh(geometry, material);
        scene.add(globe);

        // Add lighting
        const light = new THREE.DirectionalLight(0xffffff, 0.8);
        light.position.set(5, 3, 5);
        scene.add(light);

        const ambientLight = new THREE.AmbientLight(0x0ea5e9, 0.5);
        scene.add(ambientLight);

        // CRITICAL: Make sure animation starts
        let animationId: number | null = null;
        let rotationX = 0;
        let rotationY = 0;
        let isAnimating = true;

        const animate = () => {
            if (!isAnimating) return;
            
            animationId = requestAnimationFrame(animate);

            // Update rotations continuously
            rotationX += 0.001;
            rotationY += 0.003;

            globe.rotation.x = rotationX;
            globe.rotation.y = rotationY;

            renderer.render(scene, camera);
        };

        // START ANIMATION IMMEDIATELY - use setTimeout to ensure it starts after render
        setTimeout(() => {
            isAnimating = true;
            animate();
            console.log('Globe animation started!');
        }, 0);

        return () => {
            isAnimating = false;
            if (animationId !== null) {
                cancelAnimationFrame(animationId);
            }
            if (containerRef.current && renderer.domElement.parentNode === containerRef.current) {
                containerRef.current.removeChild(renderer.domElement);
            }
            geometry.dispose();
            material.dispose();
            texture.dispose();
            renderer.dispose();
        };
    }, []);

    return (
        <div
            ref={containerRef}
            style={{
                position: 'fixed',
                width: '1400px',
                height: '1400px',
                bottom: '-450px',
                right: '-300px',
                zIndex: 1,
                pointerEvents: 'none',
                overflow: 'hidden',
            }}
        />
    );
}