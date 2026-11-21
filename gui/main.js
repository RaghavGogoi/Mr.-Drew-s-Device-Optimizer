// =========================================================================
// Mr. Drew's Device Optimizer - 60 FPS Canvas Background & Palette Studio
// =========================================================================

let isPyWebViewReady = false;
let isAudioMuted = false;
let audioCtx = null;
let continuousMode = "gaming";
let isContinuousActive = false;
let continuousUptimeTimer = null;
let continuousStartTime = 0;

let appConfig = {
    theme: "obsidian",
    accent_color: "#00f0ff",
    accent_secondary: "#a855f7",
    custom_accent_active: false,
    gradient_mode_active: true,
    custom_palette_swatches: [
        "#00f0ff", "#10b981", "#c084fc", "#f59e0b", 
        "#fcee0a", "#ff2a85", "#ff1e42", "#38bdf8",
        "#00ff66", "#e11d48", "#8b5cf6", "#ff7300"
    ],
    bg_design: "matrix",
    bg_fx_intensity: 0.70,
    bg_fx_speed: 1.0,
    card_glass_opacity: "0.68",
    glass_effect: "16px",
    corner_radius: "16px",
    font_family: "'Outfit', sans-serif",
    text_glow: true,
    continuous_enabled: false,
    continuous_interval_sec: 30,
    continuous_mode: "gaming",
    target_free_ram_gb: 4.0,
    sound_effects: true,
    run_on_startup: false,
    close_to_tray: true
};

// =========================================================================
// 14 LIVE 60 FPS GPU CANVAS BACKGROUND SHADERS & DESIGNS
// =========================================================================
class BackgroundCanvasEngine {
    constructor() {
        this.canvas = document.getElementById("bg-canvas");
        this.ctx = this.canvas ? this.canvas.getContext("2d") : null;
        this.animationFrameId = null;
        this.width = window.innerWidth;
        this.height = window.innerHeight;
        this.time = 0;
        this.lastTimestamp = performance.now();
        this.state = {};
        
        this.initResize();
        this.start();
    }

    initResize() {
        window.addEventListener("resize", () => this.resize());
        this.resize();
    }

    resize() {
        if (!this.canvas) return;
        this.width = this.canvas.width = window.innerWidth;
        this.height = this.canvas.height = window.innerHeight;
        this.resetDesignState();
    }

    resetDesignState() {
        const design = appConfig.bg_design || "matrix";
        this.state = {};

        if (design === "matrix") {
            const fontSize = 15;
            const columns = Math.ceil(this.width / fontSize);
            const glyphChars = "0123456789ABCDEFｦｱｳｴｵｶｷｹｺｻｼｽｾｿﾀﾂﾃﾅﾆﾇﾈﾊﾋﾎﾏﾐﾑﾒﾓﾔﾕﾗﾘﾜ9876543210XYZW$#@%&*+-=";
            
            // Create authentic cascading stream chains (1 to 2 streams per column)
            const chains = [];
            for (let c = 0; c < columns; c++) {
                const streamCount = Math.random() > 0.4 ? 2 : 1;
                for (let s = 0; s < streamCount; s++) {
                    const len = Math.floor(Math.random() * 20 + 12);
                    const streamChars = [];
                    for (let k = 0; k < len; k++) {
                        streamChars.push(glyphChars[Math.floor(Math.random() * glyphChars.length)]);
                    }
                    chains.push({
                        col: c,
                        y: Math.random() * -80 - (s * 30),
                        length: len,
                        speed: Math.random() * 14 + 12, // rows per second
                        chars: streamChars,
                        mutateTimer: Math.random() * 0.2
                    });
                }
            }
            this.state.chains = chains;
            this.state.glyphChars = glyphChars;
            this.state.fontSize = fontSize;
        } else if (design === "tron_grid") {
            this.state.offset = 0;
            this.state.mountains = Array(30).fill(0).map((_, i) => ({
                x: (i / 29) * this.width,
                h: Math.sin(i * 0.7) * 45 + Math.cos(i * 1.3) * 35 + 50
            }));
        } else if (design === "vaporwave") {
            this.state.offset = 0;
            this.state.peaks = Array(24).fill(0).map((_, i) => ({
                x: (i / 23) * this.width,
                h: Math.sin(i * 0.9) * 40 + Math.cos(i * 1.7) * 25 + 40
            }));
        } else if (design === "tunnel") {
            this.state.rings = Array(12).fill(0).map((_, i) => ({
                z: i * 80,
                rot: i * 0.2
            }));
        } else if (design === "starfield") {
            const count = 240;
            this.state.stars = Array(count).fill(0).map(() => ({
                x: (Math.random() - 0.5) * this.width * 2,
                y: (Math.random() - 0.5) * this.height * 2,
                z: Math.random() * this.width,
                pz: 0
            }));
        } else if (design === "neural") {
            const nodeCount = 38;
            this.state.nodes = Array(nodeCount).fill(0).map(() => ({
                x: Math.random() * this.width,
                y: Math.random() * this.height,
                vx: (Math.random() - 0.5) * 40,
                vy: (Math.random() - 0.5) * 40,
                r: Math.random() * 2.5 + 2
            }));
        } else if (design === "wireframe") {
            this.state.gridOffset = 0;
        } else if (design === "hex_shield") {
            this.state.pulse = 0;
        } else if (design === "circuit") {
            const lineCount = 20;
            this.state.lines = Array(lineCount).fill(0).map(() => ({
                x: Math.random() * this.width,
                y: Math.random() * this.height,
                vx: (Math.random() > 0.5 ? 1 : -1) * (Math.random() * 60 + 40),
                vy: (Math.random() > 0.5 ? 1 : -1) * (Math.random() * 60 + 40),
                history: []
            }));
        } else if (design === "dna") {
            this.state.angle = 0;
        } else if (design === "visualizer") {
            this.state.bars = Array(48).fill(0).map(() => Math.random());
        } else if (design === "bokeh") {
            const orbsCount = 22;
            this.state.orbs = Array(orbsCount).fill(0).map(() => ({
                x: Math.random() * this.width,
                y: Math.random() * this.height,
                r: Math.random() * 80 + 40,
                vx: (Math.random() - 0.5) * 20,
                vy: (Math.random() - 0.5) * 20,
                alpha: Math.random() * 0.35 + 0.15
            }));
        }
    }

    start() {
        const render = (now) => {
            const dt = Math.min((now - this.lastTimestamp) / 1000, 0.1);
            this.lastTimestamp = now;
            this.draw(dt);
            this.animationFrameId = requestAnimationFrame(render);
        };
        this.animationFrameId = requestAnimationFrame(render);
    }

