<script setup>
const faqs = [
  {
    q: '平台使用需要收费吗?',
    a: '平台核心功能完全免费，旨在为广大农业工作者提供普惠的AI技术支持。未来部分高级专家定制服务可能会采取灵活的订阅模式，但基础识别与知识库将始终开放。',
  },
  {
    q: '平台支持哪些作物的病虫害识别?',
    a: '覆盖120+种常见作物，包括水稻、小麦、玉米等大宗粮食作物，以及苹果、柑橘、番茄等主要经济作物和蔬菜。系统模型正在持续迭代扩展中。',
  },
  {
    q: '上传的图片有什么要求?',
    a: '建议拍摄特写，确保病变部位清晰可见且光照充足。支持JPG/PNG格式，单张图片大小不超过10MB。避免过度模糊或逆光拍摄。',
  },
  {
    q: '手机上可以使用这个平台吗?',
    a: '做了全移动端适配。您可以通过手机浏览器直接访问，或者关注我们的微信小程序，随时随地在田间地头进行拍照识别。',
  },
  {
    q: 'AI给出的防治方案靠谱吗?',
    a: '基于GraphRAG双引擎检索架构，所有防治方案均溯源至权威农技文献和专家知识库。生成内容经过严格的专家审核校验机制过滤，确保科学性和实用性。',
  },
  {
    q: '什么是GraphRAG?',
    a: '知识图谱+检索增强生成架构。它结合了知识图谱的结构化逻辑和大型语言模型的生成能力，有效降低了AI的"幻觉"问题，提供逻辑性更强、更精准的解答。',
  },
];
</script>

<template>
  <section class="w-full bg-tech-darker py-24 relative overflow-hidden border-t border-primary/10">
    <!-- Background -->
    <div class="absolute inset-0 bg-tech-grid bg-grid-size opacity-10 pointer-events-none"></div>

    <div class="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 w-full relative z-10 reveal-up">
      <!-- Header -->
      <div class="mb-12 text-center md:text-left">
        <h2 class="text-[1.75rem] font-bold font-headline text-white mb-4 drop-shadow-[0_0_10px_rgba(25,118,210,0.3)]">
          常见<span class="text-tech-blue-light">问题</span>解答
        </h2>
        <p class="text-[1rem] text-white/60 font-body">
          你关心的问题，这里都有答案
        </p>
      </div>

      <!-- FAQ Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4 items-start">
        <div
          v-for="faq in faqs"
          :key="faq.q"
          class="glass-card bg-[#112614]/60 rounded-xl group border border-primary/10 hover:border-tech-blue/30 hover:shadow-[0_0_20px_rgba(25,118,210,0.12)] transition-all duration-300"
        >
          <details class="w-full cursor-pointer faq-details">
            <summary class="flex justify-between items-center text-[1rem] font-semibold text-white list-none py-6 px-6">
              <span class="flex items-center gap-3">
                <span class="w-1 h-5 rounded-full bg-tech-blue/0 group-hover:bg-tech-blue/60 transition-colors duration-300 detail-indicator"></span>
                {{ faq.q }}
              </span>
              <span class="material-symbols-outlined text-tech-blue-light transition-transform duration-300 detail-arrow">expand_more</span>
            </summary>
            <div class="px-6 pb-6 -mt-2">
              <p class="text-[0.875rem] text-white/70 leading-relaxed pl-4 border-l border-tech-blue/20">
                {{ faq.a }}
              </p>
            </div>
          </details>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.faq-details[open] .detail-arrow {
  transform: rotate(180deg);
}
.faq-details[open] .detail-indicator {
  background: rgba(25, 118, 210, 0.6);
}
.faq-details summary::-webkit-details-marker {
  display: none;
}
</style>
