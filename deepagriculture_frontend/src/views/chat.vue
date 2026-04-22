<script setup>
import { computed, nextTick, onBeforeUnmount, ref, onMounted } from "vue"; // 👈 新增了 onMounted
import { postChat, postIdentify, postChatStream, postIdentifyStream } from "@/services/chatApi";
import { marked } from "marked";
import DOMPurify from "dompurify";

// 在你的 import 语句下方添加
marked.setOptions({
  gfm: true,      // 启用 GitHub 风格的 Markdown（支持表格）
  breaks: true,   // 启用自动换行（把 \n 转换为 <br>）
  mangle: false,  // 防止一些转义问题
  headerIds: false
});

function getOrCreateSessionId() {
  const key = "deepagriculture.session_id";
  const existing = localStorage.getItem(key);
  if (existing) return existing;
  const id = crypto?.randomUUID ? crypto.randomUUID() : String(Date.now());
  localStorage.setItem(key, id);
  return id;
}

const sessionId = ref(getOrCreateSessionId());

// ==========================================
// 📍 新增：静默获取用户地理位置逻辑
// ==========================================
const userLocation = ref({
  province: '未知',
  city: '未知'
});

// ==========================================
// 📍 设备原生 GPS/基站定位 + 开源地图解析
// ==========================================