    draw(dt) {
        if (!this.ctx) return;
        const ctx = this.ctx;
        const w = this.width;
        const h = this.height;
        const design = appConfig.bg_design || "matrix";
        const speed = appConfig.bg_fx_speed !== undefined ? parseFloat(appConfig.bg_fx_speed) : 1.0;
        const accent = appConfig.accent_color || "#00f0ff";
        const secondary = appConfig.accent_secondary || "#a855f7";

        this.time += dt * speed;

        if (design === "solid") {
            ctx.fillStyle = "#030712";
            ctx.fillRect(0, 0, w, h);
            return;
        }

        // 1. Authentic Matrix Digital Rain (Chained Streams with Leading White Heads & Glitch Mutation)
        if (design === "matrix") {
            ctx.fillStyle = "#030712";
            ctx.fillRect(0, 0, w, h);

            const fontSize = this.state.fontSize || 15;
            const rows = Math.ceil(h / fontSize);
            const chains = this.state.chains || [];
            const glyphChars = this.state.glyphChars || "0123456789ABCDEF";

            ctx.font = `bold ${fontSize}px 'JetBrains Mono', 'Courier New', monospace`;

            chains.forEach(chain => {
                // Update position with precision speed
                chain.y += chain.speed * dt * speed;

                // Mutate random character in the chain stream periodically
                chain.mutateTimer -= dt * (speed > 0 ? speed : 0.5);
                if (chain.mutateTimer <= 0) {
                    chain.mutateTimer = Math.random() * 0.15 + 0.05;
                    const randIdx = Math.floor(Math.random() * chain.chars.length);
                    chain.chars[randIdx] = glyphChars[Math.floor(Math.random() * glyphChars.length)];
                }

                // If chain completely passed bottom of viewport, reset above top
                if ((chain.y - chain.length) > rows + 2) {
                    chain.y = Math.random() * -30 - 5;
                    chain.length = Math.floor(Math.random() * 20 + 12);
                    chain.speed = Math.random() * 14 + 12;
                    chain.chars = [];
                    for (let k = 0; k < chain.length; k++) {
                        chain.chars.push(glyphChars[Math.floor(Math.random() * glyphChars.length)]);
                    }
                }

                // Render the cascading stream chain from head to tail
                const headRow = Math.floor(chain.y);
                const x = chain.col * fontSize;

                for (let i = 0; i < chain.length; i++) {
                    const row = headRow - i;
                    if (row >= 0 && row <= rows + 1) {
                        const y = (row + 1) * fontSize;
                        const char = chain.chars[i] || "0";

                        if (i === 0) {
                            // Chain Head: Brilliant Luminous White with Glow Aura
                            ctx.fillStyle = "#ffffff";
                            ctx.shadowColor = accent;
                            ctx.shadowBlur = 10;
                            ctx.globalAlpha = 1.0;
                            ctx.fillText(char, x, y);
                        } else if (i === 1) {
                            // Head Trail: Bright High-Intensity Tint
                            ctx.fillStyle = "#ffffff";
                            ctx.shadowColor = accent;
                            ctx.shadowBlur = 4;
                            ctx.globalAlpha = 0.95;
                            ctx.fillText(char, x, y);
                        } else {
                            // Chain Body: Fading Alpha Gradient in Active Accent Color
                            const alpha = Math.max(0.04, Math.pow(1 - (i / chain.length), 1.35));
                            ctx.fillStyle = accent;
                            ctx.shadowBlur = 0;
                            ctx.globalAlpha = alpha;
                            ctx.fillText(char, x, y);
                        }
                    }
                }
            });

            ctx.globalAlpha = 1.0;
            ctx.shadowBlur = 0;
        }

        // 2. Cyber Tron Horizon (Fixed, Moving Outrun Grid + Mountains)
        else if (design === "tron_grid") {
            ctx.fillStyle = "#030712";
            ctx.fillRect(0, 0, w, h);

            const horizonY = h * 0.45;

            // Neon Horizon Sky Glow
            const skyGrad = ctx.createLinearGradient(0, 0, 0, horizonY);
            skyGrad.addColorStop(0, "#030712");
            skyGrad.addColorStop(0.7, secondary + "33");
            skyGrad.addColorStop(1, accent + "66");
            ctx.fillStyle = skyGrad;
            ctx.fillRect(0, 0, w, horizonY);

            // Sun over horizon
            ctx.save();
            ctx.beginPath();
            ctx.arc(w * 0.5, horizonY, 65, Math.PI, 0, false);
            const sunGrad = ctx.createLinearGradient(0, horizonY - 65, 0, horizonY);
            sunGrad.addColorStop(0, "#fcee0a");
            sunGrad.addColorStop(0.5, "#ff7300");
            sunGrad.addColorStop(1, "#ff0055");
            ctx.fillStyle = sunGrad;
            ctx.fill();
            ctx.restore();

            // Wireframe Horizon Mountains
            const mts = this.state.mountains || [];
            ctx.strokeStyle = secondary + "88";
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.moveTo(0, horizonY);
            mts.forEach((m, idx) => {
                ctx.lineTo(m.x, horizonY - m.h);
            });
            ctx.lineTo(w, horizonY);
            ctx.stroke();

            // 3D Perspective Moving Grid Floor
            this.state.offset = ((this.state.offset || 0) + 90 * dt * speed) % 40;
            const gridOffset = this.state.offset;

            ctx.strokeStyle = accent + "77";
            ctx.lineWidth = 1.5;

            // Horizontal receding lines
            for (let i = 0; i < 18; i++) {
                const p = (i * 40 + gridOffset) / 720;
                const y = horizonY + Math.pow(p, 2.2) * (h - horizonY);
                if (y >= horizonY && y <= h) {
                    ctx.beginPath();
                    ctx.moveTo(0, y);
                    ctx.lineTo(w, y);
                    ctx.stroke();
                }
            }

            // Radial perspective lines converging to horizon center
            const numVerts = 24;
            for (let i = -numVerts; i <= numVerts; i++) {
                const bottomX = (w * 0.5) + (i * (w / 12));
                ctx.beginPath();
                ctx.moveTo(w * 0.5, horizonY);
                ctx.lineTo(bottomX, h);
                ctx.stroke();
            }
        }

        // 3. Vaporwave 80s Sunset (Fixed, Clean Striped Sun & Moving Neon Grid)
        else if (design === "vaporwave") {
            ctx.fillStyle = "#0c0517";
            ctx.fillRect(0, 0, w, h);

            const horizonY = h * 0.48;

            // Sky gradient
            const sky = ctx.createLinearGradient(0, 0, 0, horizonY);
            sky.addColorStop(0, "#0c0517");
            sky.addColorStop(0.5, "#2a0845");
            sky.addColorStop(1, "#6441a5");
            ctx.fillStyle = sky;
            ctx.fillRect(0, 0, w, horizonY);

            // Striped Sun (Properly clipped circle)
            const sunR = 75;
            ctx.save();
            ctx.beginPath();
            ctx.arc(w * 0.5, horizonY - 15, sunR, 0, Math.PI * 2);
            ctx.clip();

            const sunGrad = ctx.createLinearGradient(0, horizonY - 15 - sunR, 0, horizonY - 15 + sunR);
            sunGrad.addColorStop(0, "#fcee0a");
            sunGrad.addColorStop(0.4, "#ff7300");
            sunGrad.addColorStop(0.8, "#ff007f");
            ctx.fillStyle = sunGrad;
            ctx.fillRect(w * 0.5 - sunR, horizonY - 15 - sunR, sunR * 2, sunR * 2);

            // Horizontal blind cutout slats inside sun
            ctx.fillStyle = "#0c0517";
            for (let y = horizonY - 15 - 10; y < horizonY - 15 + sunR; y += 12) {
                const slatH = ((y - (horizonY - 15 - 10)) / sunR) * 6 + 2;
                ctx.fillRect(w * 0.5 - sunR, y, sunR * 2, slatH);
            }
            ctx.restore();

            // Wireframe synthwave horizon line
            ctx.strokeStyle = "#ff2a85";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(0, horizonY);
            ctx.lineTo(w, horizonY);
            ctx.stroke();

            // Neon Floor Grid
            this.state.offset = ((this.state.offset || 0) + 80 * dt * speed) % 36;
            ctx.strokeStyle = "#00f5d4";
            ctx.lineWidth = 1.4;

            for (let i = 0; i < 16; i++) {
                const p = (i * 36 + this.state.offset) / 576;
                const y = horizonY + Math.pow(p, 2.0) * (h - horizonY);
                if (y >= horizonY && y <= h) {
                    ctx.beginPath();
                    ctx.moveTo(0, y);
                    ctx.lineTo(w, y);
                    ctx.stroke();
                }
            }

            for (let i = -16; i <= 16; i++) {
                const bottomX = (w * 0.5) + (i * (w / 10));
                ctx.beginPath();
                ctx.moveTo(w * 0.5, horizonY);
                ctx.lineTo(bottomX, h);
                ctx.stroke();
            }
        }

        // 4. Hyperspace Neon Tunnel (Infinite 3D Zooming Tunnel)
        else if (design === "tunnel") {
            ctx.fillStyle = "rgba(3, 7, 18, 0.22)";
            ctx.fillRect(0, 0, w, h);

            const cx = w * 0.5;
            const cy = h * 0.5;
            const rings = this.state.rings || [];

            rings.forEach(r => {
                r.z -= 140 * dt * speed;
                r.rot += 0.3 * dt * speed;
                if (r.z <= 0) r.z += 960;

                const size = (1 - r.z / 960) * Math.min(w, h) * 0.85;
                const alpha = Math.min(1, (1 - r.z / 960) * 1.6);

                ctx.save();
                ctx.translate(cx, cy);
                ctx.rotate(r.rot);
                ctx.strokeStyle = (r.z % 2 === 0 ? accent : secondary);
                ctx.globalAlpha = alpha;
                ctx.lineWidth = 2;

                ctx.strokeRect(-size * 0.5, -size * 0.5, size, size);
                ctx.restore();
            });
            ctx.globalAlpha = 1.0;
        }

        // 5. Warp Speed Starfield
        else if (design === "starfield") {
            ctx.fillStyle = "rgba(3, 7, 18, 0.28)";
            ctx.fillRect(0, 0, w, h);

            const cx = w * 0.5;
            const cy = h * 0.5;
            const stars = this.state.stars || [];

            stars.forEach(s => {
                s.pz = s.z;
                s.z -= 450 * dt * speed;
                if (s.z <= 0) {
                    s.z = w;
                    s.pz = w;
                    s.x = (Math.random() - 0.5) * w * 2;
                    s.y = (Math.random() - 0.5) * h * 2;
                }

                const k = 250 / s.z;
                const px = s.x * k + cx;
                const py = s.y * k + cy;

                const pk = 250 / s.pz;
                const prevX = s.x * pk + cx;
                const prevY = s.y * pk + cy;

                if (px >= 0 && px < w && py >= 0 && py < h) {
                    const alpha = Math.min(1, (1 - s.z / w) * 1.5);
                    ctx.strokeStyle = (s.z % 2 === 0 ? accent : secondary);
                    ctx.globalAlpha = alpha;
                    ctx.lineWidth = (1 - s.z / w) * 2.5 + 0.5;
                    ctx.beginPath();
                    ctx.moveTo(prevX, prevY);
                    ctx.lineTo(px, py);
                    ctx.stroke();
                }
            });
            ctx.globalAlpha = 1.0;
        }

        // 6. Neural Network Synapse
        else if (design === "neural") {
            ctx.fillStyle = "#030712";
            ctx.fillRect(0, 0, w, h);

            const nodes = this.state.nodes || [];
            nodes.forEach(n => {
                n.x += n.vx * dt * speed;
                n.y += n.vy * dt * speed;
                if (n.x < 0 || n.x > w) n.vx *= -1;
                if (n.y < 0 || n.y > h) n.vy *= -1;
            });

            ctx.lineWidth = 1.0;
            for (let i = 0; i < nodes.length; i++) {
                for (let j = i + 1; j < nodes.length; j++) {
                    const dist = Math.hypot(nodes[i].x - nodes[j].x, nodes[i].y - nodes[j].y);
                    if (dist < 160) {
                        const alpha = 1 - (dist / 160);
                        ctx.strokeStyle = accent;
                        ctx.globalAlpha = alpha * 0.45;
                        ctx.beginPath();
                        ctx.moveTo(nodes[i].x, nodes[i].y);
                        ctx.lineTo(nodes[j].x, nodes[j].y);
                        ctx.stroke();
                    }
                }
            }

            nodes.forEach(n => {
                ctx.beginPath();
                ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
                ctx.fillStyle = secondary;
                ctx.globalAlpha = 0.9;
                ctx.fill();
            });
            ctx.globalAlpha = 1.0;
        }

        // 7. Wireframe Mountain Terrain
        else if (design === "wireframe") {
            ctx.fillStyle = "#030712";
            ctx.fillRect(0, 0, w, h);

            this.state.gridOffset = ((this.state.gridOffset || 0) + 30 * dt * speed) % 30;
            const rows = 14;
            const cols = 20;
            const cellW = w / cols;
            const horizon = h * 0.45;

            ctx.strokeStyle = accent + "66";
            ctx.lineWidth = 1.2;

            for (let r = 0; r < rows; r++) {
                const y = horizon + Math.pow(r / rows, 1.8) * (h - horizon);
                ctx.beginPath();
                for (let c = 0; c <= cols; c++) {
                    const x = c * cellW;
                    const elevation = Math.sin(c * 0.6 + this.time) * Math.cos(r * 0.5 + this.time) * 30 * (r / rows);
                    if (c === 0) ctx.moveTo(x, y - elevation);
                    else ctx.lineTo(x, y - elevation);
                }
                ctx.stroke();
            }
        }

        // 8. Hexagonal Cyber Shield
        else if (design === "hex_shield") {
            ctx.fillStyle = "#030712";
            ctx.fillRect(0, 0, w, h);

            const hexSize = 36;
            const hexH = hexSize * Math.sqrt(3);
            ctx.lineWidth = 1.2;

            for (let y = 0; y < h + hexH; y += hexH) {
                for (let x = 0; x < w + hexSize * 3; x += hexSize * 3) {
                    this.drawHexagon(ctx, x, y, hexSize, accent, this.time);
                    this.drawHexagon(ctx, x + hexSize * 1.5, y + hexH * 0.5, hexSize, secondary, this.time);
                }
            }
        }

        // 9. Circuit PCB Traces
        else if (design === "circuit") {
            ctx.fillStyle = "rgba(3, 7, 18, 0.18)";
            ctx.fillRect(0, 0, w, h);

            const lines = this.state.lines || [];
            ctx.lineWidth = 2;

            lines.forEach(l => {
                ctx.beginPath();
                ctx.arc(l.x, l.y, 3.5, 0, Math.PI * 2);
                ctx.fillStyle = accent;
                ctx.fill();

                l.x += l.vx * dt * speed;
                l.y += l.vy * dt * speed;

                if (Math.random() > 0.95) {
                    if (Math.random() > 0.5) l.vx = (Math.random() > 0.5 ? 1 : -1) * (Math.random() * 50 + 30);
                    else l.vy = (Math.random() > 0.5 ? 1 : -1) * (Math.random() * 50 + 30);
                }

                if (l.x < 0 || l.x > w) l.vx *= -1;
                if (l.y < 0 || l.y > h) l.vy *= -1;
            });
        }

        // 10. DNA Cyber Helix
        else if (design === "dna") {
            ctx.fillStyle = "#030712";
            ctx.fillRect(0, 0, w, h);

            const numPoints = 28;
            const cy = h * 0.5;

            for (let i = 0; i < numPoints; i++) {
                const x = (i / (numPoints - 1)) * w;
                const phase = i * 0.35 + this.time * 2;
                const y1 = cy + Math.sin(phase) * 110;
                const y2 = cy - Math.sin(phase) * 110;

                ctx.strokeStyle = secondary + "44";
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(x, y1);
                ctx.lineTo(x, y2);
                ctx.stroke();

                ctx.beginPath();
                ctx.arc(x, y1, 4.5, 0, Math.PI * 2);
                ctx.fillStyle = accent;
                ctx.fill();

                ctx.beginPath();
                ctx.arc(x, y2, 4.5, 0, Math.PI * 2);
                ctx.fillStyle = secondary;
                ctx.fill();
            }
        }

        // 11. Audio Visualizer Spectrum Bars
        else if (design === "visualizer") {
            ctx.fillStyle = "#030712";
            ctx.fillRect(0, 0, w, h);

            const bars = this.state.bars || [];
            const barW = w / bars.length;

            bars.forEach((b, i) => {
                const val = Math.abs(Math.sin(i * 0.25 + this.time * 3) * Math.cos(i * 0.1 - this.time * 2));
                const barH = val * (h * 0.5) + 15;
                const y = h - barH;

                const grad = ctx.createLinearGradient(0, y, 0, h);
                grad.addColorStop(0, accent);
                grad.addColorStop(1, secondary + "33");
                ctx.fillStyle = grad;
                ctx.fillRect(i * barW + 2, y, barW - 4, barH);
            });
        }

        // 12. Aurora Plasma Waves
        else if (design === "aurora") {
            ctx.fillStyle = "#030712";
            ctx.fillRect(0, 0, w, h);

            for (let i = 0; i < 4; i++) {
                ctx.beginPath();
                ctx.moveTo(0, h);
                for (let x = 0; x <= w; x += 25) {
                    const y = h * 0.5 + Math.sin(x * 0.003 + this.time + i) * 120 + Math.cos(x * 0.006 - this.time * 0.7) * 70;
                    ctx.lineTo(x, y);
                }
                ctx.lineTo(w, h);
                ctx.closePath();

                const grad = ctx.createLinearGradient(0, 0, w, h);
                grad.addColorStop(0, accent + "33");
                grad.addColorStop(0.5, secondary + "33");
                grad.addColorStop(1, "transparent");
                ctx.fillStyle = grad;
                ctx.fill();
            }
        }

        // 13. Cyberpunk Bokeh Orbs
        else if (design === "bokeh") {
            ctx.fillStyle = "#030712";
            ctx.fillRect(0, 0, w, h);

            const orbs = this.state.orbs || [];
            orbs.forEach((o, idx) => {
                o.x += o.vx * dt * speed;
                o.y += o.vy * dt * speed;
                if (o.x < -100 || o.x > w + 100) o.vx *= -1;
                if (o.y < -100 || o.y > h + 100) o.vy *= -1;

                const g = ctx.createRadialGradient(o.x, o.y, 0, o.x, o.y, o.r);
                g.addColorStop(0, (idx % 2 === 0 ? accent : secondary) + "66");
                g.addColorStop(1, "transparent");
                ctx.fillStyle = g;
                ctx.beginPath();
                ctx.arc(o.x, o.y, o.r, 0, Math.PI * 2);
                ctx.fill();
            });
        }
    }

