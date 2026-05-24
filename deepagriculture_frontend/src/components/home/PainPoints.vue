<script setup>
const painPoints = [
  {
    icon: 'visibility_off',
    title: '识别困难',
    desc: '早期症状往往很微妙且容易混淆，导致干预延迟和广泛感染。',
    stat: '60%',
    statLabel: '病害误诊率',
    accent: 'tech-blue',
    accentClass: 'border-tech-blue/40 bg-tech-blue/5 hover:shadow-[0_0_40px_rgba(25,118,210,0.2)]',
    iconBg: 'bg-tech-blue/10 text-tech-blue-light group-hover:shadow-[0_0_20px_rgba(66,165,245,0.5)]',
    statColor: 'text-tech-blue-light',
  },
  {
    icon: 'person_off',
    title: '专家短缺',
    desc: '农村地区农技人员稀缺，造成了及时、本地化建议的瓶颈。',
    stat: '1:10,000',
    statLabel: '农技人员与农户比',
    accent: 'accent-orange',
    accentClass: 'border-accent-orange/30 bg-accent-orange/5 hover:shadow-[0_0_40px_rgba(255,152,0,0.2)]',
    iconBg: 'bg-accent-orange/10 text-accent-orange group-hover:shadow-[0_0_20px_rgba(255,152,0,0.5)]',
    statColor: 'text-accent-orange',
  },
  {
    icon: 'science',
    title: '农药滥用',
    desc: '不准确的诊断导致广谱喷洒，破坏土壤生态并增加运营成本。',
    stat: '35%',
    statLabel: '农药过量使用率',
    accent: 'primary',
    accentClass: 'border-primary/30 bg-primary/5 hover:shadow-[0_0_40px_rgba(46,125,50,0.2)]',
    iconBg: 'bg-primary/10 text-primary group-hover:shadow-[0_0_20px_rgba(46,125,50,0.5)]',
    statColor: 'text-primary-fixed',
  },
  {
    icon: 'update_disabled',
    title: '信息滞后',
    desc: '传统文献是静态的。病原体的突变和适应速度比物理手册的更新速度更快。',
    stat: '6个月+',
    statLabel: '知识更新延迟',
    accent: 'tech-cyan',
    accentClass: 'border-tech-cyan/30 bg-tech-cyan/5 hover:shadow-[0_0_40px_rgba(0,188,212,0.2)]',
    iconBg: 'bg-tech-cyan/10 text-tech-cyan group-hover:shadow-[0_0_20px_rgba(0,188,212,0.5)]',
    statColor: 'text-tech-cyan',
  },
];
</script>

