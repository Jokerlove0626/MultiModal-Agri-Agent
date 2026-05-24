<script setup>
</script>

<template>
  <section class="min-h-[80vh] flex items-center justify-center relative overflow-hidden bg-gradient-to-br from-tech-dark via-tech-blue/30 to-tech-dark py-20">
    <!-- Background layers -->
    <div class="absolute inset-0 bg-tech-grid bg-grid-size opacity-20 pointer-events-none"></div>
    <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-tech-blue/10 rounded-full blur-3xl pointer-events-none"></div>
    <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent-orange/8 rounded-full blur-3xl pointer-events-none"></div>

    <div class="relative z-10 text-center px-8 max-w-4xl mx-auto flex flex-col items-center justify-center h-full space-y-10 reveal-up">
      <h2 class="font-headline text-4xl md:text-6xl font-bold text-white leading-tight drop-shadow-lg">
        准备好体验你的随身 <span class="bg-gradient-to-r from-tech-blue-light to-tech-cyan bg-clip-text text-transparent">AI 植保专家</span> 了吗？
      </h2>
      <p class="font-body text-xl text-white/80 max-w-2xl">
        无需注册，无需下载，打开就能用，田间难题一键解决
      </p>

      <!-- CTA Button with ripple -->
      <router-link
        to="/chat"
        class="cta-ripple inline-flex items-center gap-2 bg-accent-orange text-white px-10 py-5 rounded-full font-headline font-bold text-lg hover:shadow-glow-orange-lg hover:scale-105 transition-all duration-400 ease-[cubic-bezier(0.25,1,0.5,1)] group"
      >
        立即免费体验 AI 问诊
        <span class="material-symbols-outlined ml-2 align-middle group-hover:translate-x-1 transition-transform">arrow_forward</span>
      </router-link>

      <!-- Bottom links -->
      <div class="pt-16 flex flex-col md:flex-row items-center justify-center gap-12 text-white/70">
        <div class="flex items-center gap-4">
          <div class="w-16 h-16 bg-white/10 backdrop-blur border border-white/20 rounded-lg flex items-center justify-center p-2">
            <span class="material-symbols-outlined text-3xl text-white/80">qr_code_2</span>
          </div>
          <div class="text-left">
            <div class="text-sm font-bold text-white">扫码即可手机端使用</div>
            <div class="text-xs">随时随地，拍照问诊</div>
          </div>
        </div>
        <div class="w-px h-12 bg-white/20 hidden md:block"></div>
        <div class="flex flex-col gap-2 text-sm text-left">
          <a class="hover:text-tech-blue-light transition-colors flex items-center gap-2" href="#">
            <span class="material-symbols-outlined text-base">code</span>
            开源仓库 GitHub
          </a>
          <a class="hover:text-tech-blue-light transition-colors flex items-center gap-2" href="#">
            <span class="material-symbols-outlined text-base">mail</span>
            contact@deepagri.com
          </a>
        </div>
      </div>
    </div>
    <!-- Bottom fade: CTA blue -> tech-darker -->
    <div class="absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-t from-tech-darker/70 to-transparent pointer-events-none z-[2]"></div>
  </section>
</template>