    drawHexagon(ctx, x, y, r, color, time) {
        ctx.beginPath();
        for (let i = 0; i < 6; i++) {
            const angle = (Math.PI / 3) * i;
            const hx = x + r * Math.cos(angle);
            const hy = y + r * Math.sin(angle);
            if (i === 0) ctx.moveTo(hx, hy);
            else ctx.lineTo(hx, hy);
        }
        ctx.closePath();
        const dist = Math.hypot(x - this.width * 0.5, y - this.height * 0.5);
        const glow = Math.sin(dist * 0.01 - time * 2);
        ctx.strokeStyle = glow > 0.4 ? color + "99" : color + "1a";
        ctx.stroke();
    }
}

let bgCanvasEngine = null;

// Lifecycle Initialization
document.addEventListener("DOMContentLoaded", () => {
    bgCanvasEngine = new BackgroundCanvasEngine();
    initPyWebViewBridge();
    setInterval(refreshSystemStats, 1800);
    setInterval(refreshContinuousStatus, 2000);
});

function initPyWebViewBridge() {
    window.addEventListener('pywebviewready', async () => {
        isPyWebViewReady = true;
        logToConsole("Native Python Bridge Connected.", "success");
        await loadAppConfig();
        await refreshSystemStats();
        await refreshContinuousStatus();
        await refreshTopProcesses();
    });

    setTimeout(async () => {
        if (!isPyWebViewReady) {
            logToConsole("Running in Local Web Interface Mode.", "info");
            await loadAppConfig();
            await refreshSystemStats();
            await refreshContinuousStatus();
            await refreshTopProcesses();
        }
    }, 500);
}

