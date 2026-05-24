<script setup>
</script>

<template>
  <section class="py-24 bg-[#0d1f11] relative overflow-hidden">
    <!-- Background -->
    <div class="absolute inset-0 bg-tech-grid bg-grid-size opacity-10 pointer-events-none"></div>
    <div class="absolute top-0 right-0 w-[400px] h-[400px] bg-tech-blue/4 rounded-full blur-3xl pointer-events-none"></div>

    <div class="max-w-[1200px] mx-auto px-8 grid grid-cols-1 lg:grid-cols-12 gap-16 relative z-10">
      <!-- Sticky Left Header -->
      <div class="col-span-12 lg:col-span-4 relative">
        <div class="sticky top-24 space-y-6 reveal-down">
          <h2 class="font-headline text-4xl md:text-5xl font-bold text-white mb-2 drop-shadow-[0_0_10px_rgba(25,118,210,0.4)]">
            智能引擎<span class="text-tech-blue-light">运作全流程</span>
          </h2>
          <p class="text-lg text-tech-blue-light/70 font-medium font-body leading-relaxed">
            从数据到答案，全链路技术闭环，保障输出精准可靠
          </p>
          <div class="w-16 h-1 bg-gradient-to-r from-tech-blue to-tech-cyan rounded-full mt-8"></div>
        </div>
      </div>

      <!-- Timeline Right -->
      <div class="col-span-12 lg:col-span-8 relative pt-8">
        <!-- Timeline Line SVG with flowing dot -->
        <svg class="absolute left-[27px] top-[10%] w-2 h-[80%] z-0 hidden md:block" preserveaspectratio="none">
          <line class="timeline-line stroke-tech-blue/30" stroke-width="2" x1="50%" x2="50%" y1="0" y2="100%"></line>
          <!-- Flowing dot along the line -->
          <circle class="flow-dot" cx="50%" r="4" fill="#42A5F5" filter="url(#flow-glow)">
            <animate attributeName="cy" from="0%" to="100%" dur="6s" repeatCount="indefinite" />
          </circle>
          <defs>
            <filter id="flow-glow">
              <feGaussianBlur stdDeviation="3" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>
        </svg>

        <div class="space-y-16 relative z-10">

          <!-- Step 1 -->
          <div class="timeline-item flex flex-col md:flex-row gap-6 md:gap-10 group">
            <div class="flex-shrink-0 flex items-start">
              <div class="w-14 h-14 rounded-2xl bg-[#0d3311]/60 border border-tech-blue/20 flex items-center justify-center timeline-icon-container backdrop-blur-sm z-10 mt-1 relative">
                <span class="absolute -top-1.5 -right-1.5 w-5 h-5 bg-tech-blue rounded-full text-[10px] font-bold text-white flex items-center justify-center">1</span>
                <span class="material-symbols-outlined text-tech-blue-light/60 timeline-icon text-2xl">dataset</span>
              </div>
            </div>
            <div class="timeline-content pt-2 pb-8 border-b border-primary/10 last:border-0 w-full">
              <h3 class="text-xl font-bold text-white mb-3 font-headline group-hover:text-tech-blue-light transition-colors">
                多源数据采集
              </h3>
              <p class="text-white/60 font-body leading-relaxed text-[15px]">
                权威植保数据集、专业文献、专家知识库、全国病虫害监测数据汇聚
              </p>
            </div>
          </div>

          <!-- Step 2 -->
          <div class="timeline-item flex flex-col md:flex-row gap-6 md:gap-10 group">
            <div class="flex-shrink-0 flex items-start">
              <div class="w-14 h-14 rounded-2xl bg-[#0d3311]/60 border border-tech-blue/20 flex items-center justify-center timeline-icon-container backdrop-blur-sm z-10 mt-1 relative">
                <span class="absolute -top-1.5 -right-1.5 w-5 h-5 bg-tech-blue rounded-full text-[10px] font-bold text-white flex items-center justify-center">2</span>
                <span class="material-symbols-outlined text-tech-blue-light/60 timeline-icon text-2xl">sync_alt</span>
              </div>
            </div>
            <div class="timeline-content pt-2 pb-8 border-b border-primary/10 last:border-0 w-full">
              <h3 class="text-xl font-bold text-white mb-3 font-headline group-hover:text-tech-blue-light transition-colors">
                双库自动同步
              </h3>
              <p class="text-white/60 font-body leading-relaxed text-[15px]">
                数据自动解析同步至向量数据库（语义检索）与图谱数据库（逻辑推理）
              </p>
            </div>
          </div>

          <!-- Step 3 -->
          <div class="timeline-item flex flex-col md:flex-row gap-6 md:gap-10 group">
            <div class="flex-shrink-0 flex items-start">
              <div class="w-14 h-14 rounded-2xl bg-[#0d3311]/60 border border-tech-blue/20 flex items-center justify-center timeline-icon-container backdrop-blur-sm z-10 mt-1 relative">
                <span class="absolute -top-1.5 -right-1.5 w-5 h-5 bg-tech-blue rounded-full text-[10px] font-bold text-white flex items-center justify-center">3</span>
                <span class="material-symbols-outlined text-tech-blue-light/60 timeline-icon text-2xl">add_photo_alternate</span>
              </div>
            </div>
            <div class="timeline-content pt-2 pb-8 border-b border-primary/10 last:border-0 w-full">
              <h3 class="text-xl font-bold text-white mb-3 font-headline group-hover:text-tech-blue-light transition-colors">
                用户多模态输入
              </h3>
              <p class="text-white/60 font-body leading-relaxed text-[15px]">
                文本提问 / 病害照片上传，田间需求一键提交
              </p>
            </div>
          </div>

          <!-- Step 4 -->
          <div class="timeline-item flex flex-col md:flex-row gap-6 md:gap-10 group">
            <div class="flex-shrink-0 flex items-start">
              <div class="w-14 h-14 rounded-2xl bg-[#0d3311]/60 border border-tech-blue/20 flex items-center justify-center timeline-icon-container backdrop-blur-sm z-10 mt-1 relative">
                <span class="absolute -top-1.5 -right-1.5 w-5 h-5 bg-tech-cyan rounded-full text-[10px] font-bold text-white flex items-center justify-center">4</span>
                <span class="material-symbols-outlined text-tech-blue-light/60 timeline-icon text-2xl">hub</span>
              </div>
            </div>
            <div class="timeline-content pt-2 pb-8 border-b border-primary/10 last:border-0 w-full">
              <h3 class="text-xl font-bold text-white mb-3 font-headline group-hover:text-tech-blue-light transition-colors">
                GraphRAG 双引擎检索
              </h3>
              <p class="text-white/60 font-body leading-relaxed text-[15px]">
                知识库 + 知识图谱双路径融合检索，精准匹配相关内容
              </p>
            </div>
          </div>

          <!-- Step 5 -->
          <div class="timeline-item flex flex-col md:flex-row gap-6 md:gap-10 group">
            <div class="flex-shrink-0 flex items-start">
              <div class="w-14 h-14 rounded-2xl bg-[#0d3311]/60 border border-tech-blue/20 flex items-center justify-center timeline-icon-container backdrop-blur-sm z-10 mt-1 relative">
                <span class="absolute -top-1.5 -right-1.5 w-5 h-5 bg-tech-blue rounded-full text-[10px] font-bold text-white flex items-center justify-center">5</span>
                <span class="material-symbols-outlined text-tech-blue-light/60 timeline-icon text-2xl">neurology</span>
              </div>
            </div>
            <div class="timeline-content pt-2 pb-8 border-b border-primary/10 last:border-0 w-full">
              <h3 class="text-xl font-bold text-white mb-3 font-headline group-hover:text-tech-blue-light transition-colors">
                多模态大模型推理
              </h3>
              <p class="text-white/60 font-body leading-relaxed text-[15px]">
                视觉 + NLP 联合诊断，农业场景微调优化，生成专业合规内容
              </p>
            </div>
          </div>

          <!-- Step 6 -->
          <div class="timeline-item flex flex-col md:flex-row gap-6 md:gap-10 group">
            <div class="flex-shrink-0 flex items-start">
              <div class="w-14 h-14 rounded-2xl bg-[#0d3311]/60 border border-tech-blue/20 flex items-center justify-center timeline-icon-container backdrop-blur-sm z-10 mt-1 relative">
                <span class="absolute -top-1.5 -right-1.5 w-5 h-5 bg-accent-orange rounded-full text-[10px] font-bold text-white flex items-center justify-center">6</span>
                <span class="material-symbols-outlined text-tech-blue-light/60 timeline-icon text-2xl">check_circle</span>
              </div>
            </div>
            <div class="timeline-content pt-2 pb-0 border-b-0 w-full">
              <h3 class="text-xl font-bold text-white mb-3 font-headline group-hover:text-accent-orange transition-colors">
                精准结果输出
              </h3>
              <p class="text-white/60 font-body leading-relaxed text-[15px]">
                可视化诊断结果、分阶段防治方案、决策建议一键获取
              </p>
            </div>
          </div>

        </div>
      </div>
    </div>
    <!-- Bottom fade: #0d1f11 -> tech-darker -->
    <div class="absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-t from-tech-darker/60 to-transparent pointer-events-none z-[2]"></div>
  </section>
</template>
