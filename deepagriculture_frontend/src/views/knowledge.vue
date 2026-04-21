<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue';

const form = ref({
  disease_name: '',
  symptom: '',
  treatment: '',
  admin_token: ''
});

const isSubmitting = ref(false);
const toastState = ref({
  show: false,
  message: '',
  type: 'success'
});

const showToast = (msg, type = 'success') => {
  toastState.value = { show: true, message: msg, type };
  setTimeout(() => {
    toastState.value.show = false;
  }, 3500);
};

const submitKnowledge = async () => {
  if (!form.value.disease_name || !form.value.symptom || !form.value.treatment || !form.value.admin_token) {
    showToast('请完整填写所有字段', 'error');
    return;
  }

  isSubmitting.value = true;
  try {
    const res = await fetch('http://127.0.0.1:8000/api/knowledge/add', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(form.value)
    });

    const data = await res.json();

    if (res.ok) {
      showToast('知识库数据双写同步成功！', 'success');
      form.value.disease_name = '';
      form.value.symptom = '';
      form.value.treatment = '';
    } else {
      showToast(data.detail || '接口验证失败', 'error');
    }
  } catch (err) {
    showToast('网络错误，请检查后端服务是否启动', 'error');
  } finally {
    isSubmitting.value = false;
  }
};

onMounted(() => {
  document.body.classList.add('knowledge-theme');
  nextTick(() => {
    const revealElements = document.querySelectorAll('.reveal-left, .reveal-right');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('active');
        }
      });
    }, { threshold: 0.1 });
    revealElements.forEach((el) => observer.observe(el));
  });
});

onUnmounted(() => {
  document.body.classList.remove('knowledge-theme');
});
</script>

