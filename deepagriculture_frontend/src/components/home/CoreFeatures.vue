<script setup>
</script>

<template>
  <section class="py-24 bg-tech-dark text-surface relative overflow-hidden">
    <!-- Background layers -->
    <div class="absolute inset-0 bg-tech-grid bg-grid-size opacity-10 pointer-events-none"></div>
    <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-tech-blue/4 rounded-full blur-3xl pointer-events-none"></div>
    <!-- Secondary glow -->
    <div class="absolute top-[20%] right-[10%] w-[400px] h-[400px] bg-tech-cyan/4 rounded-full blur-[100px] pointer-events-none"></div>

    <div class="max-w-screen-2xl mx-auto px-8 relative z-10">
      <!-- Section Header -->
      <div class="text-center mb-20 reveal-down">
        <div class="inline-flex items-center gap-2 bg-tech-blue/10 border border-tech-blue/20 rounded-full px-4 py-1.5 mb-6">
          <span class="flex gap-1">
            <span class="w-1.5 h-1.5 rounded-full bg-tech-blue-light animate-pulse"></span>
            <span class="w-1.5 h-1.5 rounded-full bg-tech-cyan animate-pulse" style="animation-delay: 0.3s;"></span>
            <span class="w-1.5 h-1.5 rounded-full bg-tech-blue-light animate-pulse" style="animation-delay: 0.6s;"></span>
          </span>
          <span class="font-headline text-xs tracking-widest uppercase text-tech-blue-light">Core Engine</span>
        </div>
        <h2 class="font-headline text-4xl md:text-5xl font-bold text-white drop-shadow-[0_0_10px_rgba(25,118,210,0.4)]">
          智能<span class="text-tech-blue-light">架构</span>
        </h2>
        <p class="text-white/50 font-body mt-3 text-lg">三大核心能力，重构农业植保体验</p>
      </div>

      <!-- 3-Column Bento -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">

        <!-- ===== CARD 1: 拍照即诊 — Sci-Fi Scan Terminal ===== -->
        <div class="group relative rounded-[2rem] p-8 flex flex-col h-full transition-all duration-500 ease-[cubic-bezier(0.25,1,0.5,1)] hover:-translate-y-3 reveal-up"
          style="background: linear-gradient(145deg, rgba(13,51,17,0.9) 0%, rgba(10,30,14,0.95) 100%); border: 1px solid rgba(25,118,210,0.25);">
          <!-- Corner accents -->
          <div class="absolute top-3 left-3 w-5 h-5 border-l-2 border-t-2 border-tech-blue/40 rounded-tl-lg group-hover:border-tech-blue-light/70 group-hover:shadow-[0_0_8px_rgba(25,118,210,0.5)] transition-all duration-500"></div>
          <div class="absolute top-3 right-3 w-5 h-5 border-r-2 border-t-2 border-tech-blue/40 rounded-tr-lg group-hover:border-tech-blue-light/70 group-hover:shadow-[0_0_8px_rgba(25,118,210,0.5)] transition-all duration-500"></div>
          <div class="absolute bottom-3 left-3 w-5 h-5 border-l-2 border-b-2 border-tech-blue/40 rounded-bl-lg group-hover:border-tech-blue-light/70 transition-all duration-500"></div>
          <div class="absolute bottom-3 right-3 w-5 h-5 border-r-2 border-b-2 border-tech-blue/40 rounded-br-lg group-hover:border-tech-blue-light/70 transition-all duration-500"></div>

          <!-- Hover glow border -->
          <div class="absolute inset-0 rounded-[2rem] opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"
            style="box-shadow: inset 0 0 60px rgba(25,118,210,0.08), 0 0 40px rgba(25,118,210,0.15);"></div>

          <div class="relative z-10 flex flex-col h-full">
            <div class="flex items-center gap-3 mb-3">
              <div class="w-10 h-10 rounded-xl bg-tech-blue/15 flex items-center justify-center group-hover:bg-tech-blue/25 transition-all duration-400 group-hover:shadow-[0_0_15px_rgba(25,118,210,0.4)]">
                <span class="material-symbols-outlined text-tech-blue-light text-xl">photo_camera</span>
              </div>
              <h3 class="font-headline text-xl font-bold text-white group-hover:text-tech-blue-light transition-colors duration-300">拍照即诊</h3>
            </div>
            <p class="text-white/50 text-sm mb-6">边缘优化模型 · 毫秒级视觉诊断</p>

            <!-- Scan Terminal -->
            <div class="relative mt-auto bg-black/60 rounded-2xl border border-tech-blue/15 group-hover:border-tech-blue/30 overflow-hidden transition-colors duration-500">
              <!-- Scan line animation -->
              <div class="absolute inset-0 pointer-events-none z-[2]">
                <div class="absolute top-0 left-0 right-0 h-[2px] bg-tech-cyan/40 animate-[terminalScan_3s_ease-in-out_infinite] shadow-[0_0_15px_rgba(0,188,212,0.6)]"></div>
              </div>

              <!-- Image placeholder with crosshair -->
              <div class="relative h-36 bg-gradient-to-br from-tech-dark/80 to-black/80 flex items-center justify-center overflow-hidden">
                <!-- Grid overlay -->
                <div class="absolute inset-0 opacity-[0.06]" style="background-image: linear-gradient(rgba(0,188,212,0.5) 1px, transparent 1px), linear-gradient(90deg, rgba(0,188,212,0.5) 1px, transparent 1px); background-size: 16px 16px;"></div>
                <!-- Crosshair -->
                <div class="relative z-10">
                  <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-16 h-16 border border-tech-cyan/40 rounded-full animate-pulse shadow-[0_0_15px_rgba(0,188,212,0.3)]"></div>
                  <div class="w-px h-14 bg-tech-cyan/50 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"></div>
                  <div class="h-px w-14 bg-tech-cyan/50 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"></div>
                  <span class="material-symbols-outlined text-4xl text-tech-cyan/30">psychiatry</span>
                </div>
                <!-- Corner brackets -->
                <div class="absolute top-2 left-2 w-3 h-3 border-l border-t border-tech-cyan/30"></div>
                <div class="absolute top-2 right-2 w-3 h-3 border-r border-t border-tech-cyan/30"></div>
                <div class="absolute bottom-2 left-2 w-3 h-3 border-l border-b border-tech-cyan/30"></div>
                <div class="absolute bottom-2 right-2 w-3 h-3 border-r border-b border-tech-cyan/30"></div>
              </div>

              <!-- Terminal output -->
              <div class="px-4 py-3 font-mono text-[11px] leading-relaxed border-t border-tech-blue/10 group-hover:border-tech-blue/20 transition-colors">
                <div class="text-tech-blue-light/80">&gt; analyze --crop tomato</div>
                <div class="text-white/40 mt-0.5">Scanning leaf surface...</div>
                <div class="flex items-center gap-1.5 mt-1">
                  <span class="text-tech-cyan drop-shadow-[0_0_6px_rgba(0,188,212,0.8)]">&gt;&gt; 晚疫病</span>
                  <span class="text-accent-orange font-bold">94.2%</span>
                  <span class="inline-block w-1.5 h-3.5 bg-tech-blue-light ml-0.5 cursor-blink shadow-[0_0_5px_rgba(66,165,245,0.8)]"></span>
                </div>
              </div>
            </div>

            <!-- Status indicator -->
            <div class="flex items-center gap-2 mt-4 pt-3 border-t border-white/5">
              <span class="w-2 h-2 rounded-full bg-tech-cyan animate-pulse shadow-[0_0_6px_rgba(0,188,212,0.8)]"></span>
              <span class="text-white/30 text-xs font-headline tracking-wide">VISION MODEL ACTIVE</span>
            </div>
          </div>
        </div>

        <!-- ===== CARD 2: 图谱推理 — Hero Holographic Graph ===== -->
        <div class="group relative rounded-[2rem] p-8 flex flex-col h-full transition-all duration-500 ease-[cubic-bezier(0.25,1,0.5,1)] hover:-translate-y-3 reveal-up delay-100"
          style="background: linear-gradient(145deg, rgba(13,55,35,0.95) 0%, rgba(8,30,50,0.95) 100%); border: 1px solid rgba(0,188,212,0.35);">
          <!-- Corner accents (cyan theme) -->
          <div class="absolute top-3 left-3 w-5 h-5 border-l-2 border-t-2 border-tech-cyan/50 rounded-tl-lg group-hover:border-tech-cyan group-hover:shadow-[0_0_10px_rgba(0,188,212,0.6)] transition-all duration-500"></div>
          <div class="absolute top-3 right-3 w-5 h-5 border-r-2 border-t-2 border-tech-cyan/50 rounded-tr-lg group-hover:border-tech-cyan group-hover:shadow-[0_0_10px_rgba(0,188,212,0.6)] transition-all duration-500"></div>
          <div class="absolute bottom-3 left-3 w-5 h-5 border-l-2 border-b-2 border-tech-cyan/50 rounded-bl-lg group-hover:border-tech-cyan transition-all duration-500"></div>
          <div class="absolute bottom-3 right-3 w-5 h-5 border-r-2 border-b-2 border-tech-cyan/50 rounded-br-lg group-hover:border-tech-cyan transition-all duration-500"></div>

          <!-- Hero hover glow -->
          <div class="absolute inset-0 rounded-[2rem] opacity-30 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"
            style="box-shadow: inset 0 0 80px rgba(0,188,212,0.08), 0 0 60px rgba(0,188,212,0.2);"></div>

          <div class="relative z-10 flex flex-col h-full">
            <div class="flex items-center gap-3 mb-3">
              <div class="w-10 h-10 rounded-xl bg-tech-cyan/15 flex items-center justify-center group-hover:bg-tech-cyan/25 transition-all duration-400 group-hover:shadow-[0_0_20px_rgba(0,188,212,0.5)]">
                <span class="material-symbols-outlined text-tech-cyan text-xl">hub</span>
              </div>
              <h3 class="font-headline text-xl font-bold text-white group-hover:text-tech-cyan transition-colors duration-300">图谱推理</h3>
            </div>
            <p class="text-white/50 text-sm mb-6">GraphRAG 多跳推理 · 关联发现</p>

            <!-- Graph Visualization -->
            <div class="relative mt-auto flex items-center justify-center h-48">
              <!-- Outer ring -->
              <svg class="absolute inset-0 w-full h-full animate-[spin_30s_linear_infinite] pointer-events-none opacity-70" viewBox="0 0 200 200">
                <circle cx="100" cy="100" r="88" fill="none" stroke="rgba(0,188,212,0.2)" stroke-width="1" stroke-dasharray="30 15 4 15" />
              </svg>
              <!-- Mid ring (reverse) -->
              <svg class="absolute inset-0 w-full h-full animate-[spin_20s_linear_infinite_reverse] pointer-events-none opacity-60" viewBox="0 0 200 200">
                <circle cx="100" cy="100" r="68" fill="none" stroke="rgba(66,165,245,0.25)" stroke-width="1.5" stroke-dasharray="8 12" />
              </svg>
              <!-- Inner ring -->
              <svg class="absolute inset-0 w-full h-full animate-[spin_14s_linear_infinite] pointer-events-none opacity-80" viewBox="0 0 200 200">
                <circle cx="100" cy="100" r="48" fill="none" stroke="rgba(129,199,132,0.3)" stroke-width="1" stroke-dasharray="3 8" />
              </svg>

              <!-- SVG Graph nodes and edges -->
              <svg class="absolute inset-0 w-full h-full pointer-events-none" viewBox="0 0 200 200">
                <!-- Edge lines -->
                <line x1="100" y1="100" x2="55" y2="42" stroke="rgba(0,188,212,0.35)" stroke-width="1" class="data-flow-dash" />
                <line x1="100" y1="100" x2="155" y2="50" stroke="rgba(66,165,245,0.35)" stroke-width="1" class="data-flow-dash" style="animation-delay: 0.5s;" />
                <line x1="100" y1="100" x2="40" y2="140" stroke="rgba(129,199,132,0.3)" stroke-width="1" class="data-flow-dash" style="animation-delay: 1s;" />
                <line x1="100" y1="100" x2="160" y2="130" stroke="rgba(0,188,212,0.3)" stroke-width="1" class="data-flow-dash" style="animation-delay: 1.5s;" />
                <line x1="55" y1="42" x2="155" y2="50" stroke="rgba(66,165,245,0.15)" stroke-width="0.5" class="data-flow-dash" style="animation-delay: 0.8s;" />
                <line x1="40" y1="140" x2="160" y2="130" stroke="rgba(129,199,132,0.15)" stroke-width="0.5" class="data-flow-dash" style="animation-delay: 2s;" />

                <!-- Nodes -->
                <circle cx="100" cy="100" r="7" fill="rgba(0,188,212,0.4)" stroke="#00BCD4" stroke-width="2" class="animate-pulse">
                  <animate attributeName="r" values="7;9;7" dur="2s" repeatCount="indefinite" />
                </circle>
                <circle cx="55" cy="42" r="5" fill="rgba(66,165,245,0.5)" stroke="#42A5F5" stroke-width="1.5">
                  <animate attributeName="opacity" values="1;0.5;1" dur="3s" repeatCount="indefinite" />
                </circle>
                <circle cx="155" cy="50" r="4" fill="rgba(129,199,132,0.6)" stroke="#81C784" stroke-width="1.5">
                  <animate attributeName="opacity" values="0.6;1;0.6" dur="2.5s" repeatCount="indefinite" />
                </circle>
                <circle cx="40" cy="140" r="5" fill="rgba(0,188,212,0.5)" stroke="#00BCD4" stroke-width="1.5">
                  <animate attributeName="opacity" values="0.7;1;0.7" dur="3.5s" repeatCount="indefinite" />
                </circle>
                <circle cx="160" cy="130" r="4" fill="rgba(66,165,245,0.5)" stroke="#42A5F5" stroke-width="1.5">
                  <animate attributeName="opacity" values="1;0.4;1" dur="2.8s" repeatCount="indefinite" />
                </circle>

                <!-- Floating data particles along edges -->
                <circle r="2" fill="#00BCD4" opacity="0.8">
                  <animateMotion dur="3s" repeatCount="indefinite" path="M100,100 L55,42 L100,100" />
                </circle>
                <circle r="1.5" fill="#42A5F5" opacity="0.7">
                  <animateMotion dur="4s" repeatCount="indefinite" path="M100,100 L155,50 L100,100" />
                </circle>
                <circle r="1.5" fill="#81C784" opacity="0.6">
                  <animateMotion dur="3.5s" repeatCount="indefinite" path="M100,100 L40,140 L100,100" />
                </circle>
              </svg>

              <!-- Center stat -->
              <div class="relative z-10 text-center">
                <div class="text-5xl font-headline font-bold text-white drop-shadow-[0_0_25px_rgba(0,188,212,0.6)]">+32%</div>
                <div class="text-white/50 text-xs font-headline tracking-wide mt-1">准确率提升</div>
              </div>
            </div>

            <!-- Labels -->
            <div class="flex justify-between items-center mt-4 pt-3 border-t border-white/5">
              <span class="text-white/30 text-xs font-headline tracking-wide">5 NODES · 6 EDGES</span>
              <span class="flex gap-1">
                <span class="w-1.5 h-1.5 rounded-full bg-tech-cyan animate-pulse"></span>
                <span class="w-1.5 h-1.5 rounded-full bg-tech-blue-light animate-pulse" style="animation-delay: 0.3s;"></span>
                <span class="w-1.5 h-1.5 rounded-full bg-primary-fixed animate-pulse" style="animation-delay: 0.6s;"></span>
              </span>
            </div>
          </div>
        </div>

        <!-- ===== CARD 3: 动态大屏 — Live Monitor Dashboard ===== -->
        <div class="group relative rounded-[2rem] p-8 flex flex-col h-full transition-all duration-500 ease-[cubic-bezier(0.25,1,0.5,1)] hover:-translate-y-3 reveal-up delay-200"
          style="background: linear-gradient(145deg, rgba(13,51,17,0.9) 0%, rgba(10,30,14,0.95) 100%); border: 1px solid rgba(25,118,210,0.25);">
          <!-- Corner accents -->
          <div class="absolute top-3 left-3 w-5 h-5 border-l-2 border-t-2 border-tech-blue/40 rounded-tl-lg group-hover:border-tech-blue-light/70 group-hover:shadow-[0_0_8px_rgba(25,118,210,0.5)] transition-all duration-500"></div>
          <div class="absolute top-3 right-3 w-5 h-5 border-r-2 border-t-2 border-tech-blue/40 rounded-tr-lg group-hover:border-tech-blue-light/70 group-hover:shadow-[0_0_8px_rgba(25,118,210,0.5)] transition-all duration-500"></div>
          <div class="absolute bottom-3 left-3 w-5 h-5 border-l-2 border-b-2 border-tech-blue/40 rounded-bl-lg group-hover:border-tech-blue-light/70 transition-all duration-500"></div>
          <div class="absolute bottom-3 right-3 w-5 h-5 border-r-2 border-b-2 border-tech-blue/40 rounded-br-lg group-hover:border-tech-blue-light/70 transition-all duration-500"></div>

          <div class="absolute inset-0 rounded-[2rem] opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"
            style="box-shadow: inset 0 0 60px rgba(25,118,210,0.08), 0 0 40px rgba(25,118,210,0.15);"></div>

          <div class="relative z-10 flex flex-col h-full">
            <div class="flex items-center gap-3 mb-3">
              <div class="w-10 h-10 rounded-xl bg-tech-blue/15 flex items-center justify-center group-hover:bg-tech-blue/25 transition-all duration-400 group-hover:shadow-[0_0_15px_rgba(25,118,210,0.4)]">
                <span class="material-symbols-outlined text-tech-blue-light text-xl">monitoring</span>
              </div>
              <h3 class="font-headline text-xl font-bold text-white group-hover:text-tech-blue-light transition-colors duration-300">动态大屏</h3>
            </div>
            <p class="text-white/50 text-sm mb-6">全国态势感知 · 实时预警</p>

            <!-- Live Dashboard -->
            <div class="relative mt-auto bg-black/60 rounded-2xl border border-tech-blue/15 group-hover:border-tech-blue/30 overflow-hidden transition-colors duration-500">
              <!-- Header bar -->
              <div class="flex items-center justify-between px-4 py-2.5 border-b border-tech-blue/10 group-hover:border-tech-blue/20 transition-colors">
                <div class="flex gap-1.5">
                  <span class="w-2 h-2 rounded-full bg-red-400/80 shadow-[0_0_4px_rgba(248,113,113,0.6)]"></span>
                  <span class="w-2 h-2 rounded-full bg-yellow-400/80 shadow-[0_0_4px_rgba(250,204,21,0.6)]"></span>
                  <span class="w-2 h-2 rounded-full bg-green-400/80 shadow-[0_0_4px_rgba(74,222,128,0.6)]"></span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-[10px] text-tech-cyan/60 font-mono tracking-wider">LIVE</span>
                  <span class="w-1.5 h-1.5 rounded-full bg-tech-cyan animate-pulse shadow-[0_0_6px_rgba(0,188,212,0.8)]"></span>
                </div>
              </div>

              <!-- Dashboard content -->
              <div class="p-4 space-y-3">
                <!-- Chart bars -->
                <div class="space-y-2">
                  <div class="flex items-end gap-2 h-16">
                    <div v-for="(h, i) in [45, 72, 38, 85, 55, 68, 42, 90]" :key="'bar'+i"
                      class="flex-1 rounded-t-sm transition-all duration-700"
                      :style="{
                        height: h + '%',
                        background: i === 3 || i === 7 ? 'linear-gradient(to top, rgba(0,188,212,0.8), rgba(0,188,212,0.3))' : 'linear-gradient(to top, rgba(25,118,210,0.6), rgba(25,118,210,0.2))',
                        boxShadow: i === 3 || i === 7 ? '0 0 10px rgba(0,188,212,0.4)' : 'none',
                        animationDelay: (i * 0.1) + 's',
                      }"
                    ></div>
                  </div>
                  <!-- X-axis labels -->
                  <div class="flex justify-between text-[8px] text-white/25 font-mono">
                    <span v-for="label in ['浙', '苏', '粤', '鲁', '豫', '川', '鄂', '湘']" :key="label">{{ label }}</span>
                  </div>
                </div>

                <!-- Bottom stats row -->
                <div class="grid grid-cols-3 gap-2 pt-2 border-t border-tech-blue/10 group-hover:border-tech-blue/20 transition-colors">
                  <div class="text-center">
                    <div class="text-tech-cyan text-sm font-headline font-bold drop-shadow-[0_0_6px_rgba(0,188,212,0.5)]">2.4K</div>
                    <div class="text-white/25 text-[9px] font-headline tracking-wide">在线设备</div>
                  </div>
                  <div class="text-center">
                    <div class="text-accent-orange text-sm font-headline font-bold drop-shadow-[0_0_6px_rgba(255,152,0,0.5)]">12</div>
                    <div class="text-white/25 text-[9px] font-headline tracking-wide">预警区域</div>
                  </div>
                  <div class="text-center">
                    <div class="text-primary-fixed text-sm font-headline font-bold drop-shadow-[0_0_6px_rgba(129,199,132,0.5)]">98.5%</div>
                    <div class="text-white/25 text-[9px] font-headline tracking-wide">系统在线</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Status indicator -->
            <div class="flex items-center gap-2 mt-4 pt-3 border-t border-white/5">
              <span class="w-2 h-2 rounded-full bg-tech-cyan animate-pulse shadow-[0_0_6px_rgba(0,188,212,0.8)]"></span>
              <span class="text-white/30 text-xs font-headline tracking-wide">STREAMING DATA · 12 REGIONS</span>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- Bottom fade -->
    <div class="absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-t from-[#0d1f11]/60 to-transparent pointer-events-none z-[2]"></div>
  </section>
</template>

<style scoped>
@keyframes terminalScan {
  0%, 100% { top: 0%; opacity: 0; }
  20%, 80% { opacity: 1; }
  50% { top: 92%; }
}
</style>
