<script setup>
</script>

<template>
  <section class="py-24 bg-surface-container-lowest relative overflow-hidden">
    <!-- Subtle top tech-dot accent -->
    <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[60%] h-px bg-gradient-to-r from-transparent via-tech-blue/30 to-transparent pointer-events-none"></div>

    <div class="max-w-screen-xl mx-auto px-8 relative z-10">
      <!-- Section Header -->
      <div class="mb-16 max-w-2xl reveal-down">
        <h2 class="font-headline text-3xl md:text-4xl font-bold text-on-surface mb-4">
          农业面临的<span class="text-tech-blue">挑战</span>
        </h2>
        <p class="text-on-surface/60 font-body text-lg">
          目前作物管理中系统性的效率低下导致了大规模的产量损失和生态压力。
        </p>
      </div>

      <!-- 2x2 Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Card 1 -->
        <div class="glass-card p-10 rounded-2xl transition-all duration-400 ease-[cubic-bezier(0.25,1,0.5,1)] hover:-translate-y-2 hover:shadow-[0_12px_40px_rgba(25,118,210,0.12)] reveal-up group border border-primary/10 hover:border-tech-blue/30">
          <div class="w-12 h-12 bg-primary/10 text-primary group-hover:bg-tech-blue/10 group-hover:text-tech-blue rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-all duration-300">
            <span class="material-symbols-outlined">visibility_off</span>
          </div>
          <h3 class="font-body text-xl font-semibold mb-3 text-on-surface group-hover:text-tech-blue transition-colors duration-300">
            识别困难
          </h3>
          <p class="text-on-surface/70 leading-relaxed">
            早期症状往往很微妙且容易混淆，导致干预延迟和广泛感染。
          </p>
        </div>

        <!-- Card 2 -->
        <div class="glass-card p-10 rounded-2xl transition-all duration-400 ease-[cubic-bezier(0.25,1,0.5,1)] hover:-translate-y-2 hover:shadow-[0_12px_40px_rgba(25,118,210,0.12)] reveal-up delay-100 group border border-primary/10 hover:border-tech-blue/30">
          <div class="w-12 h-12 bg-primary/10 text-primary group-hover:bg-tech-blue/10 group-hover:text-tech-blue rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-all duration-300">
            <span class="material-symbols-outlined">person_off</span>
          </div>
          <h3 class="font-body text-xl font-semibold mb-3 text-on-surface group-hover:text-tech-blue transition-colors duration-300">
            专家短缺
          </h3>
          <p class="text-on-surface/70 leading-relaxed">
            农村地区农技人员稀缺，造成了及时、本地化建议的瓶颈。
          </p>
        </div>

        <!-- Card 3 -->
        <div class="glass-card p-10 rounded-2xl transition-all duration-400 ease-[cubic-bezier(0.25,1,0.5,1)] hover:-translate-y-2 hover:shadow-[0_12px_40px_rgba(25,118,210,0.12)] reveal-up group border border-primary/10 hover:border-tech-blue/30">
          <div class="w-12 h-12 bg-primary/10 text-primary group-hover:bg-tech-blue/10 group-hover:text-tech-blue rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-all duration-300">
            <span class="material-symbols-outlined">science</span>
          </div>
          <h3 class="font-body text-xl font-semibold mb-3 text-on-surface group-hover:text-tech-blue transition-colors duration-300">
            农药滥用
          </h3>
          <p class="text-on-surface/70 leading-relaxed">
            不准确的诊断导致广谱喷洒，破坏土壤生态并增加运营成本。
          </p>
        </div>

        <!-- Card 4 -->
        <div class="glass-card p-10 rounded-2xl transition-all duration-400 ease-[cubic-bezier(0.25,1,0.5,1)] hover:-translate-y-2 hover:shadow-[0_12px_40px_rgba(25,118,210,0.12)] reveal-up delay-100 group border border-primary/10 hover:border-tech-blue/30">
          <div class="w-12 h-12 bg-primary/10 text-primary group-hover:bg-tech-blue/10 group-hover:text-tech-blue rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-all duration-300">
            <span class="material-symbols-outlined">update_disabled</span>
          </div>
          <h3 class="font-body text-xl font-semibold mb-3 text-on-surface group-hover:text-tech-blue transition-colors duration-300">
            信息滞后
          </h3>
          <p class="text-on-surface/70 leading-relaxed">
            传统文献是静态的。病原体的突变和适应速度比物理手册的更新速度更快。
          </p>
        </div>
      </div>
    </div>
  </section>
</template>
