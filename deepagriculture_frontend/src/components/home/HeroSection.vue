
<script setup>
const statBadges = [
  { value: '120+', label: '覆盖作物' },
  { value: '2000+', label: '病虫害库' },
  { value: '94%', label: '识别准确率' },
];
</script>

<template>
  <header class="relative min-h-[105vh] flex items-center overflow-hidden hero-lab">
    <!-- ===== Rich Forest-Green Background ===== -->
    <div class="absolute inset-0 bg-[#0d2a1a]"></div>

    <!-- Ambient depth gradient (lighter, more vibrant) -->
    <div class="absolute inset-0 bg-gradient-to-b from-[#123820] via-[#18452c] to-[#225e3d]"></div>

    <!-- Hexagonal Grid (precision agriculture) -->
    <div class="absolute inset-0 hex-grid-bg opacity-[0.09] pointer-events-none"></div>

    <!-- Tech dot overlay -->
    <div class="absolute inset-0 tech-dot-bg opacity-25 pointer-events-none"></div>

    <!-- Atmospheric Glows (brighter) -->
    <div class="absolute top-[-15%] right-[-5%] w-[650px] h-[650px] bg-tech-blue/15 rounded-full blur-[130px] pointer-events-none"></div>
    <div class="absolute bottom-[-10%] left-[-5%] w-[550px] h-[550px] bg-primary/12 rounded-full blur-[110px] pointer-events-none"></div>
    <div class="absolute top-[25%] left-[45%] w-[350px] h-[350px] bg-tech-cyan/8 rounded-full blur-[90px] pointer-events-none"></div>
    <!-- Extra central warm glow -->
    <div class="absolute top-[40%] left-[30%] w-[450px] h-[450px] bg-tech-blue/6 rounded-full blur-[150px] pointer-events-none"></div>

    <!-- Bottom fade-to-light gradient (bridges to PainPoints) -->
    <div class="absolute bottom-0 left-0 right-0 h-96 bg-gradient-to-t from-surface/60 via-surface/25 to-transparent pointer-events-none z-[3]"></div>

    <!-- Full-width Scan Line -->
    <div class="absolute inset-0 pointer-events-none z-[2] overflow-hidden">
      <div class="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-tech-cyan/30 to-transparent hero-scan"></div>
    </div>

    <!-- ===== Main Content Grid ===== -->
    <div class="max-w-screen-2xl mx-auto px-8 w-full grid grid-cols-1 lg:grid-cols-2 gap-12 items-center relative z-10">

      <!-- ===== LEFT: Text Content ===== -->
      <div class="space-y-8 max-w-xl pt-8">
        <!-- Floating Data Badges -->
        <div class="flex flex-wrap gap-3 reveal-down">
          <div
            v-for="(badge, idx) in statBadges"
            :key="badge.label"
            :class="[
              'flex items-center gap-2 px-4 py-2.5 rounded-full text-sm font-medium border backdrop-blur-md transition-all duration-500 hover:scale-105',
              idx === 0 ? 'bg-tech-blue/10 border-tech-blue/30 text-tech-blue-light hover:shadow-[0_0_20px_rgba(25,118,210,0.3)]' : '',
              idx === 1 ? 'bg-tech-cyan/10 border-tech-cyan/30 text-tech-cyan hover:shadow-[0_0_20px_rgba(0,188,212,0.25)]' : '',
              idx === 2 ? 'bg-accent-orange/10 border-accent-orange/30 text-accent-orange hover:shadow-[0_0_20px_rgba(255,152,0,0.25)]' : '',
            ]"
          >
            <span class="w-1.5 h-1.5 rounded-full animate-pulse"
              :class="[
                idx === 0 ? 'bg-tech-blue-light shadow-[0_0_6px_rgba(66,165,245,0.8)]' : '',
                idx === 1 ? 'bg-tech-cyan shadow-[0_0_6px_rgba(0,188,212,0.8)]' : '',
                idx === 2 ? 'bg-accent-orange shadow-[0_0_6px_rgba(255,152,0,0.8)]' : '',
              ]"
            ></span>
            <span class="font-headline font-bold text-base">{{ badge.value }}</span>
            <span class="text-white/50 font-headline text-xs tracking-wide">{{ badge.label }}</span>
          </div>
        </div>

        <!-- GraphRAG Badge -->
        <div class="inline-flex items-center gap-2 bg-white/5 backdrop-blur-md px-4 py-2.5 rounded-full text-sm font-medium text-tech-blue-light reveal-down border border-tech-blue/20 border-glow-pulse">
          <span class="w-2 h-2 rounded-full bg-tech-blue-light animate-pulse shadow-[0_0_8px_rgba(66,165,245,0.8)]"></span>
          基于 GraphRAG 的智能诊断
        </div>

        <!-- Main Title -->
        <h1 class="font-headline text-5xl md:text-7xl font-bold leading-[1.1] reveal-down delay-100">
          <span class="text-white">智农大夫:</span><br />
          <span class="holo-text bg-gradient-to-r from-[#a5d6a7] via-tech-blue-light to-tech-cyan bg-clip-text text-transparent">
            农业病虫害
          </span><br />
          <span class="text-white/90">AI诊断专家</span>
        </h1>

        <p class="font-body text-lg text-white/60 leading-relaxed reveal-up delay-200 max-w-lg">
          将土壤的原始生命力与人工智能的临床精度相连接。体验高端、权威的农业植保与病害管理方案。
        </p>

        <!-- CTA -->
        <div class="flex items-center gap-4 pt-4 reveal-up delay-300">
          <router-link
            to="/chat"
            class="cta-ripple bg-accent-orange text-white px-8 py-4 rounded-full font-headline font-bold text-lg hover:shadow-glow-orange-lg transition-all duration-400 flex items-center gap-2 hover:-translate-y-1 group z-[1]"
          >
            立即体验AI问诊
            <span class="material-symbols-outlined group-hover:translate-x-1 transition-transform">arrow_forward</span>
          </router-link>
          <router-link
            to="/graph"
            class="px-8 py-4 rounded-full font-headline font-bold text-lg border-2 border-tech-blue/40 text-tech-blue-light hover:bg-tech-blue/10 hover:border-tech-blue-light hover:shadow-glow-blue transition-all duration-400 hover:-translate-y-1"
          >
            探索知识图谱
          </router-link>
        </div>
      </div>

      <!-- ===== RIGHT: Refined Holographic Crop Globe ===== -->
      <div class="relative h-[650px] hidden lg:flex items-center justify-center reveal-up delay-200">

        <!-- Platform base glow -->
        <div class="absolute bottom-[8%] w-72 h-1.5 bg-gradient-to-r from-transparent via-tech-cyan/25 to-transparent rounded-full blur-[2px]"></div>
        <div class="absolute bottom-[6%] w-52 h-0.5 bg-gradient-to-r from-transparent via-tech-blue/30 to-transparent rounded-full blur-[1px]"></div>

        <!-- ===== Main Globe Container ===== -->
        <div class="relative w-[370px] h-[370px] flex items-center justify-center">

          <!-- Glass Sphere Base -->
          <div class="absolute inset-[8%] rounded-full bg-gradient-radial from-tech-blue/8 via-tech-cyan/4 to-transparent backdrop-blur-[2px] border border-tech-blue/15 shadow-[inset_0_0_80px_rgba(0,188,212,0.06)]"></div>

          <!-- ===== Data Rings (various angles & speeds) ===== -->
          <!-- Ring 1: Outer, slow, horizontal-ish -->
          <svg class="absolute inset-[-5%] w-[110%] h-[110%] animate-[spin_22s_linear_infinite] pointer-events-none"
            style="transform: rotateX(72deg);">
            <circle cx="50%" cy="50%" r="45%" fill="none" stroke="rgba(25,118,210,0.25)" stroke-width="1" stroke-dasharray="80 20 10 20" />
          </svg>

          <!-- Ring 2: Mid, medium speed, tilted opposite -->
          <svg class="absolute inset-[-3%] w-[106%] h-[106%] animate-[spin_16s_linear_infinite_reverse] pointer-events-none"
            style="transform: rotateX(-55deg) rotateY(25deg);">
            <circle cx="50%" cy="50%" r="45%" fill="none" stroke="rgba(0,188,212,0.3)" stroke-width="1.5" stroke-dasharray="40 30 5 30" />
          </svg>

          <!-- Ring 3: Inner, faster, steep tilt -->
          <svg class="absolute inset-0 w-full h-full animate-[spin_12s_linear_infinite] pointer-events-none"
            style="transform: rotateY(60deg) rotateX(20deg);">
            <circle cx="50%" cy="50%" r="42%" fill="none" stroke="rgba(66,165,245,0.2)" stroke-width="1" stroke-dasharray="6 10" />
          </svg>

          <!-- Ring 4: Latitude lines (static wireframe) -->
          <svg class="absolute inset-[5%] w-[90%] h-[90%] pointer-events-none opacity-30">
            <ellipse cx="50%" cy="30%" rx="42%" ry="8%" fill="none" stroke="rgba(129,199,132,0.4)" stroke-width="0.5" />
            <ellipse cx="50%" cy="50%" rx="45%" ry="10%" fill="none" stroke="rgba(129,199,132,0.5)" stroke-width="0.5" />
            <ellipse cx="50%" cy="70%" rx="42%" ry="8%" fill="none" stroke="rgba(129,199,132,0.4)" stroke-width="0.5" />
          </svg>

          <!-- Ring 5: Longitude lines (static wireframe) -->
          <svg class="absolute inset-[5%] w-[90%] h-[90%] pointer-events-none opacity-20"
            style="transform: rotateY(15deg);">
            <ellipse cx="50%" cy="50%" rx="8%" ry="45%" fill="none" stroke="rgba(0,188,212,0.4)" stroke-width="0.5" />
            <ellipse cx="50%" cy="50%" rx="4%" ry="45%" fill="none" stroke="rgba(0,188,212,0.3)" stroke-width="0.5" />
          </svg>

          <!-- ===== Inner Crop Leaf Silhouettes ===== -->
          <div class="absolute inset-[18%] flex items-center justify-center">

            <!-- Central core -->
            <div class="absolute w-16 h-16 bg-gradient-radial from-tech-cyan/25 to-transparent rounded-full blur-lg animate-pulse"></div>

            <!-- Leaf 1: Left, larger -->
            <svg class="absolute w-full h-full animate-[cropFloat_8s_ease-in-out_infinite]" viewBox="0 0 240 240" fill="none">
              <defs>
                <radialGradient id="leafGrad1" cx="100" cy="100" r="100" gradientUnits="userSpaceOnUse">
                  <stop offset="0%" stop-color="rgba(129,199,132,0.5)" />
                  <stop offset="100%" stop-color="rgba(46,125,50,0.15)" />
                </radialGradient>
              </defs>
              <path d="M120 120 Q70 40 30 55 Q10 70 60 105 Q95 130 120 120Z"
                fill="url(#leafGrad1)" stroke="rgba(129,199,132,0.7)" stroke-width="1.2" />
              <path d="M120 120 Q75 55 80 50" stroke="rgba(166,213,168,0.5)" stroke-width="0.6" fill="none" />
              <path d="M120 120 Q65 70 55 75" stroke="rgba(166,213,168,0.3)" stroke-width="0.4" fill="none" />
            </svg>

            <!-- Leaf 2: Right, larger -->
            <svg class="absolute w-full h-full animate-[cropFloat_9s_ease-in-out_infinite_1s]" viewBox="0 0 240 240" fill="none">
              <defs>
                <radialGradient id="leafGrad2" cx="140" cy="100" r="100" gradientUnits="userSpaceOnUse">
                  <stop offset="0%" stop-color="rgba(129,199,132,0.45)" />
                  <stop offset="100%" stop-color="rgba(46,125,50,0.1)" />
                </radialGradient>
              </defs>
              <path d="M120 120 Q170 40 210 55 Q230 70 180 105 Q145 130 120 120Z"
                fill="url(#leafGrad2)" stroke="rgba(129,199,132,0.6)" stroke-width="1.2" />
              <path d="M120 120 Q165 55 160 50" stroke="rgba(166,213,168,0.4)" stroke-width="0.6" fill="none" />
            </svg>

            <!-- Leaf 3: Top -->
            <svg class="absolute w-full h-full animate-[cropFloat_9.5s_ease-in-out_infinite_0.3s]" viewBox="0 0 240 240" fill="none">
              <path d="M120 120 Q95 10 115 5 Q140 10 120 120Z"
                fill="rgba(129,199,132,0.3)" stroke="rgba(0,188,212,0.5)" stroke-width="1" />
              <line x1="120" y1="120" x2="118" y2="12" stroke="rgba(0,188,212,0.3)" stroke-width="0.6" />
            </svg>

            <!-- Leaf 4: Bottom small -->
            <svg class="absolute w-full h-full animate-[cropFloat_7.5s_ease-in-out_infinite_2s]" viewBox="0 0 240 240" fill="none">
              <path d="M120 120 Q85 200 75 215 Q65 225 95 200 Q112 185 120 120Z"
                fill="rgba(46,125,50,0.25)" stroke="rgba(66,165,245,0.5)" stroke-width="1" />
            </svg>

            <!-- Leaf 5: Bottom-right accent -->
            <svg class="absolute w-full h-full animate-[cropFloat_8.2s_ease-in-out_infinite_1.5s]" viewBox="0 0 240 240" fill="none">
              <path d="M120 120 Q155 185 175 200 Q190 210 160 190 Q135 170 120 120Z"
                fill="rgba(0,188,212,0.15)" stroke="rgba(0,188,212,0.35)" stroke-width="0.8" />
            </svg>

            <!-- Center crop icon -->
            <div class="relative z-10 flex flex-col items-center">
              <span class="material-symbols-outlined text-[42px] text-tech-cyan/70 drop-shadow-[0_0_18px_rgba(0,188,212,0.5)]">psychiatry</span>
            </div>
          </div>

          <!-- ===== Sphere Scan Line ===== -->
          <div class="absolute left-[-5%] right-[-5%] h-[2px] bg-gradient-to-r from-transparent via-tech-cyan/50 to-transparent holo-sphere-scan pointer-events-none z-[5]"></div>

          <!-- ===== Rising Particles ===== -->
          <div class="absolute inset-0 pointer-events-none overflow-hidden rounded-full">
            <div v-for="i in 15" :key="'p'+i"
              class="absolute w-1 h-1 rounded-full particle-rise"
              :class="i % 3 === 0 ? 'bg-tech-cyan/70' : i % 3 === 1 ? 'bg-tech-blue-light/60' : 'bg-primary-fixed/50'"
              :style="{
                left: `${8 + Math.random() * 84}%`,
                bottom: `${Math.random() * 15}%`,
                animationDelay: `${Math.random() * 3.5}s`,
                animationDuration: `${3 + Math.random() * 4}s`,
              }"
            ></div>
          </div>

        </div>

        <!-- ===== Floating Data Callouts (font-headline) ===== -->
        <!-- Callout 1: Top Right -->
        <div class="absolute top-[6%] right-[4%] bg-black/50 backdrop-blur-lg border border-tech-blue/30 rounded-xl px-4 py-2.5 animate-[calloutFloat_4s_ease-in-out_infinite] shadow-[0_0_25px_rgba(25,118,210,0.2)]">
          <div class="font-headline text-[10px] tracking-widest uppercase text-white/40 mb-1">GraphRAG Engine</div>
          <div class="flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 rounded-full bg-tech-cyan animate-pulse shadow-[0_0_6px_rgba(0,188,212,0.8)]"></span>
            <span class="font-headline text-sm font-semibold text-tech-cyan tracking-wide">知识图谱已连接</span>
          </div>
        </div>

        <!-- Callout 2: Bottom Left -->
        <div class="absolute bottom-[18%] left-[0%] bg-black/50 backdrop-blur-lg border border-primary/25 rounded-xl px-4 py-2.5 animate-[calloutFloat_5s_ease-in-out_infinite_1s] shadow-[0_0_25px_rgba(46,125,50,0.15)]">
          <div class="font-headline text-[10px] tracking-widest uppercase text-white/40 mb-1">Vision Model</div>
          <div class="flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 rounded-full bg-primary-fixed animate-pulse shadow-[0_0_6px_rgba(129,199,132,0.8)]"></span>
            <span class="font-headline text-sm font-semibold text-primary-fixed tracking-wide">视觉模型就绪</span>
          </div>
        </div>

        <!-- Callout 3: Mid Right -->
        <div class="absolute top-[40%] right-[0%] bg-black/50 backdrop-blur-lg border border-tech-cyan/30 rounded-xl px-4 py-2.5 animate-[calloutFloat_4.5s_ease-in-out_infinite_0.5s] shadow-[0_0_25px_rgba(0,188,212,0.2)]">
          <div class="font-headline text-[10px] tracking-widest uppercase text-white/40 mb-1">Accuracy</div>
          <div class="font-headline text-xl font-bold text-tech-cyan tracking-tight">94.2<span class="text-sm text-tech-cyan/60">%</span></div>
        </div>

      </div>
    </div>
  </header>