// Config Loader
async function loadAppConfig() {
    try {
        if (window.pywebview && window.pywebview.api && window.pywebview.api.get_config) {
            const cfg = await window.pywebview.api.get_config();
            if (cfg) appConfig = Object.assign({}, appConfig, cfg);
        }
        if (window.pywebview && window.pywebview.api && window.pywebview.api.is_startup_enabled) {
            const startupActive = await window.pywebview.api.is_startup_enabled();
            appConfig.run_on_startup = startupActive;
        }
    } catch (e) {
        console.error("Config load error:", e);
    }
    applyConfigToUI();
}

function applyConfigToUI() {
    const root = document.documentElement;
    root.setAttribute("data-theme", appConfig.theme || "obsidian");

    // Theme cards active state
    document.querySelectorAll(".theme-card").forEach(c => {
        c.classList.toggle("active", c.getAttribute("data-theme-id") === appConfig.theme);
    });

    // Background designs active state
    document.querySelectorAll(".bg-design-card").forEach(c => {
        c.classList.toggle("active", c.getAttribute("data-bg-design") === appConfig.bg_design);
    });

    // Form settings
    const intervalSelect = document.getElementById("setting-interval");
    if (intervalSelect) intervalSelect.value = String(appConfig.continuous_interval_sec || 30);

    const headroomSelect = document.getElementById("setting-ram-headroom");
    if (headroomSelect) headroomSelect.value = (appConfig.target_free_ram_gb || 4.0).toFixed(1);

    const startupToggle = document.getElementById("setting-startup-toggle");
    if (startupToggle) startupToggle.checked = Boolean(appConfig.run_on_startup);

    const closeTrayToggle = document.getElementById("setting-close-tray-toggle");
    if (closeTrayToggle) closeTrayToggle.checked = Boolean(appConfig.close_to_tray !== false);

    const soundToggle = document.getElementById("setting-sound-toggle");
    if (soundToggle) soundToggle.checked = Boolean(appConfig.sound_effects);

    const bgIntensitySelect = document.getElementById("setting-bg-intensity");
    if (bgIntensitySelect && appConfig.bg_fx_intensity !== undefined) {
        bgIntensitySelect.value = (parseFloat(appConfig.bg_fx_intensity)).toFixed(2);
    }

    const bgSpeedSelect = document.getElementById("setting-bg-speed");
    if (bgSpeedSelect && appConfig.bg_fx_speed !== undefined) {
        bgSpeedSelect.value = (parseFloat(appConfig.bg_fx_speed)).toFixed(1);
    }

    const opacitySelect = document.getElementById("setting-card-opacity");
    if (opacitySelect && appConfig.card_glass_opacity) opacitySelect.value = appConfig.card_glass_opacity;

    const blurSelect = document.getElementById("setting-glass-blur");
    if (blurSelect && appConfig.glass_effect) blurSelect.value = appConfig.glass_effect;

    const radiusSelect = document.getElementById("setting-corner-radius");
    if (radiusSelect && appConfig.corner_radius) radiusSelect.value = appConfig.corner_radius;

    const fontSelect = document.getElementById("setting-font-family");
    if (fontSelect && appConfig.font_family) fontSelect.value = appConfig.font_family;

    const textGlowToggle = document.getElementById("setting-text-glow-toggle");
    if (textGlowToggle) textGlowToggle.checked = Boolean(appConfig.text_glow !== false);

    const gradToggle = document.getElementById("setting-gradient-mode");
    if (gradToggle) gradToggle.checked = Boolean(appConfig.gradient_mode_active !== false);

    renderPaletteSwatches();
    applyCustomStyles();

    isAudioMuted = !appConfig.sound_effects;
    updateSoundIcon();

    if (appConfig.continuous_mode) {
        setContinuousModePreset(appConfig.continuous_mode, false);
    }
}

function applyCustomStyles() {
    const root = document.documentElement;

    if (appConfig.bg_fx_intensity !== undefined) {
        root.style.setProperty("--bg-fx-opacity", appConfig.bg_fx_intensity);
    }

    if (appConfig.card_glass_opacity) {
        root.style.setProperty("--card-opacity", appConfig.card_glass_opacity);
    }

    if (appConfig.glass_effect) {
        root.style.setProperty("--blur-val", appConfig.glass_effect);
    }

    if (appConfig.corner_radius) {
        root.style.setProperty("--radius-card", appConfig.corner_radius);
    }

    if (appConfig.font_family) {
        root.style.setProperty("--font-main", appConfig.font_family);
    }

    document.querySelectorAll(".text-glow").forEach(el => {
        el.style.textShadow = appConfig.text_glow !== false ? "0 0 12px var(--accent-glow)" : "none";
    });

    if (appConfig.accent_color) {
        root.style.setProperty("--accent", appConfig.accent_color);
        root.style.setProperty("--border-glow", appConfig.accent_color + "55");
        root.style.setProperty("--accent-glow", appConfig.accent_color + "44");
    }

    if (appConfig.accent_secondary) {
        root.style.setProperty("--accent-secondary", appConfig.accent_secondary);
        root.style.setProperty("--purple", appConfig.accent_secondary);
    }

    document.body.classList.toggle("gradient-mode-on", Boolean(appConfig.gradient_mode_active !== false));

    const primaryPicker = document.getElementById("primary-color-picker");
    if (primaryPicker) primaryPicker.value = appConfig.accent_color || "#00f0ff";
    const primaryHex = document.getElementById("primary-hex-label");
    if (primaryHex) primaryHex.innerText = appConfig.accent_color || "#00f0ff";

    const secPicker = document.getElementById("secondary-color-picker");
    if (secPicker) secPicker.value = appConfig.accent_secondary || "#a855f7";
    const secHex = document.getElementById("secondary-hex-label");
    if (secHex) secHex.innerText = appConfig.accent_secondary || "#a855f7";

    if (bgCanvasEngine) bgCanvasEngine.resetDesignState();
}

// =========================================================================
// BACKGROUND FX DESIGN & SPEED CONTROLS
// =========================================================================
async function selectBgDesign(designId) {
    appConfig.bg_design = designId;
    document.querySelectorAll(".bg-design-card").forEach(c => {
        c.classList.toggle("active", c.getAttribute("data-bg-design") === designId);
    });

    if (bgCanvasEngine) bgCanvasEngine.resetDesignState();
    playAudioFX("click");
    logToConsole(`Background canvas design set to '${designId}'`, "info");

    if (window.pywebview && window.pywebview.api && window.pywebview.api.update_setting) {
        window.pywebview.api.update_setting("bg_design", designId);
    }
}

async function updateBgIntensity(val) {
    const num = parseFloat(val);
    appConfig.bg_fx_intensity = num;
    applyCustomStyles();
    playAudioFX("click");

    if (window.pywebview && window.pywebview.api && window.pywebview.api.update_setting) {
        window.pywebview.api.update_setting("bg_fx_intensity", num);
    }
}

async function updateBgSpeed(val) {
    const num = parseFloat(val);
    appConfig.bg_fx_speed = num;
    playAudioFX("click");
    logToConsole(`FX Motion Speed set to ${num}x`, "info");

    if (window.pywebview && window.pywebview.api && window.pywebview.api.update_setting) {
        window.pywebview.api.update_setting("bg_fx_speed", num);
    }
}

// =========================================================================
// PALETTE MANAGER
// =========================================================================
function renderPaletteSwatches() {
    const list = document.getElementById("palette-swatches-list");
    if (!list) return;
    list.innerHTML = "";

    const swatches = appConfig.custom_palette_swatches || [];
    const countLabel = document.getElementById("palette-count-label");
    if (countLabel) countLabel.innerText = swatches.length;

    swatches.forEach((hex, idx) => {
        const item = document.createElement("div");
        item.className = "palette-swatch-item" + (appConfig.accent_color === hex ? " active" : "");
        item.style.backgroundColor = hex;
        item.title = `Color: ${hex} (Click to set Primary)`;

        item.onclick = (e) => {
            if (e.target.classList.contains("swatch-delete-btn")) return;
            setPrimaryAccent(hex);
        };

        if (swatches.length > 2) {
            const delBtn = document.createElement("span");
            delBtn.className = "swatch-delete-btn";
            delBtn.innerText = "✕";
            delBtn.title = "Delete swatch";
            delBtn.onclick = (e) => {
                e.stopPropagation();
                deletePaletteSwatch(idx);
            };
            item.appendChild(delBtn);
        }

        list.appendChild(item);
    });

    const addBtn = document.createElement("div");
    addBtn.className = "palette-add-btn";
    addBtn.innerText = "+";
    addBtn.title = "Add new custom color to palette";
    addBtn.onclick = () => promptAddNewColor();
    list.appendChild(addBtn);
}