<template>
  <div
    class="min-h-screen bg-tech-darker text-surface relative overflow-x-hidden p-6 md:p-12 font-body flex items-center justify-center pt-24 md:pt-32 selection:bg-primary/30">
    <!-- Background Effects -->
    <div class="absolute inset-0 bg-tech-grid bg-grid-size opacity-20 pointer-events-none z-0"></div>
    <div
      class="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-primary/20 rounded-full blur-[120px] pointer-events-none">
    </div>
    <div
      class="absolute bottom-[-10%] right-[-10%] w-[600px] h-[600px] bg-[#00f2fe]/10 rounded-full blur-[150px] pointer-events-none">
    </div>

    <div class="relative z-10 w-full max-w-6xl grid grid-cols-1 lg:grid-cols-12 gap-12 items-start">

      <!-- Left Panel: Instruction & Visualization -->
      <div class="col-span-1 lg:col-span-5 space-y-8 reveal-left">
        <div>
          <div
            class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/30 text-primary text-xs font-mono mb-6 uppercase tracking-wider">
            <span class="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
            System Admin Panel
          </div>
          <h1 class="text-4xl md:text-5xl font-headline font-bold text-white mb-4 leading-tight">
            动态知识<span class="text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#00f2fe]">入库引擎</span>
          </h1>
          <p class="text-white/60 leading-relaxed text-sm md:text-base">
            管理员手动录入新病害知识，系统底层基座将自动执行数据双写：<br />
            同时同步至 <strong>Chroma 向量数据库</strong>（用于模糊语义检索）与 <strong>Neo4j 知识图谱</strong>（用于高精度关联推理）。
          </p>
        </div>

        <!-- Abstract Tech Visual -->
        <div class="glass-card border border-white/10 rounded-2xl p-6 relative overflow-hidden backdrop-blur-md">
          <div class="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent"></div>
          <h3 class="text-sm font-headline text-white/80 mb-6 flex justify-between items-center relative z-10">
            <span>Data Sync Pipeline</span>
            <span class="text-xs font-mono text-primary bg-primary/10 px-2 py-0.5 rounded">Active</span>
          </h3>

          <div class="flex flex-col gap-6 relative z-10">
            <div
              class="flex items-center justify-between p-4 rounded-xl bg-black/40 border border-white/5 group hover:border-primary/30 transition-colors">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-lg bg-indigo-500/20 flex items-center justify-center text-indigo-400">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
                  </svg>
                </div>
                <div>
                  <div class="text-sm font-medium text-white/90">ChromaDB</div>
                  <div class="text-xs text-white/50">Vector Embeddings</div>
                </div>
              </div>
              <div class="text-xs font-mono text-indigo-400">Wait...</div>
            </div>

            <div
              class="flex items-center justify-between p-4 rounded-xl bg-black/40 border border-white/5 group hover:border-primary/30 transition-colors">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-lg bg-primary/20 flex items-center justify-center text-primary">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                  </svg>
                </div>
                <div>
                  <div class="text-sm font-medium text-white/90">Neo4j Graph</div>
                  <div class="text-xs text-white/50">Entities & Relations</div>
                </div>
              </div>
              <div class="text-xs font-mono text-primary">Wait...</div>
            </div>

            <!-- Connecting Line -->
            <div
              class="absolute left-9 top-[3.5rem] bottom-[3.5rem] w-[2px] bg-gradient-to-b from-indigo-500/50 to-primary/50 flex flex-col justify-center -z-10">
              <div class="w-2 h-2 rounded-full bg-white/80 animate-ping -translate-x-[3px]"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Panel: Data Entry Form -->
      <div class="col-span-1 lg:col-span-7 reveal-right delay-100">
        <form @submit.prevent="submitKnowledge"
          class="glass-card bg-[#0a140d]/80 border border-primary/20 rounded-3xl p-6 md:p-10 shadow-[0_0_40px_rgba(46,125,50,0.1)] backdrop-blur-xl relative">

          <!-- Decorative edges -->
          <div class="absolute top-0 left-10 w-20 h-[1px] bg-primary/60 shadow-[0_0_10px_#2e7d32]"></div>
          <div class="absolute bottom-0 right-10 w-20 h-[1px] bg-primary/60 shadow-[0_0_10px_#2e7d32]"></div>

          <h2
            class="text-xl md:text-2xl font-headline text-white mb-8 border-b border-white/10 pb-4 flex items-center gap-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-primary" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            知识节点构建
          </h2>

          <div class="space-y-6">
            <!-- Disease Name -->
            <div class="space-y-2 group">
              <label
                class="text-xs font-mono text-white/60 group-focus-within:text-primary transition-colors tracking-widest uppercase block">
                [Node] Disease Name
              </label>
              <input v-model="form.disease_name"
                class="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3.5 text-white placeholder-white/30 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/50 transition-all font-body"
                placeholder="例如: 草莓炭疽病" required />
            </div>

            <!-- Symptom & Treatment grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- Symptom -->
              <div class="space-y-2 group">
                <label
                  class="text-xs font-mono text-white/60 group-focus-within:text-primary transition-colors tracking-widest uppercase block">
                  [Property] Symptom
                </label>
                <textarea v-model="form.symptom"
                  class="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3.5 text-white placeholder-white/30 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/50 transition-all font-body resize-none h-32"
                  placeholder="详细描述病害的临床表现、发病部位等..." required></textarea>
              </div>

              <!-- Treatment -->
              <div class="space-y-2 group">
                <label
                  class="text-xs font-mono text-white/60 group-focus-within:text-primary transition-colors tracking-widest uppercase block">
                  [Property] Treatment
                </label>
                <textarea v-model="form.treatment"
                  class="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3.5 text-white placeholder-white/30 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/50 transition-all font-body resize-none h-32"
                  placeholder="农业防治、化学防治的具体药剂与方法..." required></textarea>
              </div>
            </div>

            <!-- Admin Token -->
            <div class="space-y-2 group">
              <label
                class="text-xs font-mono text-white/60 group-focus-within:text-primary transition-colors tracking-widest uppercase flex items-center justify-between">
                <span>[Auth] Admin Token</span>
                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-white/40" fill="none" viewBox="0 0 24 24"
                  stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </label>
              <input v-model="form.admin_token" type="password"
                class="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3.5 text-white placeholder-white/30 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary/50 transition-all font-body font-mono text-sm"
                placeholder="••••••••••••" required />
            </div>

            <!-- Submit Button -->
            <div class="pt-4">
              <button type="submit" :disabled="isSubmitting"
                class="w-full bg-primary hover:bg-primary/90 text-white font-headline font-medium py-4 rounded-xl transition-all shadow-[0_0_20px_rgba(46,125,50,0.3)] hover:shadow-[0_0_30px_rgba(46,125,50,0.5)] flex items-center justify-center gap-3 disabled:opacity-70 disabled:cursor-not-allowed group overflow-hidden relative">
                <div class="absolute inset-0 transition-opacity duration-300"></div>
                <span class="relative z-10 flex items-center gap-2">
                  <svg v-if="isSubmitting" class="animate-spin -ml-1 mr-2 h-5 w-5 text-white"
                    xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                    </path>
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg"
                    class="w-5 h-5 group-hover:scale-110 transition-transform" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  {{ isSubmitting ? '同步注入引擎中...' : '提交图谱与向量库' }}
                </span>
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <!-- Toast Notification -->
    <transition name="toast">
      <div v-if="toastState.show"
        class="fixed bottom-10 z-50 px-6 py-3 rounded-full flex items-center gap-3 shadow-xl border backdrop-blur-md font-body text-sm font-medium"
        :class="toastState.type === 'success' ? 'bg-primary/20 border-primary/40 text-primary-container' : 'bg-red-500/20 border-red-500/40 text-red-200'">
        <svg v-if="toastState.type === 'success'" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none"
          viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24"
          stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        {{ toastState.message }}
      </div>
    </transition>
  </div>
