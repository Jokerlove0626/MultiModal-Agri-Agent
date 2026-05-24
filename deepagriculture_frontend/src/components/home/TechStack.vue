<script setup>
const techItems = [
  {
    icon: 'memory',
    title: 'AI 核心层',
    desc: 'GraphRAG 双引擎 (知识图谱 + RAG)、多模态视觉大模型、Python',
  },
  {
    icon: 'dns',
    title: '后端框架层',
    desc: 'FastAPI、Uvicorn ASGI 服务器、Docker 容器化部署',
  },
  {
    icon: 'speed',
    title: '架构优化',
    desc: '全异步 RESTful API、全局单例模式挂载 AI 引擎、CORS 跨域支持、全网段访问',
  },
  {
    icon: 'web',
    title: '前端技术层',
    desc: 'Vue 3、Vite、ECharts 可视化、Tailwind CSS、响应式布局',
  },
  {
    icon: 'database',
    title: '数据存储层',
    desc: '向量数据库、Neo4j 图数据库、关系型数据库',
  },
  {
    icon: 'security',
    title: '安全管控',
    desc: '管理员 Token 鉴权、403 防护、标准化 FastAPI 异常状态码响应',
  },
];
</script>

<template>
  <section class="py-24 bg-tech-darker relative overflow-hidden border-t border-primary/10">
    <!-- Background -->
    <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-tech-blue/5 via-transparent to-transparent pointer-events-none"></div>

    <div class="max-w-[1200px] mx-auto px-8 relative z-10">
      <!-- Header -->
      <div class="text-center mb-16 reveal-down">
        <h2 class="font-headline text-3xl md:text-4xl font-bold text-white mb-4 drop-shadow-[0_0_10px_rgba(25,118,210,0.3)]">
          全栈技术<span class="text-tech-blue-light">体系</span>，筑牢平台核心能力
        </h2>
        <p class="text-white/60 font-body text-lg max-w-2xl mx-auto">
          采用现代化 AI 微服务架构，以高性能和高可扩展性为核心驱动
        </p>
      </div>

      <!-- Cards Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="(item, idx) in techItems"
          :key="item.title"
          :class="[
            'glass-card bg-[#112614]/80 rounded-2xl p-6 border border-primary/20 hover:-translate-y-1 hover:border-tech-blue/40 hover:shadow-[0_0_30px_rgba(25,118,210,0.15)] transition-all duration-300 reveal-up group',
            `delay-${idx * 100}`
          ]"
        >
          <div class="w-10 h-10 rounded-lg bg-tech-blue/20 flex items-center justify-center mb-4 text-tech-blue-light group-hover:scale-110 transition-transform">
            <span class="material-symbols-outlined">{{ item.icon }}</span>
          </div>
          <h3 class="text-lg font-bold text-white mb-3 font-headline group-hover:text-tech-blue-light transition-colors">
            {{ item.title }}
          </h3>
          <p class="text-white/60 text-sm leading-relaxed">{{ item.desc }}</p>
        </div>
      </div>
    </div>
  </section>
</template>