async function setPrimaryAccent(hex) {
    appConfig.accent_color = hex;
    appConfig.custom_accent_active = true;
    applyCustomStyles();
    renderPaletteSwatches();
    playAudioFX("click");
    logToConsole(`Primary accent updated to ${hex}`, "info");

    if (window.pywebview && window.pywebview.api && window.pywebview.api.update_setting) {
        window.pywebview.api.update_setting("accent_color", hex);
        window.pywebview.api.update_setting("custom_accent_active", true);
    }
}

async function setSecondaryAccent(hex) {
    appConfig.accent_secondary = hex;
    applyCustomStyles();
    playAudioFX("click");
    logToConsole(`Secondary accent updated to ${hex}`, "info");

    if (window.pywebview && window.pywebview.api && window.pywebview.api.update_setting) {
        window.pywebview.api.update_setting("accent_secondary", hex);
    }
}

async function promptAddNewColor() {
    playAudioFX("click");
    const vibrantColors = ["#00ff99", "#ff007f", "#7928ca", "#ff4d4d", "#00dfd8", "#f7b731", "#5f27cd", "#48dbfb", "#ff3838", "#c56cf0"];
    const randomHex = vibrantColors[Math.floor(Math.random() * vibrantColors.length)];
    
    if (!appConfig.custom_palette_swatches.includes(randomHex)) {
        appConfig.custom_palette_swatches.push(randomHex);
        setPrimaryAccent(randomHex);
        savePaletteSwatches();
        logToConsole(`Added new swatch ${randomHex} to palette!`, "success");
    } else {
        const picker = document.getElementById("primary-color-picker");
        if (picker) picker.click();
    }
}

async function deletePaletteSwatch(index) {
    if (appConfig.custom_palette_swatches.length <= 2) return;
    const removed = appConfig.custom_palette_swatches.splice(index, 1)[0];
    playAudioFX("action");
    renderPaletteSwatches();
    savePaletteSwatches();
    logToConsole(`Removed swatch ${removed} from palette.`, "info");
}

async function randomizePaletteHarmonies() {
    playAudioFX("action");
    const harmonies = [
        { primary: "#00f0ff", secondary: "#a855f7", name: "Cyberpunk Duel" },
        { primary: "#ff2a85", secondary: "#ff7300", name: "Synthwave Sunset" },
        { primary: "#10b981", secondary: "#06b6d4", name: "Matrix Biohazard" },
        { primary: "#fcee0a", secondary: "#ff0055", name: "Tokyo Neon" },
        { primary: "#ff1e42", secondary: "#9333ea", name: "Crimson Abyss" },
        { primary: "#38bdf8", secondary: "#ec4899", name: "Ice Blossom" }
    ];
    const picked = harmonies[Math.floor(Math.random() * harmonies.length)];
    appConfig.accent_color = picked.primary;
    appConfig.accent_secondary = picked.secondary;
    appConfig.custom_accent_active = true;

    if (!appConfig.custom_palette_swatches.includes(picked.primary)) appConfig.custom_palette_swatches.unshift(picked.primary);
    if (!appConfig.custom_palette_swatches.includes(picked.secondary)) appConfig.custom_palette_swatches.unshift(picked.secondary);

    applyCustomStyles();
    renderPaletteSwatches();
    savePaletteSwatches();
    logToConsole(`Harmonized palette: ${picked.name} (${picked.primary} + ${picked.secondary})`, "success");
}

async function savePaletteSwatches() {
    if (window.pywebview && window.pywebview.api && window.pywebview.api.update_setting) {
        window.pywebview.api.update_setting("custom_palette_swatches", appConfig.custom_palette_swatches);
    }
}

async function toggleGradientMode(enable) {
    appConfig.gradient_mode_active = enable;
    applyCustomStyles();
    playAudioFX("click");
    logToConsole(`Dual-tone neon gradient mode set to ${enable ? 'ENABLED' : 'DISABLED'}.`, "info");

    if (window.pywebview && window.pywebview.api && window.pywebview.api.update_setting) {
        window.pywebview.api.update_setting("gradient_mode_active", enable);
    }
}

async function changeAppTheme(themeId) {
    appConfig.theme = themeId;
    appConfig.custom_accent_active = false;
    document.documentElement.removeAttribute("style");
    applyConfigToUI();
    playAudioFX("click");
    logToConsole(`Theme updated to '${themeId}'`, "info");

    if (window.pywebview && window.pywebview.api && window.pywebview.api.update_setting) {
        try {
            await window.pywebview.api.update_setting("theme", themeId);
            await window.pywebview.api.update_setting("custom_accent_active", false);
        } catch (e) {}
    }
}

// Other UI Geometry & Settings
async function updateCardOpacity(val) {
    appConfig.card_glass_opacity = val;
    applyCustomStyles();
    playAudioFX("click");
    if (window.pywebview && window.pywebview.api && window.pywebview.api.update_setting) {
        window.pywebview.api.update_setting("card_glass_opacity", val);
    }
}

async function updateGlassBlur(val) {
    appConfig.glass_effect = val;
    applyCustomStyles();
    playAudioFX("click");
    if (window.pywebview && window.pywebview.api && window.pywebview.api.update_setting) {
        window.pywebview.api.update_setting("glass_effect", val);
    }
}

async function updateCornerRadius(val) {
    appConfig.corner_radius = val;
    applyCustomStyles();
    playAudioFX("click");
    if (window.pywebview && window.pywebview.api && window.pywebview.api.update_setting) {
        window.pywebview.api.update_setting("corner_radius", val);
    }
}

async function updateFontFamily(val) {
    appConfig.font_family = val;
    applyCustomStyles();
    playAudioFX("click");
    if (window.pywebview && window.pywebview.api && window.pywebview.api.update_setting) {
        window.pywebview.api.update_setting("font_family", val);
    }
}

async function toggleTextGlow(enable) {
    appConfig.text_glow = enable;
    applyCustomStyles();
    playAudioFX("click");
    if (window.pywebview && window.pywebview.api && window.pywebview.api.update_setting) {
        window.pywebview.api.update_setting("text_glow", enable);
    }
}

async function toggleStartupSetting(enable) {
    appConfig.run_on_startup = enable;
    playAudioFX("click");
    if (window.pywebview && window.pywebview.api && window.pywebview.api.set_run_on_startup) {
        try {
            const res = await window.pywebview.api.set_run_on_startup(enable);
            logToConsole(res.message, res.status ? "success" : "warning");
        } catch (e) {
            logToConsole(`Startup setting error: ${e}`, "warning");
        }
    }
}

async function toggleCloseToTraySetting(enable) {
    appConfig.close_to_tray = enable;
    playAudioFX("click");
    logToConsole(`Close to tray (run in background) set to ${enable ? 'ENABLED' : 'DISABLED'}.`, "info");
    if (window.pywebview && window.pywebview.api && window.pywebview.api.update_setting) {
        window.pywebview.api.update_setting("close_to_tray", enable);
    }
}

async function toggleSoundSetting(enable) {
    appConfig.sound_effects = enable;
    isAudioMuted = !enable;
    updateSoundIcon();
    if (enable) playAudioFX("click");
    if (window.pywebview && window.pywebview.api && window.pywebview.api.update_setting) {
        window.pywebview.api.update_setting("sound_effects", enable);
    }
}

async function updateContinuousInterval(val) {
    const sec = parseInt(val);
    appConfig.continuous_interval_sec = sec;
    playAudioFX("click");
    logToConsole(`Continuous loop interval set to ${sec}s`, "info");
    if (window.pywebview && window.pywebview.api && window.pywebview.api.update_setting) {
        window.pywebview.api.update_setting("continuous_interval_sec", sec);
        if (isContinuousActive) handleMasterToggleChange(true);
    }
}

async function updateTargetRamThreshold(val) {
    const gb = parseFloat(val);
    appConfig.target_free_ram_gb = gb;
    playAudioFX("click");
    logToConsole(`Target free RAM threshold set to ${gb} GB`, "info");
    if (window.pywebview && window.pywebview.api && window.pywebview.api.update_setting) {
        window.pywebview.api.update_setting("target_free_ram_gb", gb);
    }
}