</template>

<style scoped>
.glass-card {
  background: rgba(13, 31, 17, 0.4);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
}

.reveal-left {
  opacity: 0;
  transform: translateX(-40px);
  transition: all 1s cubic-bezier(0.16, 1, 0.3, 1);
}

.reveal-right {
  opacity: 0;
  transform: translateX(40px);
  transition: all 1s cubic-bezier(0.16, 1, 0.3, 1);
}

.reveal-left.active,
.reveal-right.active {
  opacity: 1;
  transform: translateX(0);
}

.delay-100 {
  transition-delay: 100ms;
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.toast-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.9);
}

.toast-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.9);
}
</style>

<style>
/* 知识库专属导航栏深色主题覆盖 */
body.knowledge-theme #main-nav {
  background-color: rgba(10, 20, 13, 0.8) !important;
  border-bottom: 1px solid rgba(46, 125, 50, 0.2) !important;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5) !important;
}

body.knowledge-theme #main-nav.glass-card {
  background-color: rgba(10, 20, 13, 0.9) !important;
  backdrop-filter: blur(20px) !important;
}

body.knowledge-theme #main-nav .text-primary {
  color: #81c784 !important;
  /* 调整为明亮适合深色背景的绿 */
}

body.knowledge-theme #main-nav .text-on-surface\/60 {
  color: rgba(255, 255, 255, 0.7) !important;
}

body.knowledge-theme #main-nav .hover\:text-primary:hover {
  color: #81c784 !important;
}

body.knowledge-theme #main-nav .border-primary {
  border-color: #81c784 !important;
}

body.knowledge-theme #main-nav .bg-primary {
  background-color: #2e7d32 !important;
  /* 保留原先的绿色按钮，或者也可以改亮 */
  color: #ffffff !important;
}

body.knowledge-theme #main-nav .hover\:bg-primary\/10:hover {
  background-color: rgba(129, 199, 132, 0.15) !important;
}
</style>