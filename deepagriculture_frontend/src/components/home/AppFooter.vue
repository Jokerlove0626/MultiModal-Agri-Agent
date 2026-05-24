<script setup>
const footerColumns = [
  {
    title: '平台介绍',
    links: ['关于智农大夫', '实验室团队', '最新动态'],
  },
  {
    title: '核心功能',
    links: ['图像诊断', '知识问答', '农业知识图谱'],
  },
  {
    title: '帮助中心',
    links: ['使用指南', '常见问题', '意见反馈'],
  },
  {
    title: '合规相关',
    links: ['服务协议', '隐私政策', '免责声明'],
  },
];
</script>

<template>
  <footer class="bg-tech-darker text-surface/70 py-16 font-body text-sm border-t border-white/10 relative overflow-hidden">
    <!-- Subtle top gradient border -->
    <div class="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-tech-blue/40 to-transparent"></div>

    <div class="max-w-screen-2xl mx-auto px-8 space-y-12 relative z-10">
      <!-- Footer Links -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
        <div v-for="col in footerColumns" :key="col.title" class="space-y-4">
          <h4 class="font-headline font-semibold text-white text-base mb-6">
            {{ col.title }}
          </h4>
          <ul class="space-y-3">
            <li v-for="link in col.links" :key="link">
              <a class="hover:text-tech-blue-light transition-colors duration-200 relative after:absolute after:bottom-0 after:left-0 after:w-0 after:h-px after:bg-tech-blue-light after:transition-all hover:after:w-full" href="#">
                {{ link }}
              </a>
            </li>
          </ul>
        </div>
      </div>

      <!-- Bottom Bar -->
      <div class="border-t border-white/10 pt-8 flex flex-col gap-4 text-xs">
        <div class="flex flex-col md:flex-row justify-between gap-4">
          <p class="text-white/50">
            版权所有 &copy; 2026 DeepAgriculture 智农大夫研发团队 |
            主办单位：浙江农林大学 | 指导单位：计算机科学与技术学院
          </p>
          <div class="flex gap-4 text-white/40">
            <span>备案号：浙ICP备XXXXXXXX号-1</span>
          </div>
        </div>

        <!-- Disclaimer -->
        <div class="bg-black/30 p-4 rounded-lg border border-white/5 text-surface/60">
          <span class="font-semibold text-tech-blue-light">免责声明：</span>
          平台内容仅供参考，不构成农事操作唯一指导建议，具体防治请结合当地实际情况与农技人员专业指导。
        </div>
      </div>
    </div>
  </footer>
</template>