async function exportDiagnosticsReport() {
    playAudioFX("click");
    if (window.pywebview && window.pywebview.api && window.pywebview.api.export_diagnostics) {
        try {
            const report = await window.pywebview.api.export_diagnostics();
            navigator.clipboard.writeText(report);
            logToConsole("System diagnostics report copied to clipboard!", "success");
        } catch (e) {
            logToConsole(`Failed to export diagnostics: ${e}`, "warning");
        }
    }
}

async function resetConfigDefaults() {
    playAudioFX("warning");
    if (window.pywebview && window.pywebview.api && window.pywebview.api.reset_config) {
        try {
            const defaults = await window.pywebview.api.reset_config();
            if (defaults) appConfig = defaults;
            document.documentElement.removeAttribute("style");
            applyConfigToUI();
            logToConsole("Restored default configuration.", "success");
        } catch (e) {}
    }
}

// Master Continuous Toggle
async function handleMasterToggleChange(enable) {
    playAudioFX("click");
    updateMasterUIState(enable);

    if (window.pywebview && window.pywebview.api && window.pywebview.api.toggle_continuous_mode) {
        try {
            const interval = parseInt(document.getElementById("setting-interval")?.value || "30");
            const res = await window.pywebview.api.toggle_continuous_mode(enable, continuousMode, interval);
            if (res && res.message) {
                logToConsole(res.message, enable ? "success" : "info");
                playAudioFX(enable ? "success" : "action");
            }
        } catch (e) {
            logToConsole(`Toggle error: ${e}`, "warning");
        }
    } else {
        logToConsole(`Continuous mode set to ${enable ? 'ACTIVE' : 'IDLE'}.`, enable ? "success" : "info");
        playAudioFX(enable ? "success" : "action");
    }

    refreshContinuousStatus();
}

function updateMasterUIState(active) {
    isContinuousActive = active;
    const toggle = document.getElementById("master-continuous-toggle");
    if (toggle) toggle.checked = active;

    const box = document.getElementById("master-toggle-box");
    const badge = document.getElementById("master-status-badge");
    const dot = document.getElementById("master-status-dot");
    const text = document.getElementById("master-status-text");
    const switchLabel = document.getElementById("switch-state-label");
    const sidebarDot = document.getElementById("daemon-sidebar-dot");
    const sidebarTitle = document.getElementById("daemon-sidebar-title");
    const sidebarSub = document.getElementById("daemon-sidebar-sub");

    if (active) {
        if (box) box.classList.add("active-state");
        if (badge) badge.className = "toggle-status-badge active";
        if (dot) dot.className = "daemon-status-dot active";
        if (text) text.innerText = `CONTINUOUS MODE: ACTIVE (${continuousMode.toUpperCase()})`;
        if (switchLabel) {
            switchLabel.innerText = "RUNNING / ON";
            switchLabel.className = "switch-text active";
        }
        if (sidebarDot) sidebarDot.className = "daemon-status-dot active";
        if (sidebarTitle) sidebarTitle.innerText = "Daemon: Running";
        if (sidebarSub) sidebarSub.innerText = `${continuousMode.toUpperCase()} mode active`;

        if (!continuousUptimeTimer) {
            continuousStartTime = Date.now();
            continuousUptimeTimer = setInterval(updateUptimeDisplay, 1000);
        }
    } else {
        if (box) box.classList.remove("active-state");
        if (badge) badge.className = "toggle-status-badge";
        if (dot) dot.className = "daemon-status-dot";
        if (text) text.innerText = "CONTINUOUS MODE: IDLE";
        if (switchLabel) {
            switchLabel.innerText = "OFF / STANDBY";
            switchLabel.className = "switch-text";
        }
        if (sidebarDot) sidebarDot.className = "daemon-status-dot";
        if (sidebarTitle) sidebarTitle.innerText = "Daemon: Standby";
        if (sidebarSub) sidebarSub.innerText = "Ready to optimize";

        if (continuousUptimeTimer) {
            clearInterval(continuousUptimeTimer);
            continuousUptimeTimer = null;
        }
        document.getElementById("daemon-uptime").innerText = "00:00:00";
    }
}

function updateUptimeDisplay() {
    if (!isContinuousActive) return;
    const elapsedSec = Math.floor((Date.now() - continuousStartTime) / 1000);
    const hrs = String(Math.floor(elapsedSec / 3600)).padStart(2, '0');
    const mins = String(Math.floor((elapsedSec % 3600) / 60)).padStart(2, '0');
    const secs = String(elapsedSec % 60).padStart(2, '0');
    document.getElementById("daemon-uptime").innerText = `${hrs}:${mins}:${secs}`;
}

async function refreshContinuousStatus() {
    if (window.pywebview && window.pywebview.api && window.pywebview.api.get_continuous_status) {
        try {
            const status = await window.pywebview.api.get_continuous_status();
            if (status) {
                if (status.is_running !== isContinuousActive) {
                    if (status.is_running && status.uptime_sec > 0) {
                        continuousStartTime = Date.now() - (status.uptime_sec * 1000);
                    }
                    updateMasterUIState(status.is_running);
                }
                document.getElementById("daemon-cycles").innerText = `${status.cycles_completed || 0} Cycles`;
                document.getElementById("daemon-reclaimed").innerText = `${status.total_reclaimed_mb || 0} MB Freed`;
            }
        } catch (e) {}
    }
}

function setContinuousModePreset(mode, notifyBackend = true) {
    continuousMode = mode;
    playAudioFX("click");
    document.querySelectorAll(".mode-chip").forEach(c => c.classList.remove("active"));
    const activeChip = document.getElementById(`chip-${mode}`);
    if (activeChip) activeChip.classList.add("active");

    if (isContinuousActive) {
        document.getElementById("master-status-text").innerText = `CONTINUOUS MODE: ACTIVE (${mode.toUpperCase()})`;
    }

    if (notifyBackend && window.pywebview && window.pywebview.api && window.pywebview.api.update_setting) {
        window.pywebview.api.update_setting("continuous_mode", mode);
        if (isContinuousActive) handleMasterToggleChange(true);
    }
}

// Telemetry Stats Refresh
async function refreshSystemStats() {
    try {
        let specs = null;
        let hw = null;

        if (window.pywebview && window.pywebview.api) {
            specs = await window.pywebview.api.get_system_specs();
            hw = await window.pywebview.api.get_hardware_details();
        } else {
            specs = { os_name: "Windows 11", total_ram_gb: 16.0, used_ram_gb: 6.8, avail_ram_gb: 9.2, percent_used: 42.5, cpu_percent: 18.0, timer_res_ms: 1.0, is_admin: true };
            hw = { cpu_cores_logical: 16, gpu_vendor: "NVIDIA GeForce RTX 4070", device_profile: "High-End Gaming Rig (32GB+ RAM)" };
        }

        if (specs) {
            document.getElementById("dash-ram-percent").innerText = `${specs.percent_used}%`;
            document.getElementById("dash-ram-fraction").innerText = `${specs.used_ram_gb} / ${specs.total_ram_gb} GB`;
            document.getElementById("dash-ram-fill").style.width = `${specs.percent_used}%`;
            document.getElementById("dash-ram-avail").innerText = `${specs.avail_ram_gb} GB Free`;

            document.getElementById("dash-cpu-percent").innerText = `${specs.cpu_percent}%`;
            document.getElementById("dash-cpu-fill").style.width = `${Math.min(100, specs.cpu_percent)}%`;
            if (hw) document.getElementById("dash-cpu-cores").innerText = `${hw.cpu_cores_logical} Cores`;

            document.getElementById("dash-timer-val").innerText = `${specs.timer_res_ms || 1.0} ms`;
            
            const badgeOsText = document.getElementById("badge-os-text");
            if (badgeOsText) badgeOsText.innerText = specs.os_name;

            const badgeAdmin = document.getElementById("badge-admin");
            const badgeAdminText = document.getElementById("badge-admin-text");
            if (badgeAdmin) {
                if (specs.is_admin) {
                    badgeAdmin.className = "badge badge-green";
                    if (badgeAdminText) badgeAdminText.innerText = "Admin (Elevated)";
                } else {
                    badgeAdmin.className = "badge badge-amber";
                    if (badgeAdminText) badgeAdminText.innerText = "Standard (Elevate)";
                }
            }

            if (hw) {
                document.getElementById("engine-subtitle").innerText = `${hw.gpu_vendor} • ${hw.device_profile}`;
                document.getElementById("specs-summary-line").innerText = `OS: ${specs.os_name} | CPU: ${hw.cpu_cores_logical} Cores | RAM: ${specs.total_ram_gb} GB | GPU: ${hw.gpu_vendor}`;
            }
        }
    } catch (e) {
        console.error("Stats refresh error:", e);
    }
}

