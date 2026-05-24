<script setup>
</script>

<template>
  <section class="py-24 bg-tech-dark text-surface relative overflow-hidden">
    <!-- Background layers -->
    <div class="absolute inset-0 bg-tech-grid bg-grid-size opacity-10 pointer-events-none"></div>
    <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-tech-blue/5 rounded-full blur-3xl pointer-events-none"></div>

    <div class="max-w-screen-2xl mx-auto px-8 relative z-10">
      <!-- Section Header -->
      <div class="text-center mb-20 reveal-down">
        <h2 class="font-headline text-4xl font-bold text-white drop-shadow-[0_0_10px_rgba(25,118,210,0.4)]">
          智能<span class="text-tech-blue-light">架构</span>
        </h2>
        <p class="text-white/50 font-body mt-3 text-lg">三大核心能力，重构农业植保体验</p>
      </div>

      <!-- 3-Column Bento -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">

        <!-- Feature 1: 拍照即诊 -->
        <div class="glass-card bg-tech-darker/60 rounded-[2rem] p-8 flex flex-col h-full hover:-translate-y-2 hover:shadow-[0_0_40px_rgba(25,118,210,0.2)] transition-all duration-500 reveal-up group border border-primary/30 hover:border-tech-blue/40">
          <h3 class="font-headline text-2xl font-bold mb-2 text-primary-fixed group-hover:text-tech-blue-light transition-colors duration-300">
            拍照即诊
          </h3>
          <p class="text-surface/70 mb-8 flex-grow">
            通过边缘优化模型进行即时视觉诊断。
          </p>
          <!-- Code Block -->
          <div class="bg-black/50 rounded-xl p-4 font-mono text-xs text-primary-fixed/80 overflow-hidden border border-primary/20 group-hover:border-tech-blue/30 shadow-inner relative transition-colors duration-300">
            <span class="text-tech-blue-light">POST</span>
            /api/v1/diagnose<br />
            {<br />
            &nbsp;&nbsp;"image_b64": "...",<br />
            &nbsp;&nbsp;"crop_type": "番茄",<br />
            &nbsp;&nbsp;"context": {"humidity": 85}<br />
            }<br />
            <span class="text-tech-cyan drop-shadow-[0_0_5px_rgba(0,188,212,0.6)]">&gt;&gt; Result: 晚疫病 (94%)</span>
            <span class="inline-block w-2 h-4 bg-tech-blue-light ml-0.5 align-middle cursor-blink"></span>
          </div>
        </div>

        <!-- Feature 2: 图谱推理 (Hero Card) -->
        <div class="glass-card bg-gradient-to-br from-primary/30 to-tech-blue/20 text-white rounded-[2rem] p-8 flex flex-col h-full relative overflow-hidden hover:-translate-y-2 transition-all duration-500 shadow-[0_0_30px_rgba(25,118,210,0.2)] hover:shadow-[0_0_50px_rgba(25,118,210,0.4)] reveal-up delay-100 border border-tech-blue/30">
          <div class="relative z-10 flex flex-col h-full">
            <h3 class="font-headline text-2xl font-bold mb-2 text-white">
              图谱推理
            </h3>
            <p class="text-white/80 mb-8">
              GraphRAG 多跳推理引擎。
            </p>
            <!-- Stat with particle ring -->
            <div class="relative mt-auto pt-8">
              <!-- Decorative rings around the number -->
              <svg class="absolute -top-2 -left-4 w-36 h-36 pointer-events-none rotate-ring opacity-60" viewBox="0 0 144 144">
                <circle cx="72" cy="72" r="62" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="1" stroke-dasharray="40 100" />
                <circle cx="72" cy="72" r="54" fill="none" stroke="rgba(0,188,212,0.3)" stroke-width="1.5" stroke-dasharray="20 80" />
                <circle cx="72" cy="72" r="46" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="1" stroke-dasharray="60 60" />
              </svg>
              <div class="text-6xl font-headline font-bold text-white drop-shadow-[0_0_20px_rgba(255,255,255,0.5)]">
                +32%
              </div>
              <p class="text-sm text-white/70 mt-2">
                在复杂的症状重叠场景中，准确率提升优于标准 RAG。
              </p>
            </div>
          </div>
          <!-- Decorative blurs -->
          <div class="absolute -bottom-20 -right-20 w-64 h-64 bg-tech-blue rounded-full blur-3xl opacity-30 mix-blend-screen"></div>
          <div class="absolute -top-10 -left-10 w-40 h-40 bg-tech-cyan rounded-full blur-3xl opacity-20 mix-blend-screen"></div>
        </div>

        <!-- Feature 3: 动态大屏 -->
        <div class="glass-card bg-tech-darker/60 rounded-[2rem] p-8 flex flex-col h-full hover:-translate-y-2 hover:shadow-[0_0_40px_rgba(25,118,210,0.2)] transition-all duration-500 reveal-up delay-200 group border border-primary/30 hover:border-tech-blue/40">
          <h3 class="font-headline text-2xl font-bold mb-2 text-primary-fixed group-hover:text-tech-blue-light transition-colors duration-300">
            动态大屏
          </h3>
          <p class="text-surface/70 mb-8 flex-grow">
            合作中心的区域态势感知。
          </p>
          <!-- Mock Dashboard -->
          <div class="w-full aspect-[4/3] bg-black/50 rounded-xl border border-primary/20 group-hover:border-tech-blue/30 p-4 flex flex-col gap-2 relative overflow-hidden scan-line transition-colors duration-300">
            <div class="absolute inset-0 tech-dot-bg opacity-20"></div>
            <div class="flex justify-between items-center pb-2 border-b border-primary/20 group-hover:border-tech-blue/30 relative z-10 transition-colors">
              <div class="h-2 w-16 bg-tech-blue/60 rounded"></div>
              <div class="flex gap-1.5">
                <div class="w-2 h-2 rounded-full bg-tech-cyan animate-pulse shadow-[0_0_6px_rgba(0,188,212,0.6)]"></div>
                <div class="w-2 h-2 rounded-full bg-tech-blue-light animate-pulse delay-200 shadow-[0_0_6px_rgba(66,165,245,0.6)]"></div>
              </div>
            </div>
            <div class="flex-grow flex gap-2 pt-2 relative z-10">
              <div class="w-1/3 h-full bg-tech-blue/10 rounded border border-tech-blue/20 flex items-end p-2 backdrop-blur-sm">
                <div class="w-full h-1/2 bg-gradient-to-t from-tech-blue/60 to-tech-cyan/40 rounded-sm shadow-[0_0_10px_rgba(0,188,212,0.4)]"></div>
              </div>
              <div class="w-2/3 h-full bg-tech-blue/5 rounded border border-tech-blue/20 flex items-center justify-center backdrop-blur-sm">
                <div class="w-12 h-12 rounded-full border-4 border-tech-blue/20 border-t-tech-blue-light animate-spin shadow-[0_0_15px_rgba(25,118,210,0.4)]"></div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
    <!-- Bottom fade: tech-dark -> #0d1f11 -->
    <div class="absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-t from-[#0d1f11]/60 to-transparent pointer-events-none z-[2]"></div>
  </section>
</template>