const fetchDeviceLocation = () => {
  // 1. 检查设备/浏览器是否支持原生定位
  if (!navigator.geolocation) {
    console.warn("当前浏览器不支持设备定位功能");
    userLocation.value = { province: '广东省', city: '广州市' };
    return;
  }

  console.log("正在请求设备定位权限...");

  // 2. 调起浏览器原生定位（此时会弹窗询问用户权限）
  navigator.geolocation.getCurrentPosition(
    async (position) => {
      // 成功获取设备的物理经纬度！
      const lat = position.coords.latitude;
      const lon = position.coords.longitude;
      console.log(`📍 授权成功！获取到设备物理坐标: 纬度 ${lat}, 经度 ${lon}`);

      try {
        // 3. 拿到经纬度后，使用全球开源地图 (OSM) 把它翻译成中文省市
        // accept-language=zh-CN 确保返回的数据是中文
        const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}&zoom=10&addressdetails=1&accept-language=zh-CN`;
        const res = await fetch(url);
        const data = await res.json();

        if (data && data.address) {
          userLocation.value = {
            // OSM 的省份一般在 state 字段，市可能在 city/town/county 字段
            province: data.address.state || data.address.province || '未知',
            city: data.address.city || data.address.town || data.address.county || '未知'
          };
          console.log('📍 架构师埋点：设备原生定位解析成功 ->', userLocation.value);
        }
      } catch (err) {
        console.warn('经纬度转省市网络请求失败，使用兜底位置:', err);
        userLocation.value = { province: '广东省', city: '广州市' };
      }
    },
    (error) => {
      // 用户点击了“拒绝”，或者设备没有开启定位功能
      console.warn('设备定位失败或用户拒绝授权，使用兜底位置:', error.message);
      userLocation.value = { province: '河南省', city: '郑州市' }; // 拒绝时的兜底
    },
    {
      enableHighAccuracy: true, // 要求高精度定位
      timeout: 10000,           // 超时时间 10 秒
      maximumAge: 0             // 拒绝使用缓存位置
    }
  );
};

// 页面挂载时调用（注意：这里会触发浏览器的定位弹窗）
onMounted(() => {
  fetchDeviceLocation();
});
// ==========================================


const cropName = ref("");
const queryText = ref("");
const selectedFile = ref(null);
const selectedFilePreviewUrl = ref("");

const messages = ref([
  {
    id: crypto?.randomUUID ? crypto.randomUUID() : "welcome",
    role: "assistant",
    text: "开启新诊断：上传病害照片或描述作物受灾情况。",
  },
]);

const isSending = ref(false);
const errorText = ref("");

const activeStreamController = ref(null);

const isRecording = ref(false);
let recognition = null;
let tempQuery = "";

function toggleRecording() {
  if (isRecording.value) {
    isRecording.value = false;
    if (recognition) {
      recognition.stop();
    }
    return;
  }

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    errorText.value = "当前浏览器不支持语音识别，请使用 Chrome 或 Edge 浏览器。";
    return;
  }

  if (!recognition) {
    recognition = new SpeechRecognition();
    recognition.lang = "zh-CN";
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onstart = () => {
      isRecording.value = true;
      errorText.value = "";
      tempQuery = queryText.value ? queryText.value + " " : "";
    };

    recognition.onresult = (event) => {
      let currentTranscript = "";
      for (let i = 0; i < event.results.length; i++) {
        currentTranscript += event.results[i][0].transcript;
      }
      queryText.value = tempQuery + currentTranscript;
    };

    recognition.onerror = (event) => {
      if (event.error !== 'aborted') {
        if (event.error === 'network') {
          errorText.value = "语音网络错误。注：Chrome 浏览器的语音识别依赖谷歌服务(在国内可能被墙)，建议使用 Edge 浏览器或开启代理。";
        } else {
          errorText.value = `语音输入出错: ${event.error}`;
        }
      }
      isRecording.value = false;
    };

    recognition.onend = () => {
      isRecording.value = false;
    };
  }

  try {
    recognition.start();
  } catch (err) {
    console.error(err);
    isRecording.value = false;
  }
}

const canSend = computed(() => {
  return Boolean(queryText.value.trim()) || Boolean(selectedFile.value);
});

const streamRef = ref(null);
async function scrollToBottom() {
  await nextTick();
  if (!streamRef.value) return;
  streamRef.value.scrollTop = streamRef.value.scrollHeight;
}

function resetChat() {
  if (activeStreamController.value) {
    activeStreamController.value.abort();
    activeStreamController.value = null;
  }

  messages.value = [
    {
      id: crypto?.randomUUID ? crypto.randomUUID() : "welcome",
      role: "assistant",
      text: "开启新诊断：上传病害照片或描述作物受灾情况。",
    },
  ];
  errorText.value = "";
}

function setFile(file) {
  if (selectedFilePreviewUrl.value && file) {
    URL.revokeObjectURL(selectedFilePreviewUrl.value);
  }
  selectedFile.value = file || null;
  selectedFilePreviewUrl.value = file ? URL.createObjectURL(file) : "";
}

function onPickFile(e) {
  const file = e.target.files?.[0];
  setFile(file);
  e.target.value = "";
}

function removeFile() {
  if (selectedFilePreviewUrl.value) {
    URL.revokeObjectURL(selectedFilePreviewUrl.value);
  }
  setFile(null);
}

onBeforeUnmount(() => {
  if (selectedFilePreviewUrl.value) URL.revokeObjectURL(selectedFilePreviewUrl.value);
});

async function send() {
  if (!canSend.value || isSending.value) return;

  if (activeStreamController.value) {
    activeStreamController.value.abort();
    activeStreamController.value = null;
  }

  errorText.value = "";
  isSending.value = true;

  const userText = queryText.value.trim();
  const file = selectedFile.value;
  const cropNameSnapshot = cropName.value.trim();

  messages.value.push({
    id: crypto?.randomUUID ? crypto.randomUUID() : String(Date.now()),
    role: "user",
    text: userText,
    imageUrl: selectedFilePreviewUrl.value || "",
    imageName: file?.name || "",
    cropName: cropNameSnapshot,
  });

  queryText.value = "";
  selectedFile.value = null;
  selectedFilePreviewUrl.value = "";

  const loadingId = crypto?.randomUUID ? crypto.randomUUID() : `loading-${Date.now()}`;
  messages.value.push({
    id: loadingId,
    role: "assistant",
    text: "",
    loading: true,
  });

  await scrollToBottom();

  try {
    if (file) {
      activeStreamController.value = new AbortController();
      const msg = messages.value.find((m) => m.id === loadingId);

      await postIdentifyStream({
        file,
        cropName: cropNameSnapshot,
        userText: userText,
        sessionId: sessionId.value,
        province: userLocation.value.province, // 👈 关键注入点：多模态请求携带定位
        city: userLocation.value.city,         // 👈 关键注入点
        signal: activeStreamController.value.signal,
        onChunk: (chunk, fullText) => {
          if (msg) {
            msg.loading = false;
            msg.text = DOMPurify.sanitize(marked.parse(fullText));
            scrollToBottom();
          }
        },
      });

      if (msg && !msg.text) {
        msg.loading = false;
        msg.text = DOMPurify.sanitize(marked.parse("对不起，我暂时无法回答。"));
      }
      activeStreamController.value = null;
    } else {
      activeStreamController.value = new AbortController();
      const msg = messages.value.find((m) => m.id === loadingId);

      await postChatStream({
        query: userText,
        sessionId: sessionId.value,
        province: userLocation.value.province, // 👈 关键注入点：纯文本请求携带定位
        city: userLocation.value.city,         // 👈 关键注入点
        signal: activeStreamController.value.signal,
        onChunk: (chunk, fullText) => {
          if (msg) {
            msg.loading = false;
            msg.text = DOMPurify.sanitize(marked.parse(fullText));
            scrollToBottom();
          }
        },
      });

      if (msg && !msg.text) {
        msg.loading = false;
        msg.text = DOMPurify.sanitize(marked.parse("对不起，我暂时无法回答。"));
      }
      activeStreamController.value = null;
    }
  } catch (err) {
    if (err?.name === "AbortError") {
      messages.value = messages.value.filter((m) => m.id !== loadingId);
      activeStreamController.value = null;
      return;
    }

    messages.value = messages.value.filter((m) => m.id !== loadingId);
    errorText.value = err instanceof Error ? err.message : String(err);
    messages.value.push({
      id: crypto?.randomUUID ? crypto.randomUUID() : String(Date.now() + 2),
      role: "assistant",
      text: `请求失败：${errorText.value}`,
    });
  } finally {
    isSending.value = false;
    await scrollToBottom();
  }
}

function onEnterSend(e) {
  if (e.shiftKey) return;
  e.preventDefault();
  send();
}
</script>

<template>
  <div class="bg-background text-on-surface font-body h-screen flex overflow-hidden selection:bg-primary/20">
    <nav
      class="bg-white/70 text-on-surface font-body text-sm antialiased h-screen w-72 flex-col hidden md:flex fixed left-0 top-0 p-4 gap-2 z-20">
      <div class="px-4 py-6 mb-4">
        <div class="flex items-center gap-3">
          <div
            class="w-10 h-10 rounded-full bg-primary-container flex items-center justify-center shrink-0 shadow-[0_4px_20px_rgba(18,31,7,0.08)]">
            <span class="material-symbols-outlined text-on-primary-container text-xl"
              style="font-variation-settings: 'FILL' 1;">eco</span>
          </div>
          <div>
            <h1 class="font-headline font-bold text-on-surface text-base leading-tight">
              智农实验室
            </h1>
            <p class="text-xs text-on-surface-variant/70 mt-0.5">AI 诊断引擎</p>
          </div>
        </div>
      </div>

      <div class="flex-1 flex flex-col gap-1 overflow-y-auto pr-2" style="scrollbar-width: thin;">
        <button
          class="w-full flex items-center gap-3 px-4 py-3 bg-primary/10 text-on-surface rounded-xl font-medium hover:translate-x-1 transition-all duration-200 damping-spring-effect"
          type="button" @click="resetChat">
          <span class="material-symbols-outlined text-[20px]">add_box</span>
          <span>新建诊断</span>
        </button>
      </div>

      <div class="flex flex-col gap-1 pt-4 px-2">
        <button
          class="w-full flex items-center gap-3 px-4 py-2 text-on-surface-variant/80 hover:bg-primary/5 rounded-xl hover:translate-x-1 transition-all duration-200 damping-spring-effect text-xs"
          type="button">
          <span class="material-symbols-outlined text-[18px]">description</span>
          <span>文档中心</span>
        </button>
        <button
          class="w-full flex items-center gap-3 px-4 py-2 text-on-surface-variant/80 hover:bg-primary/5 rounded-xl hover:translate-x-1 transition-all duration-200 damping-spring-effect text-xs"
          type="button">
          <span class="material-symbols-outlined text-[18px]">help_outline</span>
          <span>技术支持</span>
        </button>
      </div>
    </nav>

    <main class="flex-1 ml-0 md:ml-72 flex flex-col relative bg-surface">
      <div class="absolute inset-0 pointer-events-none opacity-20"
        style="background-image: radial-gradient(circle at 2px 2px, rgba(18,31,7,0.18) 1px, transparent 0); background-size: 40px 40px;">
      </div>

      <header
        class="px-6 md:px-8 py-5 flex items-center justify-between z-10 sticky top-0 bg-surface/80 backdrop-blur-md">
        <div class="flex items-center gap-4">
          <router-link to="/"
            class="w-10 h-10 rounded-full hover:bg-surface-variant transition-colors text-on-surface-variant flex items-center justify-center -ml-2">
            <span class="material-symbols-outlined">arrow_back</span>
          </router-link>
          <div>
            <h2 class="font-headline font-medium text-[22px] text-on-surface">开启新诊断</h2>
            <p class="text-sm text-on-surface-variant mt-1">上传病害照片或描述作物受灾情况</p>
          </div>
        </div>
        <div class="flex items-center gap-4">
          <button class="p-2 rounded-full hover:bg-surface-container-low transition-colors text-on-surface-variant"
            type="button" title="更多">
            <span class="material-symbols-outlined">more_vert</span>
          </button>
        </div>
      </header>

      <div ref="streamRef"
        class="flex-1 overflow-y-auto px-4 md:px-8 lg:px-16 xl:px-24 pb-48 pt-8 flex flex-col gap-10 z-10 w-full max-w-6xl scroll-smooth">

        <div v-for="(m, idx) in messages" :key="m.id" :class="[
          'relative z-10',
          m.role === 'user'
            ? 'flex flex-col items-end w-full max-w-3xl ml-auto gap-2'
            : 'flex items-start gap-4 w-full max-w-3xl mr-auto',
        ]">
          <template v-if="m.role === 'user'">
            <div class="flex items-center gap-2 mb-1 px-1">
              <span v-if="m.cropName" class="text-xs font-medium text-on-surface-variant">{{ m.cropName }}</span>
              <span v-if="m.cropName" class="w-1.5 h-1.5 rounded-full bg-outline-variant/50"></span>
              <span class="text-xs text-on-surface-variant">我</span>
            </div>
            <div
              class="bg-white rounded-2xl rounded-tr-sm p-5 text-on-surface shadow-[0_4px_20px_rgba(18,31,7,0.03)] flex flex-col gap-4 w-full md:w-auto">
              <p class="text-[16px] leading-relaxed whitespace-pre-wrap">{{ m.text || '（图片诊断）' }}</p>
              <div v-if="m.imageUrl"
                class="relative w-48 h-32 rounded-lg overflow-hidden border border-outline-variant/15 group">
                <img :alt="m.imageName || '上传图片'" :src="m.imageUrl"
                  class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" />
              </div>
            </div>
          </template>

          <template v-else>
            <div
              class="w-10 h-10 rounded-full bg-primary flex items-center justify-center shrink-0 mt-1 shadow-[0_4px_16px_rgba(18,31,7,0.12)]">
              <span class="material-symbols-outlined text-on-primary text-[20px]"
                style="font-variation-settings: 'FILL' 1;">psychiatry</span>
            </div>
            <div class="flex-1 flex flex-col gap-1">
              <div class="flex items-center gap-2 mb-1 px-1">
                <span class="text-xs font-medium text-primary">智农大夫 (DeepAgriculture AI)</span>
                <span v-if="m.loading"
                  class="w-2.5 h-4 bg-secondary rounded-[1px] animate-[pulse_1s_ease-in-out_infinite]"
                  style="box-shadow: 0 0 10px rgba(18, 31, 7, 0.25);"></span>
              </div>
              <div
                class="bg-white p-5 rounded-2xl rounded-tl-sm shadow-[0_4px_20px_rgba(18,31,7,0.03)] text-on-surface text-[16px] leading-relaxed break-words overflow-hidden prose prose-sm md:prose-base !max-w-none prose-p:my-1 prose-headings:my-2 prose-ul:my-1 prose-li:my-0"
                v-html="m.text">
              </div>
            </div>
          </template>
        </div>
      </div>

      <div class="absolute bottom-6 left-1/2 -translate-x-1/2 w-full max-w-4xl px-4 z-20">
        <div
          class="bg-white/90 backdrop-blur-[20px] rounded-[1.5rem] p-3 shadow-[0_8px_40px_rgba(18,31,7,0.06)] border border-outline-variant/10 flex flex-col gap-3 transition-all duration-300 hover:shadow-[0_12px_48px_rgba(18,31,7,0.08)]">
          <div class="flex items-end gap-4 px-2 pt-2">
            <div v-if="selectedFilePreviewUrl" class="relative w-16 h-16 rounded-lg overflow-hidden shadow-sm shrink-0">
              <img :src="selectedFilePreviewUrl" class="w-full h-full object-cover" alt="预览" />
              <button
                class="absolute top-1 right-1 w-5 h-5 bg-surface/90 rounded-full flex items-center justify-center text-on-surface hover:bg-error hover:text-on-error transition-colors backdrop-blur-sm"
                type="button" title="移除图片" @click="removeFile">
                <span class="material-symbols-outlined text-[14px]">close</span>
              </button>
            </div>

            <div class="flex-1 max-w-xs relative group">
              <input v-model="cropName" type="text"
                class="w-full bg-surface-variant text-on-surface text-sm px-4 pt-4 pb-2 rounded-t-md border-none focus:ring-0 focus:outline-none transition-colors group-hover:bg-surface-bright peer placeholder:text-transparent"
                placeholder="作物种类 (选填)" />
              <label
                class="absolute left-4 top-1.5 text-[10px] font-medium text-primary transition-all peer-placeholder-shown:text-sm peer-placeholder-shown:top-3 peer-placeholder-shown:text-on-surface-variant peer-focus:top-1.5 peer-focus:text-[10px] peer-focus:text-primary">作物种类
                (选填)</label>
              <div
                class="absolute bottom-0 left-0 w-full h-[2px] bg-primary scale-x-100 transition-transform origin-left">
              </div>
            </div>
          </div>

          <div class="flex items-end gap-2 bg-white rounded-xl pr-2 pl-1 py-1">
            <div class="flex items-center shrink-0 mb-1">
              <input id="chat-file" type="file" accept="image/*" class="hidden" @change="onPickFile" />
              <label for="chat-file"
                class="p-2.5 rounded-full text-primary hover:bg-surface-variant transition-colors flex items-center justify-center cursor-pointer"
                title="上传图片">
                <span class="material-symbols-outlined text-[22px]">image</span>
              </label>
              <button @click="toggleRecording" :class="[
                'p-2.5 rounded-full transition-colors flex items-center justify-center hidden sm:flex',
                isRecording
                  ? 'bg-primary/20 text-primary shadow-[0_0_12px_rgba(18,31,7,0.15)] animate-pulse'
                  : 'text-on-surface-variant hover:bg-surface-variant hover:text-on-surface'
              ]" type="button" :title="isRecording ? '停止语音输入' : '语音输入'">
                <span class="material-symbols-outlined text-[22px]"
                  :style="isRecording ? 'font-variation-settings: \'FILL\' 1;' : ''">mic</span>
              </button>
            </div>

            <textarea v-model="queryText" rows="1"
              class="flex-1 bg-transparent border-none resize-none outline-none max-h-32 min-h-[44px] text-on-surface placeholder:text-on-surface-variant/60 py-3 px-2 text-[16px] focus:ring-0"
              placeholder="描述作物症状、土壤情况或询问防治方案..." @keydown.enter="onEnterSend"></textarea>

            <button
              class="w-11 h-11 mb-0.5 rounded-full bg-gradient-to-br from-primary to-primary-container text-on-primary flex items-center justify-center shrink-0 shadow-[0_4px_12px_rgba(18,31,7,0.12)] hover:shadow-[0_6px_16px_rgba(18,31,7,0.16)] transition-all duration-400 group disabled:opacity-50 disabled:cursor-not-allowed"
              style="transition-timing-function: cubic-bezier(0.25, 1, 0.5, 1);" :disabled="!canSend || isSending"
              @click="send" type="button" title="发送">
              <span
                class="material-symbols-outlined text-[20px] ml-0.5 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform">send</span>
            </button>
          </div>

          <p v-if="errorText" class="text-sm text-error px-2">{{ errorText }}</p>
        </div>
      </div>
    </main>
  </div>
</template>s

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.damping-spring-effect:active {
  transform: scale(0.97);
  transition: transform 0.1s cubic-bezier(0.25, 1, 0.5, 1);
}

/* Markdown 增强样式 */
:deep(.prose table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
  font-size: 0.9em;
}

:deep(.prose th), :deep(.prose td) {
  border: 1px solid #e2e8f0;
  padding: 8px 12px;
  text-align: left;
}

:deep(.prose th) {
  background-color: #f8fafc;
  font-weight: 600;
}

:deep(.prose tr:nth-child(even)) {
  background-color: #f1f5f9;
}

:deep(.prose ul), :deep(.prose ol) {
  padding-left: 1.5rem;
  margin: 0.5rem 0;
}

:deep(.prose li) {
  margin-bottom: 0.25rem;
}

:deep(.prose strong) {
  color: #1e293b;
  font-weight: 700;
}

</style>
