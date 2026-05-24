<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const canvasRef = ref(null);
const isLargeScreen = ref(false);

let animFrame = null;
let particles = [];
let ctx = null;
let width = 0;
let height = 0;

const PARTICLE_COUNT = 80;
const CONNECTION_DIST = 150;
const PARTICLE_COLORS = [
  'rgba(25, 118, 210, 0.5)',   // tech-blue
  'rgba(66, 165, 245, 0.4)',   // tech-blue-light
  'rgba(0, 188, 212, 0.35)',   // tech-cyan
  'rgba(129, 199, 132, 0.3)',  // light green
  'rgba(46, 125, 50, 0.25)',   // primary green
];

function createParticles() {
  particles = [];
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
      radius: Math.random() * 2 + 1,
      color: PARTICLE_COLORS[Math.floor(Math.random() * PARTICLE_COLORS.length)],
    });
  }
}

function draw() {
  if (!ctx || !canvasRef.value) return;

  ctx.clearRect(0, 0, width, height);

  // Update & draw particles
  for (const p of particles) {
    p.x += p.vx;
    p.y += p.vy;

    // Bounce off edges
    if (p.x < 0 || p.x > width) p.vx *= -1;
    if (p.y < 0 || p.y > height) p.vy *= -1;

    // Wrap around instead of bounce for smoother effect
    if (p.x < -10) p.x = width + 10;
    if (p.x > width + 10) p.x = -10;
    if (p.y < -10) p.y = height + 10;
    if (p.y > height + 10) p.y = -10;

    // Draw particle
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
    ctx.fillStyle = p.color;
    ctx.fill();
  }

  // Draw connections
  for (let i = 0; i < particles.length; i++) {
    for (let j = i + 1; j < particles.length; j++) {
      const dx = particles[i].x - particles[j].x;
      const dy = particles[i].y - particles[j].y;
      const dist = Math.sqrt(dx * dx + dy * dy);

      if (dist < CONNECTION_DIST) {
        const opacity = (1 - dist / CONNECTION_DIST) * 0.15;
        ctx.beginPath();
        ctx.moveTo(particles[i].x, particles[i].y);
        ctx.lineTo(particles[j].x, particles[j].y);
        ctx.strokeStyle = `rgba(66, 165, 245, ${opacity})`;
        ctx.lineWidth = 0.5;
        ctx.stroke();
      }
    }
  }

  animFrame = requestAnimationFrame(draw);
}

function resize() {
  if (!canvasRef.value) return;
  const rect = canvasRef.value.parentElement.getBoundingClientRect();
  width = rect.width;
  height = rect.height;
  canvasRef.value.width = width;
  canvasRef.value.height = height;
  createParticles();
}

function setup() {
  const mq = window.matchMedia('(min-width: 1024px)');
  isLargeScreen.value = mq.matches;

  if (!isLargeScreen.value) return;

  ctx = canvasRef.value.getContext('2d');
  resize();
  draw();
  window.addEventListener('resize', resize);
}

function handleVisibility() {
  if (document.hidden) {
    if (animFrame) cancelAnimationFrame(animFrame);
    animFrame = null;
  } else {
    if (!animFrame) draw();
  }
}

onMounted(() => {
  setup();
  document.addEventListener('visibilitychange', handleVisibility);
});

onUnmounted(() => {
  if (animFrame) cancelAnimationFrame(animFrame);
  window.removeEventListener('resize', resize);
  document.removeEventListener('visibilitychange', handleVisibility);
});
</script>

<template>
  <canvas
    ref="canvasRef"
    class="fixed inset-0 pointer-events-none z-0 opacity-60"
    :class="{ 'hidden': !isLargeScreen }"
    aria-hidden="true"
  />
</template>