<template>
  <section class="py-28 relative overflow-hidden" style="background: linear-gradient(180deg, #ffffff 0%, #f7faf5 40%, #f0f6ed 100%);">
    <!-- Background atmosphere -->
    <div class="absolute inset-0 pointer-events-none">
      <!-- Micro-dot grid -->
      <div class="absolute inset-0 opacity-[0.07]" style="background-image: radial-gradient(circle, #1B5E20 1.5px, transparent 1.5px); background-size: 28px 28px;"></div>
      <!-- Diagonal tech lines (subtle) -->
      <div class="absolute inset-0 opacity-[0.04]" style="background: repeating-linear-gradient(45deg, transparent, transparent 60px, rgba(25,118,210,0.3) 60px, rgba(25,118,210,0.3) 61px);"></div>
      <!-- Atmospheric blobs -->
      <div class="absolute top-[-15%] right-[-8%] w-[550px] h-[550px] bg-tech-blue/8 rounded-full blur-[130px]"></div>
      <div class="absolute bottom-[-10%] left-[-8%] w-[480px] h-[480px] bg-primary/8 rounded-full blur-[120px]"></div>
      <div class="absolute top-[40%] left-[60%] w-[300px] h-[300px] bg-tech-cyan/6 rounded-full blur-[80px]"></div>
    </div>

    <!-- Top accent line -->
    <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[70%] h-px bg-gradient-to-r from-transparent via-tech-blue/40 to-transparent pointer-events-none"></div>

    <div class="max-w-screen-xl mx-auto px-8 relative z-10">
      <!-- Section Header -->
      <div class="text-center mb-20 reveal-down">
        <div class="inline-flex items-center gap-2 bg-tech-blue/5 border border-tech-blue/15 rounded-full px-4 py-1.5 mb-6">
          <span class="w-2 h-2 rounded-full bg-tech-blue-light animate-pulse shadow-[0_0_6px_rgba(66,165,245,0.8)]"></span>
          <span class="font-headline text-xs tracking-widest uppercase text-tech-blue">The Challenge</span>
        </div>
        <h2 class="font-headline text-4xl md:text-5xl font-bold text-on-surface mb-4">
          农业面临的<span class="text-tech-blue">核心挑战</span>
        </h2>
        <p class="text-on-surface/50 font-body text-lg max-w-xl mx-auto leading-relaxed">
          目前作物管理中系统性的效率低下导致了大规模的产量损失和生态压力。
        </p>
      </div>

      <!-- 2x2 Pain Point Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 lg:gap-8">
        <div
          v-for="(point, idx) in painPoints"
          :key="point.title"
          :class="[
            'group relative rounded-2xl p-8 lg:p-10 border transition-all duration-500 ease-[cubic-bezier(0.25,1,0.5,1)] hover:-translate-y-3 reveal-up',
            'bg-white/60 backdrop-blur-sm',
            point.accentClass,
          ]"
          :style="{ transitionDelay: `${idx * 100}ms` }"
        >
          <!-- Accent bar at top -->
          <div
            :class="[
              'absolute top-0 left-6 right-6 h-[3px] rounded-full transition-all duration-500',
              idx === 0 ? 'bg-gradient-to-r from-tech-blue/60 to-tech-cyan/40 group-hover:from-tech-blue-light group-hover:to-tech-cyan' : '',
              idx === 1 ? 'bg-gradient-to-r from-accent-orange/60 to-accent-orange/20 group-hover:from-accent-orange group-hover:to-accent-orange/50' : '',
              idx === 2 ? 'bg-gradient-to-r from-primary/60 to-primary/20 group-hover:from-primary group-hover:to-primary/50' : '',
              idx === 3 ? 'bg-gradient-to-r from-tech-cyan/60 to-tech-blue/30 group-hover:from-tech-cyan group-hover:to-tech-blue-light' : '',
            ]"
          ></div>

          <!-- Content -->
          <div class="flex items-start gap-5 mt-2">
            <!-- Icon -->
            <div
              :class="[
                'w-14 h-14 rounded-2xl flex items-center justify-center flex-shrink-0 transition-all duration-400 group-hover:scale-110 group-hover:rotate-3',
                point.iconBg,
              ]"
            >
              <span class="material-symbols-outlined text-2xl">{{ point.icon }}</span>
            </div>

            <!-- Text -->
            <div class="flex-1 min-w-0">
              <h3 class="font-headline text-xl font-bold text-on-surface mb-2 group-hover:translate-x-1 transition-transform duration-400">
                {{ point.title }}
              </h3>
              <p class="text-on-surface/55 leading-relaxed text-sm">
                {{ point.desc }}
              </p>
            </div>

            <!-- Stat -->
            <div class="text-right flex-shrink-0">
              <div :class="['font-headline text-3xl font-bold tabular-nums tracking-tight', point.statColor]">
                {{ point.stat }}
              </div>
              <div class="text-on-surface/35 text-xs font-headline tracking-wide mt-0.5">
                {{ point.statLabel }}
              </div>
            </div>
          </div>

          <!-- Bottom indicator dots -->
          <div class="flex gap-1.5 mt-6">
            <span v-for="dot in 3" :key="dot"
              :class="[
                'w-1.5 h-1.5 rounded-full transition-all duration-500',
                dot === 1 ? point.statColor.replace('text-', 'bg-') + ' shadow-[0_0_6px_currentColor]' : 'bg-on-surface/10 group-hover:bg-on-surface/20',
              ]"
            ></span>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom fade to DesignPhilosophy (surface) -->
    <div class="absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-t from-surface/50 to-transparent pointer-events-none z-[2]"></div>
  </section>
</template>
