<script setup>
</script>

<template>
  <header class="relative min-h-[921px] flex items-center overflow-hidden bg-surface scan-line">
    <!-- Radial gradient background -->
    <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-tech-blue/8 via-primary/5 to-surface opacity-90 pointer-events-none"></div>
    <!-- Tech dot overlay -->
    <div class="absolute inset-0 tech-dot-bg opacity-30 pointer-events-none"></div>

    <div class="max-w-screen-2xl mx-auto px-8 w-full grid grid-cols-1 lg:grid-cols-2 gap-16 items-center relative z-10">
      <!-- Left Content -->
      <div class="space-y-8 max-w-xl">
        <!-- Badge -->
        <div class="inline-flex items-center gap-2 bg-white/80 backdrop-blur-sm px-4 py-2 rounded-full text-sm font-medium text-tech-blue reveal-down border border-tech-blue/30 border-glow-pulse">
          <span class="w-2 h-2 rounded-full bg-tech-blue animate-pulse shadow-[0_0_8px_rgba(25,118,210,0.6)]"></span>
          基于 GraphRAG 的智能诊断
        </div>

        <!-- Title with gradient -->
        <h1 class="font-headline text-5xl md:text-7xl font-bold leading-[1.1] text-on-surface reveal-down delay-100">
          智农大夫: <br />
          <span class="bg-gradient-to-r from-primary via-primary to-tech-blue bg-clip-text text-transparent tracking-tight relative">
            农业病虫害
          </span>
          <br />
          AI诊断专家
        </h1>

        <p class="font-body text-lg text-on-surface/80 leading-relaxed reveal-up delay-200">
          将土壤的原始生命力与人工智能的临床精度相连接。体验高端、权威的农业植保与病害管理方案。
        </p>

        <!-- CTA Buttons -->
        <div class="flex items-center gap-4 pt-4 reveal-up delay-300">
          <router-link
            to="/chat"
            class="cta-ripple bg-accent-orange text-white px-8 py-4 rounded-full font-headline font-bold text-lg hover:shadow-glow-orange-lg transition-all duration-400 flex items-center gap-2 hover:-translate-y-1 group"
          >
            立即体验AI问诊
            <span class="material-symbols-outlined group-hover:translate-x-1 transition-transform">arrow_forward</span>
          </router-link>
          <router-link
            to="/graph"
            class="px-8 py-4 rounded-full font-headline font-bold text-lg border-2 border-tech-blue/40 text-tech-blue hover:bg-tech-blue/10 hover:border-tech-blue hover:shadow-glow-blue transition-all duration-400 hover:-translate-y-1"
          >
            探索知识图谱
          </router-link>
        </div>
      </div>

      <!-- Right: Graph Visualization -->
      <div class="relative h-[600px] hidden lg:block reveal-up delay-200">
        <div class="absolute inset-0 glass-card-blue rounded-[2rem] p-8 flex items-center justify-center shadow-[0_0_60px_rgba(25,118,210,0.1)] bg-white/50 border border-tech-blue/20">
          <div class="relative w-full h-full max-w-md">
            <!-- Rotating Ring around center -->
            <svg class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-40 h-40 pointer-events-none z-15 rotate-ring" viewBox="0 0 160 160">
              <circle cx="80" cy="80" r="75" fill="none" stroke="rgba(25,118,210,0.2)" stroke-width="2" stroke-dasharray="90 150" />
              <circle cx="80" cy="80" r="75" fill="none" stroke="rgba(0,188,212,0.3)" stroke-width="1.5" stroke-dasharray="40 200" />
            </svg>

            <!-- Center Node -->
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-24 h-24 bg-gradient-to-br from-primary to-tech-blue text-white rounded-full flex flex-col items-center justify-center shadow-[0_0_30px_rgba(25,118,210,0.5)] pulse-node z-20 border-2 border-white/30">
              <span class="material-symbols-outlined text-3xl mb-1">psychiatry</span>
              <span class="text-xs font-headline">智能诊断</span>
            </div>

            <!-- Satellite Node 1 - Green -->
            <div class="absolute top-[8%] left-[18%] w-20 h-20 bg-white text-primary rounded-full flex flex-col items-center justify-center shadow-[0_0_20px_rgba(46,125,50,0.25)] z-10 pulse-node delay-100 border border-primary/20">
              <span class="material-symbols-outlined text-2xl" style="font-variation-settings: 'FILL' 1;">eco</span>
              <span class="text-[12px] mt-1 font-bold">环保理念</span>
            </div>

            <!-- Satellite Node 2 - Blue (NEW) -->
            <div class="absolute top-[18%] right-[12%] w-20 h-20 bg-white text-tech-blue rounded-full flex flex-col items-center justify-center shadow-[0_0_20px_rgba(25,118,210,0.25)] z-10 pulse-node delay-200 border border-tech-blue/20">
              <span class="material-symbols-outlined text-2xl">bug_report</span>
              <span class="text-[12px] mt-1 font-bold">病虫害库</span>
            </div>

            <!-- Satellite Node 3 - Green -->
            <div class="absolute top-[70%] left-[8%] w-20 h-20 bg-white text-primary rounded-full flex flex-col items-center justify-center shadow-[0_0_20px_rgba(46,125,50,0.25)] z-10 pulse-node delay-300 border border-primary/20">
              <span class="material-symbols-outlined text-2xl">medical_services</span>
              <span class="text-[12px] mt-1 font-bold">治疗方案</span>
            </div>

            <!-- Satellite Node 4 - Cyan (NEW) -->
            <div class="absolute top-[72%] right-[22%] w-20 h-20 bg-white text-tech-cyan rounded-full flex flex-col items-center justify-center shadow-[0_0_20px_rgba(0,188,212,0.25)] z-10 pulse-node delay-400 border border-tech-cyan/20">
              <span class="material-symbols-outlined text-2xl">analytics</span>
              <span class="text-[12px] mt-1 font-bold">数据支持</span>
            </div>

            <!-- SVG Connecting Lines -->
            <svg class="absolute inset-0 w-full h-full pointer-events-none z-0" stroke-width="2">
              <!-- Green lines -->
              <line class="glow-line stroke-primary/40" x1="50%" x2="25%" y1="50%" y2="13%"></line>
              <line class="glow-line stroke-primary/40" x1="50%" x2="15%" y1="50%" y2="80%"></line>
              <!-- Blue lines -->
              <line class="glow-line stroke-tech-blue/40" x1="50%" x2="82%" y1="50%" y2="23%" style="filter: drop-shadow(0 0 4px rgba(25,118,210,0.5));"></line>
              <line class="glow-line stroke-tech-cyan/40" x1="50%" x2="72%" y1="50%" y2="82%" style="filter: drop-shadow(0 0 4px rgba(0,188,212,0.5));"></line>
              <!-- Cross connection dashed -->
              <line class="glow-line stroke-tech-blue/25" stroke-dasharray="4 4" x1="25%" x2="82%" y1="13%" y2="23%"></line>
              <line class="glow-line stroke-tech-cyan/25" stroke-dasharray="4 4" x1="15%" x2="72%" y1="80%" y2="82%"></line>
            </svg>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
/* Scan line override for proper rendering within header */
header.scan-line::after {
  z-index: 5;
}
</style>