// Action Gateway
async function triggerAction(actionId, extraArg = null) {
    playAudioFX("action");
    logToConsole(`Executing action: '${actionId}'...`, "info");

    if (window.pywebview && window.pywebview.api && window.pywebview.api.execute_action) {
        try {
            const res = await window.pywebview.api.execute_action(actionId, extraArg);
            if (res && res.logs) {
                res.logs.forEach(msg => logToConsole(msg, "success"));
                playAudioFX("success");
            } else if (res && res.message) {
                logToConsole(res.message, "success");
                playAudioFX("success");
            }
            refreshSystemStats();
        } catch (err) {
            logToConsole(`Action error: ${err}`, "warning");
        }
    } else {
        logToConsole(`Action '${actionId}' executed successfully.`, "success");
        playAudioFX("success");
    }
}

// Process Manager
async function refreshTopProcesses() {
    try {
        let procs = [];
        if (window.pywebview && window.pywebview.api && window.pywebview.api.get_top_ram_processes) {
            procs = await window.pywebview.api.get_top_ram_processes(15);
        } else {
            procs = [
                { pid: 14208, name: "Valorant.exe", mem_mb: 2480.5 },
                { pid: 8912, name: "chrome.exe", mem_mb: 1220.2 },
                { pid: 4310, name: "Discord.exe", mem_mb: 460.1 },
                { pid: 9812, name: "Spotify.exe", mem_mb: 280.4 },
                { pid: 2104, name: "Steam.exe", mem_mb: 210.8 }
            ];
        }

        const tbody = document.getElementById("top-procs-tbody");
        if (!tbody) return;
        tbody.innerHTML = "";

        procs.forEach(p => {
            const tr = document.createElement("tr");
            tr.className = "proc-row";
            tr.innerHTML = `
                <td><code style="color:var(--text-muted);">${p.pid}</code></td>
                <td><strong>${p.name}</strong></td>
                <td class="text-cyan">${p.mem_mb} MB</td>
                <td><button class="btn btn-xs btn-red" onclick="triggerAction('kill_process', ${p.pid})">End Process</button></td>
            `;
            tbody.appendChild(tr);
        });
        filterProcessTable();
    } catch (e) {
        console.error("Process refresh error:", e);
    }
}

function filterProcessTable() {
    const searchEl = document.getElementById("proc-search");
    if (!searchEl) return;
    const query = searchEl.value.toLowerCase();
    document.querySelectorAll(".proc-row").forEach(row => {
        const text = row.innerText.toLowerCase();
        row.style.display = text.includes(query) ? "" : "none";
    });
}

let procRefreshInterval = null;
function switchPage(pageId) {
    playAudioFX("click");
    document.querySelectorAll(".nav-item").forEach(item => {
        item.classList.toggle("active", item.getAttribute("data-page") === pageId);
    });

    document.querySelectorAll(".page").forEach(page => {
        page.classList.toggle("active", page.id === pageId);
    });

    if (pageId === "page-processes") {
        refreshTopProcesses();
        if (!procRefreshInterval) {
            procRefreshInterval = setInterval(refreshTopProcesses, 3500);
        }
    } else {
        if (procRefreshInterval) {
            clearInterval(procRefreshInterval);
            procRefreshInterval = null;
        }
    }
}

function updateSoundIcon() {
    const wrapper = document.getElementById("sound-icon-wrapper");
    if (!wrapper) return;
    if (isAudioMuted) {
        wrapper.innerHTML = `<svg class="icon-svg icon-badge" viewBox="0 0 24 24"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><line x1="23" y1="9" x2="17" y2="15"></line><line x1="17" y1="9" x2="23" y2="15"></line></svg>`;
    } else {
        wrapper.innerHTML = `<svg class="icon-svg icon-badge" viewBox="0 0 24 24"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>`;
    }
}

function toggleAudioMute() {
    isAudioMuted = !isAudioMuted;
    appConfig.sound_effects = !isAudioMuted;
    const soundToggle = document.getElementById("setting-sound-toggle");
    if (soundToggle) soundToggle.checked = !isAudioMuted;
    updateSoundIcon();

    if (window.pywebview && window.pywebview.api && window.pywebview.api.update_setting) {
        window.pywebview.api.update_setting("sound_effects", !isAudioMuted);
    }
    if (!isAudioMuted) playAudioFX("click");
}