</template>

<style scoped>
/* === Hero Lab Container === */
.hero-lab {
  background: radial-gradient(ellipse at 60% 45%, rgba(30, 85, 50, 0.7) 0%, #0d2a1a 55%);
}

/* === Hexagonal Grid === */
.hex-grid-bg {
  background-image:
    linear-gradient(30deg, rgba(25, 118, 210, 1) 1px, transparent 1px),
    linear-gradient(-30deg, rgba(25, 118, 210, 1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(25, 118, 210, 0.5) 1px, transparent 1px);
  background-size: 60px 104px, 60px 104px, 60px 104px;
  background-position: 0 0, 0 0, 0 52px;
}

/* === Scan Line Animation === */
.hero-scan {
  animation: heroScanSweep 6s ease-in-out infinite;
}
@keyframes heroScanSweep {
  0%, 100% { top: 0%; opacity: 0; }
  15% { opacity: 1; }
  85% { opacity: 1; }
  100% { top: 100%; opacity: 0; }
}

/* === Holographic Text Effect === */
.holo-text {
  filter: drop-shadow(0 0 20px rgba(0, 188, 212, 0.35)) drop-shadow(0 0 40px rgba(25, 118, 210, 0.25));
}

/* === Sphere Scan Line === */
.holo-sphere-scan {
  animation: sphereScan 3.5s ease-in-out infinite;
}
@keyframes sphereScan {
  0%, 100% { top: 5%; opacity: 0; }
  30%, 70% { opacity: 1; }
  50% { top: 92%; }
}

/* === Particle Rise === */
.particle-rise {
  animation: particleRise linear infinite;
}
@keyframes particleRise {
  0% {
    opacity: 0;
    transform: translateY(0) scale(1);
  }
  20% { opacity: 1; }
  100% {
    opacity: 0;
    transform: translateY(-370px) scale(0.2);
  }
}

/* === Crop Leaf Float === */
@keyframes cropFloat {
  0%, 100% { transform: translateY(0) scale(1); }
  25% { transform: translateY(-5px) scale(1.02); }
  75% { transform: translateY(5px) scale(0.98); }
}

/* === Callout Float === */
@keyframes calloutFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
</style>
