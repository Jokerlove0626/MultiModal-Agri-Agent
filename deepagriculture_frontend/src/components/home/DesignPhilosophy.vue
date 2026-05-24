<script setup>
</script>

<template>
  <section class="py-16 relative bg-surface overflow-hidden">
    <!-- Subtle ambient glow -->
    <div class="absolute top-1/3 right-0 w-[500px] h-[500px] bg-tech-blue/3 rounded-full blur-3xl pointer-events-none"></div>

    <div class="max-w-screen-xl mx-auto px-8 grid grid-cols-1 lg:grid-cols-12 gap-16 relative z-10">
      <!-- Sticky Left Column -->
      <div class="col-span-12 lg:col-span-4 relative">
        <div class="sticky top-24 space-y-8">
          <div>
            <h2 class="font-headline text-4xl md:text-5xl font-bold text-primary mb-4">
              设计<span class="text-tech-blue">理念</span>
            </h2>
            <p class="text-xl text-on-surface/80 font-medium font-headline">
              洞悉作物脉搏，精准应对病虫挑战
            </p>
          </div>
          <div class="w-full aspect-[4/5] rounded-[2rem] overflow-hidden bg-primary/10 shadow-glow-lg border border-primary/20 hover:border-tech-blue/40 transition-colors duration-500">
            <img
              alt="healthy green crops in a modern greenhouse"
              class="w-full h-full object-cover opacity-90 transition-all duration-700 hover:scale-105"
              src="/img/1.png"
            />
          </div>
        </div>
      </div>

      <!-- Right Narrative Column -->
      <div class="col-span-12 lg:col-span-7 lg:col-start-6 py-8 flex flex-col justify-center min-h-[60vh]">
        <div class="space-y-12">
          <!-- Narrative Block 1 -->
          <div class="narrative-item w-full">
            <h3 class="text-on-surface font-headline font-bold text-3xl md:text-4xl leading-[1.3] tracking-tight mb-8">
              <span class="stagger-line"><span class="delay-100">
                我们以<span class="text-tech-blue mx-2 px-2 bg-tech-blue/10 rounded-lg inline-block transform -rotate-1">「科技兴农，农技普惠」</span>为初心，
              </span></span>
              <span class="stagger-line"><span class="delay-200">
                聚焦基层农业从业者的真实植保痛点，
              </span></span>
              <span class="stagger-line"><span class="delay-300">
                打破农技资源的地域壁垒，
              </span></span>
              <span class="stagger-line"><span class="delay-400">
                将 <span class="text-tech-blue font-bold">GraphRAG</span> 知识图谱、<span class="text-tech-blue font-bold">多模态大模型</span>
              </span></span>
              <span class="stagger-line"><span class="delay-500">
                与农业植保专业知识深度融合，打造出
              </span></span>
              <span class="stagger-line"><span class="delay-[600ms] text-tech-blue">
                低门槛、高精准、全场景的AI诊断平台。
              </span></span>
            </h3>
          </div>

          <!-- Narrative Block 2 -->
          <div class="narrative-item w-full border-l-4 border-tech-blue/40 pl-6">
            <p class="text-on-surface/80 font-body text-xl md:text-2xl font-medium leading-relaxed">
              <span class="stagger-line"><span class="delay-100">
                我们不止于做一个 AI 工具，更致力于成为守护农田的<span class="text-tech-blue font-semibold">智能伙伴</span>，
              </span></span>
              <span class="stagger-line"><span class="delay-200">
                让偏远地区的农户也能免费获得专业级植保指导，助力科学防治、降本增效，
              </span></span>
              <span class="stagger-line"><span class="delay-300">
                以数字技术赋能<span class="text-accent-orange font-semibold">乡村振兴</span>，守护国家粮食安全。
              </span></span>
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