function playAudioFX(type) {
    if (isAudioMuted) return;
    try {
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        if (audioCtx.state === 'suspended') audioCtx.resume();

        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);

        const now = audioCtx.currentTime;
        if (type === "click") {
            osc.frequency.setValueAtTime(600, now);
            osc.frequency.exponentialRampToValueAtTime(800, now + 0.04);
            gain.gain.setValueAtTime(0.05, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);
            osc.start(now);
            osc.stop(now + 0.04);
        } else if (type === "success") {
            osc.frequency.setValueAtTime(440, now);
            osc.frequency.exponentialRampToValueAtTime(880, now + 0.12);
            gain.gain.setValueAtTime(0.08, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
            osc.start(now);
            osc.stop(now + 0.12);
        } else if (type === "action") {
            osc.frequency.setValueAtTime(520, now);
            osc.frequency.exponentialRampToValueAtTime(320, now + 0.08);
            gain.gain.setValueAtTime(0.06, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
            osc.start(now);
            osc.stop(now + 0.08);
        } else if (type === "warning") {
            osc.frequency.setValueAtTime(300, now);
            osc.frequency.exponentialRampToValueAtTime(200, now + 0.1);
            gain.gain.setValueAtTime(0.08, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.1);
            osc.start(now);
            osc.stop(now + 0.1);
        }
    } catch (e) {}
}

function logToConsole(message, level = "info") {
    const output = document.getElementById("console-output");
    if (!output) return;

    const time = new Date().toLocaleTimeString();
    let prefix = "[INFO]";
    if (level === "success") prefix = "[SUCCESS]";
    if (level === "warning") prefix = "[WARNING]";

    output.value += `\n[${time}] ${prefix} ${message}`;
    output.scrollTop = output.scrollHeight;
}

function clearConsoleLog() {
    playAudioFX("click");
    document.getElementById("console-output").value = "[SYSTEM] Log cleared.";
}

function copyConsoleLog() {
    playAudioFX("click");
    const output = document.getElementById("console-output");
    navigator.clipboard.writeText(output.value);
    logToConsole("Activity log copied to clipboard!", "success");
}

// Interactive Feature Guide Data & Controller
let guideSteps = [
    {
        id: "welcome",
        category: "🚀 GETTING STARTED",
        title: "Welcome to Mr. Drew's Device & FPS Optimizer",
        icon: "⚡",
        color: "#00F0FF",
        how: "Combines a native C++ engine, GPU shader management, real-time memory compaction, and process priority tuning into one fast suite.",
        why: "Eliminates game micro-stutters, reclaims 2 to 5 GB physical RAM, lowers input lag, and prevents texture pop-in.",
        when: "Run before starting gaming sessions (Fortnite, Valorant, Roblox, Unreal Engine), or run Smart Auto-Guard in the background.",
        action_id: null,
        action_label: null
    },
    {
        id: "fps_booster",
        category: "🎮 GAMING ENGINE",
        title: "RUN FPS & GAME BOOSTER",
        icon: "🎮",
        color: "#F59E0B",
        how: "Locks system timer resolution to 1.0ms, flushes GPU shader caches (Nvidia/AMD/DirectX), and elevates game process CPU priority to High.",
        why: "Fixes frame drops, removes micro-stutters, and lowers input latency in competitive games.",
        when: "Click right before launching your game or whenever you notice stutters during gameplay.",
        action_id: "run_fps_booster",
        action_label: "🧪 Try FPS Booster Now"
    },
    {
        id: "asset_loader",
        category: "🎮 GAMING ENGINE",
        title: "Fast Asset Loader",
        icon: "🚀",
        color: "#10B981",
        how: "Sets Disk I/O priority to High (ProcessIoPriorityHigh) for active game processes and protects loaded game assets from RAM eviction.",
        why: "Accelerates map loading, texture streaming, and 3D asset rendering; stops texture pop-in.",
        when: "Use when loading open-world games, map transitions, or heavy Roblox / Unreal Engine projects.",
        action_id: "accelerate_asset_loading",
        action_label: "🧪 Test Asset Loader"
    },
    {
        id: "potato_mode",
        category: "🥔 LOW-SPEC ENGINE",
        title: "4GB Potato Mode",
        icon: "🥔",
        color: "#EAB308",
        how: "Triggers aggressive memory compaction targeting 1.5 GB free RAM, drops inactive page caches, and terminates background bloatware.",
        why: "Enables smooth gaming and app performance on budget/low-spec devices with 4GB to 8GB physical RAM without paging stutters.",
        when: "Activate on low-end laptops or budget PCs before launching any game.",
        action_id: "run_potato_mode",
        action_label: "🧪 Test Potato Mode"
    },
    {
        id: "ultimate_power",
        category: "⚡ POWER ENGINE",
        title: "Ultimate Power Mode",
        icon: "⚡",
        color: "#10B981",
        how: "Forces Windows OS power scheme to High / Ultimate Performance, disabling CPU core parking and power throttling.",
        why: "Ensures CPU cores run at peak clock speeds without sudden frequency drops during demanding scenes.",
        when: "Enable when gaming, video editing, or rendering on desktop or plugged-in laptops.",
        action_id: "enable_power_plan",
        action_label: "🧪 Enable Ultimate Power"
    },
    {
        id: "monster_optimizer",
        category: "🧠 MEMORY ENGINE",
        title: "RUN MONSTER OPTIMIZER",
        icon: "🔥",
        color: "#A855F7",
        how: "Multi-stage deep RAM recovery: compacts background working sets via EmptyWorkingSet, flushes kernel standby page list, and sweeps temp memory.",
        why: "Recovers the maximum possible physical memory (up to 3-6 GB RAM) in one click without closing critical system apps.",
        when: "Use when overall RAM usage exceeds 80%, or before running memory-heavy applications.",
        action_id: "run_monster_optimizer",
        action_label: "🧪 Run Monster Optimizer"
    },
    {
        id: "trim_ram",
        category: "🧠 MEMORY ENGINE",
        title: "Trim App RAM",
        icon: "✂️",
        color: "#00F0FF",
        how: "Iterates through non-critical user applications and compacts their active working set memory into physical free RAM.",
        why: "Instantly reclaims RAM held hostage by web browsers (Chrome, Edge) and background software (Discord, Spotify).",
        when: "Use while multitasking when you want to free RAM without quitting open applications.",
        action_id: "trim_working_sets",
        action_label: "🧪 Trim App RAM Now"
    },
    {
        id: "purge_standby",
        category: "🧠 MEMORY ENGINE",
        title: "Purge Standby RAM",
        icon: "🛡️",
        color: "#3B82F6",
        how: "Calls C++ NtSetSystemInformation with SystemMemoryListInformation (or POSIX drop_caches on Linux/macOS) to clear cached standby list memory.",
        why: "Fixes Windows Standby RAM bugs that cause game crashes and hitching when free RAM drops to zero.",
        when: "Use when Standby cached memory is high and free memory is low.",
        action_id: "purge_standby",
        action_label: "🧪 Purge Standby RAM"
    },
    {
        id: "clear_temp",
        category: "🧹 CLEANING ENGINE",
        title: "Clear Temp Files",
        icon: "🧹",
        color: "#EC4899",
        how: "Recursively cleans %TEMP%, %SystemRoot%\\Temp, log caches, and leftover installer clutter while bypassing locked files safely.",
        why: "Frees up gigabytes of SSD/HDD drive space and removes system clutter.",
        when: "Run weekly or whenever drive space is tight.",
        action_id: "clear_temp",
        action_label: "🧪 Clear Temp Files"
    },
    {
        id: "game_picker",
        category: "🎯 PRIORITY TUNER",
        title: "Boost Game Priority",
        icon: "🎯",
        color: "#F59E0B",
        how: "Lets you pick your active game process and elevates its OS scheduling priority class to High Priority.",
        why: "Guarantees that the CPU allocates maximum execution clock cycles to your game over background threads.",
        when: "Use whenever playing competitive multiplayer games or resource-demanding titles.",
        action_id: "open_game_picker",
        action_label: "🧪 Select & Boost Game"
    },
    {
        id: "shader_cleaner",
        category: "🎨 GRAPHICS TUNER",
        title: "Clean Shader Cache",
        icon: "🧹",
        color: "#00F0FF",
        how: "Sweeps compiled DirectX, OpenGL, Vulkan, Nvidia (DXCache/GLCache), AMD (DxCache), and Intel GPU shader caches.",
        why: "Fixes corrupted shader stuttering, visual artifacts, and frame drops caused by stale shader caches.",
        when: "Run after updating graphics drivers, installing game updates, or experiencing graphical stutters.",
        action_id: "clean_shader_cache",
        action_label: "🧪 Clean Shader Cache"
    },
    {
        id: "end_bloatware",
        category: "🛡️ SECURITY & CLEANING",
        title: "End Bloatware",
        icon: "🚫",
        color: "#EF4444",
        how: "Safely terminates non-essential background bloatware (OneDrive, Widgets, Teams, Cortana) protected by safety whitelists.",
        why: "Stops unwanted background telemetry, reduces background CPU usage, and saves memory.",
        when: "Run on computer startup or before launching games.",
        action_id: "kill_bloatware",
        action_label: "🧪 Terminate Bloatware"
    }
];

let currentGuideStepIndex = 0;

function renderGuideStep(index) {
    if (index < 0) index = 0;
    if (index >= guideSteps.length) index = guideSteps.length - 1;
    currentGuideStepIndex = index;

    const step = guideSteps[index];
    const body = document.getElementById("guide-step-body");
    const select = document.getElementById("guide-topic-select");
    const tryBtn = document.getElementById("guide-try-btn");
    const prevBtn = document.getElementById("guide-prev-btn");
    const nextBtn = document.getElementById("guide-next-btn");

    if (select) select.value = step.id;
    if (prevBtn) prevBtn.disabled = (index === 0);
    if (nextBtn) nextBtn.disabled = (index === guideSteps.length - 1);

    if (tryBtn) {
        if (step.action_id) {
            tryBtn.style.display = "";
            tryBtn.innerText = step.action_label || "🧪 Try Feature Now";
        } else {
            tryBtn.style.display = "none";
        }
    }

    if (body) {
        body.innerHTML = `
            <div class="guide-step-card">
                <div class="guide-step-header">
                    <span class="guide-category-badge">${step.category}</span>
                    <span style="font-size:11px; color:var(--text-muted);">Step ${index + 1} of ${guideSteps.length}</span>
                </div>
                <h4 style="font-size:15px; font-weight:800; color:${step.color}; margin:0; display:flex; align-items:center; gap:8px;">
                    <span>${step.icon}</span>
                    <span>${step.title}</span>
                </h4>
                <div class="guide-block how">
                    <span class="guide-block-title" style="color:var(--cyan);">🛠️ How It Works (Technical Engine)</span>
                    <span class="guide-block-desc">${step.how}</span>
                </div>
                <div class="guide-block why">
                    <span class="guide-block-title" style="color:var(--green);">💡 Why Use It (Performance Benefit)</span>
                    <span class="guide-block-desc">${step.why}</span>
                </div>
                <div class="guide-block when">
                    <span class="guide-block-title" style="color:var(--amber);">⏱️ When To Use It (Best Scenario)</span>
                    <span class="guide-block-desc">${step.when}</span>
                </div>
            </div>
        `;
    }
}

function selectGuideTopic(stepId) {
    playAudioFX("click");
    const idx = guideSteps.findIndex(s => s.id === stepId);
    if (idx !== -1) renderGuideStep(idx);
}

function nextGuideStep() {
    playAudioFX("click");
    renderGuideStep(currentGuideStepIndex + 1);
}

function prevGuideStep() {
    playAudioFX("click");
    renderGuideStep(currentGuideStepIndex - 1);
}

function tryCurrentGuideAction() {
    const step = guideSteps[currentGuideStepIndex];
    if (step && step.action_id) {
        playAudioFX("action");
        closeGuideModal();
        switchPage("page-dashboard");
        triggerAction(step.action_id);
    }
}

async function openGuideModal() {
    playAudioFX("click");
    const select = document.getElementById("guide-topic-select");
    if (select && select.options.length === 0) {
        if (window.pywebview && window.pywebview.api && window.pywebview.api.get_guide_steps) {
            try {
                const backendSteps = await window.pywebview.api.get_guide_steps();
                if (backendSteps && backendSteps.length) {
                    guideSteps = backendSteps;
                }
            } catch (e) {}
        }
        select.innerHTML = "";
        guideSteps.forEach((s, i) => {
            const opt = document.createElement("option");
            opt.value = s.id;
            opt.innerText = `${i + 1}. ${s.title}`;
            select.appendChild(opt);
        });
    }

    renderGuideStep(currentGuideStepIndex);
    const overlay = document.getElementById("guide-modal-overlay");
    if (overlay) overlay.classList.add("active");
}

function closeGuideModal() {
    playAudioFX("click");
    const overlay = document.getElementById("guide-modal-overlay");
    if (overlay) overlay.classList.remove("active");
}

// Global Keyboard & Overlay backdrop event listeners
window.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
        closeGuideModal();
    } else if (e.key === "ArrowRight") {
        const overlay = document.getElementById("guide-modal-overlay");
        if (overlay && overlay.classList.contains("active")) nextGuideStep();
    } else if (e.key === "ArrowLeft") {
        const overlay = document.getElementById("guide-modal-overlay");
        if (overlay && overlay.classList.contains("active")) prevGuideStep();
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const overlay = document.getElementById("guide-modal-overlay");
    if (overlay) {
        overlay.addEventListener("click", (e) => {
            if (e.target === overlay) closeGuideModal();
        });
    }
});
