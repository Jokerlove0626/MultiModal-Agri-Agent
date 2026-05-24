<script setup>
import AnimatedCounter from './AnimatedCounter.vue';

const counters = [
  { icon: 'eco', target: 120, suffix: '+', label: '覆盖作物 (种)' },
  { icon: 'bug_report', target: 2000, suffix: '+', label: '覆盖病虫害 (种)' },
  { icon: 'menu_book', target: 18000, suffix: '+', label: '专业知识库 (篇)' },
  { icon: 'image', target: 1200, suffix: '万+', label: '标注训练图片 (张)' },
];
</script>

<template>
  <section class="w-full bg-tech-darker py-24 relative overflow-hidden border-t border-primary/10">
    <!-- Background -->
    <div class="absolute inset-0 bg-tech-grid bg-grid-size opacity-10 pointer-events-none"></div>
    <div class="absolute bottom-0 left-1/4 w-[500px] h-[300px] bg-tech-blue/4 rounded-full blur-3xl pointer-events-none"></div>

    <div class="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 w-full relative z-10">
      <!-- Header -->
      <div class="text-center mb-16 reveal-down">
        <h2 class="text-[1.75rem] font-bold font-headline text-white drop-shadow-[0_0_10px_rgba(25,118,210,0.3)] mb-4">
          权威<span class="text-tech-blue-light">数据</span>支撑，保障内容专业可靠
        </h2>
        <p class="text-[1rem] text-white/60 font-body max-w-2xl mx-auto">
          整合多源权威植保数据，构建动态更新的农业知识库
        </p>
      </div>

      <!-- Counter Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        <div
          v-for="(item, idx) in counters"
          :key="item.label"
          :class="[
            'glass-card bg-[#112614]/80 border border-primary/20 hover:border-tech-blue/40 rounded-2xl p-8 flex flex-col items-center justify-center hover:-translate-y-1 hover:shadow-[0_0_30px_rgba(25,118,210,0.15)] transition-all duration-400 ease-[cubic-bezier(0.25,1,0.5,1)] reveal-up group',
            `delay-${idx * 100}`
          ]"
        >
          <span
            class="material-symbols-outlined text-tech-blue-light text-4xl mb-4 group-hover:scale-110 transition-transform"
            style="font-variation-settings: 'FILL' 1;"
          >{{ item.icon }}</span>
          <div class="text-[2.5rem] font-bold font-headline bg-gradient-to-b from-white to-tech-blue-light/80 bg-clip-text text-transparent mb-2">
            <AnimatedCounter :target="item.target" :suffix="item.suffix" />
          </div>
          <div class="text-[0.875rem] text-white/60 font-medium">{{ item.label }}</div>
        </div>
      </div>

      <!-- Data Source -->
      <div class="text-center text-[0.75rem] text-white/40 font-label mt-8 max-w-4xl mx-auto reveal-up delay-400">
        数据来源为中国农业科学院植保所公开数据集、国家农业农村部全国病虫害监测数据、《中国主要农业有害生物》权威工具书、核心农业期刊文献、植保专家知识库
      </div>
    </div>
  </section>
</template>
