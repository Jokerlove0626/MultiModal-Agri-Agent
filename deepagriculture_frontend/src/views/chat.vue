<script setup>
import { computed, nextTick, onBeforeUnmount, ref, onMounted, watch } from "vue";
import { postChat, postIdentify, postChatStream, postIdentifyStream } from "@/services/chatApi";
import { marked } from "marked";
import DOMPurify from "dompurify";

// 初始化 marked 配置（支持 Github 风格表格和自动换行）
marked.setOptions({
  gfm: true,
  breaks: true,
  mangle: false,
  headerIds: false
});

function parseStreamingMarkdown(text) {
  if (!text) return "";
  
  // 💥 终极修复：把后端传过来的明文 "\\n" (两个字符) 还原成真正的正则换行符！
  let processedText = text.replace(/\\n/g, '\n');

  // ==========================================
  // 📍 强行修复标题格式 (解决 # ## ### 后无空格问题)
  // ==========================================
  processedText = processedText.replace(/(^|\n)(#{1,6})([^\s#])/g, '$1$2\u3000$3');

  // 1. 智能修复：未闭合的代码块
  const codeBlockCount = (processedText.match(/```/g) || []).length;
  if (codeBlockCount % 2 !== 0) {
    processedText += '\n```'; 
  }

  // 2. 智能修复：未闭合的加粗/斜体
  const boldCount = (processedText.match(/\*\*/g) || []).length;
  if (boldCount % 2 !== 0) {
    processedText += '**';
  }

  // 3. 将修复好的纯净 Markdown 转为 HTML
  const rawHtml = marked.parse(processedText);

  // 4. 净化 HTML
  return DOMPurify.sanitize(rawHtml);
}

// ==========================================
// 📍 多会话管理与本地持久化逻辑
// ==========================================
const STORAGE_KEY = "deepagriculture.chat_sessions";
const chatSessions = ref([]);
const currentSessionId = ref("");

// 1. 加载历史会话
const loadSessions = () => {
  const saved = localStorage.getItem(STORAGE_KEY);
  if (saved) {
    try {
      const parsed = JSON.parse(saved);
      if (parsed && parsed.length > 0) {
        chatSessions.value = parsed;
        currentSessionId.value = parsed[0].id;
        return;
      }
    } catch (e) {
      console.warn("历史记录解析失败", e);
    }
  }
  createNewSession();
};

// 2. 新建会话
const createNewSession = () => {
  if (activeStreamController.value) {
    activeStreamController.value.abort();
    activeStreamController.value = null;
  }
  
  const newId = crypto?.randomUUID ? crypto.randomUUID() : String(Date.now());
  const sessionCount = chatSessions.value.length + 1; 
  
  const newSession = {
    id: newId,
    title: `新诊断 #${sessionCount}`,
    updatedAt: Date.now(),
    messages: [
      {
        id: "welcome-" + newId,
        role: "assistant",
        text: "开启新诊断：上传病害照片或描述作物受灾情况。",
      }
    ]
  };

  chatSessions.value.unshift(newSession);
  currentSessionId.value = newId;
};

// 3. 切换会话
const switchSession = (id) => {
  if (activeStreamController.value) {
    activeStreamController.value.abort();
    activeStreamController.value = null;
  }
  currentSessionId.value = id;
  scrollToBottom();
};

// 4. 当前会话的消息流 (用于页面渲染)
const messages = computed(() => {
  const session = chatSessions.value.find(s => s.id === currentSessionId.value);
  return session ? session.messages : [];
});

// 5. 监听数据变化，实时存入 LocalStorage
watch(
  chatSessions,
  (newSessions) => {
    // 过滤掉 loading 状态的消息
    const cleanSessions = newSessions.map(session => ({
      ...session,
      messages: session.messages.filter(m => !m.loading)
    }));
    localStorage.setItem(STORAGE_KEY, JSON.stringify(cleanSessions));
  },
  { deep: true }
);

// 6. 🗑️ 删除历史会话
const deleteSession = (id) => {
  // 原生确认弹窗（防止误触）
  if (!window.confirm("确定要删除这条诊断记录吗？")) return;

  // 找到并移除该会话
  const index = chatSessions.value.findIndex(s => s.id === id);
  if (index !== -1) {
    chatSessions.value.splice(index, 1);
  }

  // 边界情况 1：如果删光了，自动新建一个
  if (chatSessions.value.length === 0) {
    createNewSession();
    return;
  }

  // 边界情况 2：如果删掉的是当前正在显示的会话，自动切换到最新的一个
  if (currentSessionId.value === id) {
    switchSession(chatSessions.value[0].id);
  }
};
// ==========================================

// ==========================================
// 📍 设备原生 GPS/基站定位 + 开源地图解析
// ==========================================
const userLocation = ref({ province: '未知', city: '未知' });

const fetchDeviceLocation = () => {
  if (!navigator.geolocation) {
    console.warn("当前浏览器不支持设备定位功能");
    userLocation.value = { province: '广东省', city: '广州市' };
    return;
  }
  console.log("正在请求设备定位权限...");
  navigator.geolocation.getCurrentPosition(
    async (position) => {
      const lat = position.coords.latitude;
      const lon = position.coords.longitude;
      console.log(`📍 授权成功！获取到设备物理坐标: 纬度 ${lat}, 经度 ${lon}`);
      try {
        const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}&zoom=10&addressdetails=1&accept-language=zh-CN`;
        const res = await fetch(url);
        const data = await res.json();
        if (data && data.address) {
          userLocation.value = {
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
      console.warn('设备定位失败或用户拒绝授权，使用兜底位置:', error.message);
      userLocation.value = { province: '河南省', city: '郑州市' };
    },
    { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
  );
};

// 页面挂载时初始化定位和本地会话
onMounted(() => {
  fetchDeviceLocation();
  loadSessions();
});
// ==========================================

const cropName = ref("");
const queryText = ref("");
const selectedFile = ref(null);
const selectedFilePreviewUrl = ref("");

const isSending = ref(false);
const errorText = ref("");
const activeStreamController = ref(null);
const isRecording = ref(false);
let recognition = null;
let tempQuery = "";

function toggleRecording() {
  if (isRecording.value) {
    isRecording.value = false;
    if (recognition) recognition.stop();
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
        errorText.value = event.error === 'network' 
          ? "语音网络错误。注：Chrome 浏览器的语音识别依赖谷歌服务(在国内可能被墙)，建议使用 Edge 浏览器或开启代理。" 
          : `语音输入出错: ${event.error}`;
      }
      isRecording.value = false;
    };

    recognition.onend = () => { isRecording.value = false; };
  }

  try { recognition.start(); } catch (err) {
    console.error(err);
    isRecording.value = false;
  }
}

const canSend = computed(() => Boolean(queryText.value.trim()) || Boolean(selectedFile.value));

const streamRef = ref(null);
async function scrollToBottom() {
  await nextTick();
  if (!streamRef.value) return;
  streamRef.value.scrollTop = streamRef.value.scrollHeight;
}

function setFile(file) {
  if (selectedFilePreviewUrl.value && file) URL.revokeObjectURL(selectedFilePreviewUrl.value);
  selectedFile.value = file || null;
  selectedFilePreviewUrl.value = file ? URL.createObjectURL(file) : "";
}

function onPickFile(e) {
  const file = e.target.files?.[0];
  setFile(file);
  e.target.value = "";
}

function removeFile() {
  if (selectedFilePreviewUrl.value) URL.revokeObjectURL(selectedFilePreviewUrl.value);
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

  // 获取当前正在操作的会话
  const currentSession = chatSessions.value.find(s => s.id === currentSessionId.value);
  currentSession.updatedAt = Date.now();

  // 自动提取摘要作为标题 (美化左侧边栏)
  if (currentSession.messages.length <= 2 && userText) {
    currentSession.title = userText.length > 12 ? userText.slice(0, 12) + '...' : userText;
  }

  currentSession.messages.push({
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
  currentSession.messages.push({
    id: loadingId,
    role: "assistant",
    text: "",
    loading: true,
  });

  await scrollToBottom();

  try {
    if (file) {
      activeStreamController.value = new AbortController();
      const msg = currentSession.messages.find((m) => m.id === loadingId);

      await postIdentifyStream({
        file,
        cropName: cropNameSnapshot,
        userText: userText,
        sessionId: currentSessionId.value, // 使用多会话的 ID
        province: userLocation.value.province,
        city: userLocation.value.city,
        signal: activeStreamController.value.signal,
        onChunk: (chunk, fullText) => {
          if (msg) {
            msg.loading = false;
            // 🌟 使用大厂级流式修复解析
            msg.text = parseStreamingMarkdown(fullText); 
            scrollToBottom();
          }
        }
      });

      if (msg && !msg.text) {
        msg.loading = false;
        msg.text = DOMPurify.sanitize(marked.parse("对不起，我暂时无法回答。"));
      }
      activeStreamController.value = null;
    } else {
      activeStreamController.value = new AbortController();
      const msg = currentSession.messages.find((m) => m.id === loadingId);

      await postChatStream({
        query: userText,
        sessionId: currentSessionId.value, // 使用多会话的 ID
        province: userLocation.value.province,
        city: userLocation.value.city,
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
      currentSession.messages = currentSession.messages.filter((m) => m.id !== loadingId);
      activeStreamController.value = null;
      return;
    }

    currentSession.messages = currentSession.messages.filter((m) => m.id !== loadingId);
    errorText.value = err instanceof Error ? err.message : String(err);
    currentSession.messages.push({
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
    <nav class="bg-white/70 text-on-surface font-body text-sm antialiased h-screen w-72 flex-col hidden md:flex fixed left-0 top-0 p-4 gap-2 z-20 shadow-[4px_0_24px_rgba(18,31,7,0.03)]">
      <div class="px-4 py-6 mb-2">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-full bg-primary-container flex items-center justify-center shrink-0 shadow-[0_4px_20px_rgba(18,31,7,0.08)]">
            <span class="material-symbols-outlined text-on-primary-container text-xl" style="font-variation-settings: 'FILL' 1;">eco</span>
          </div>
          <div>
            <h1 class="font-headline font-bold text-on-surface text-base leading-tight">智农实验室</h1>
            <p class="text-xs text-on-surface-variant/70 mt-0.5">AI 诊断引擎</p>
          </div>
        </div>
      </div>

      <div class="flex-1 flex flex-col gap-1 overflow-y-auto pr-2 pb-4" style="scrollbar-width: thin;">
        <button
          class="w-full flex items-center justify-center gap-2 px-4 py-3 bg-primary text-on-primary shadow-sm hover:shadow-md rounded-xl font-medium hover:-translate-y-0.5 transition-all duration-200 mb-4"
          type="button" @click="createNewSession">
          <span class="material-symbols-outlined text-[20px]">add</span>
          <span>新建诊断</span>
        </button>

        <div class="text-[11px] font-bold text-on-surface-variant/50 px-3 mb-2 uppercase tracking-wider">历史记录</div>
        
<button 
          v-for="session in chatSessions" 
          :key="session.id"
          @click="switchSession(session.id)"
          :class="[
            'w-full flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200 text-left truncate group relative',
            currentSessionId === session.id 
              ? 'bg-primary/10 text-primary font-medium' 
              : 'text-on-surface-variant hover:bg-surface-variant/70'
          ]"
          type="button">
          
          <span class="material-symbols-outlined text-[18px] shrink-0 opacity-70 group-hover:opacity-100 transition-opacity">
            {{ currentSessionId === session.id ? 'forum' : 'chat_bubble_outline' }}
          </span>
          <span class="text-sm truncate flex-1">{{ session.title }}</span>

          <span 
            @click.stop="deleteSession(session.id)"
            class="material-symbols-outlined text-[16px] opacity-0 group-hover:opacity-60 hover:!opacity-100 hover:text-error transition-all p-1 z-10"
            title="删除此诊断">
            delete
          </span>
        </button>
      </div>

      <div class="flex flex-col gap-1 pt-4 px-2 border-t border-outline-variant/20">
        <button class="w-full flex items-center gap-3 px-3 py-2 text-on-surface-variant/80 hover:bg-surface-variant/70 rounded-xl transition-all duration-200 text-xs" type="button">
          <span class="material-symbols-outlined text-[18px]">description</span>
          <span>文档中心</span>
        </button>
        <button class="w-full flex items-center gap-3 px-3 py-2 text-on-surface-variant/80 hover:bg-surface-variant/70 rounded-xl transition-all duration-200 text-xs" type="button">
          <span class="material-symbols-outlined text-[18px]">help_outline</span>
          <span>技术支持</span>
        </button>
      </div>
    </nav>

    <main class="flex-1 ml-0 md:ml-72 flex flex-col relative bg-surface">
      <div class="absolute inset-0 pointer-events-none opacity-20" style="background-image: radial-gradient(circle at 2px 2px, rgba(18,31,7,0.18) 1px, transparent 0); background-size: 40px 40px;"></div>

      <header class="px-6 md:px-8 py-5 flex items-center justify-between z-10 sticky top-0 bg-surface/80 backdrop-blur-md">
        <div class="flex items-center gap-4">
          <router-link to="/" class="w-10 h-10 rounded-full hover:bg-surface-variant transition-colors text-on-surface-variant flex items-center justify-center -ml-2">
            <span class="material-symbols-outlined">arrow_back</span>
          </router-link>
          <div>
            <h2 class="font-headline font-medium text-[22px] text-on-surface">开启新诊断</h2>
            <p class="text-sm text-on-surface-variant mt-1">上传病害照片或描述作物受灾情况</p>
          </div>
        </div>
        <div class="flex items-center gap-4">
          <button class="p-2 rounded-full hover:bg-surface-container-low transition-colors text-on-surface-variant" type="button" title="更多">
            <span class="material-symbols-outlined">more_vert</span>
          </button>
        </div>
      </header>

      <div ref="streamRef" class="flex-1 overflow-y-auto px-4 md:px-8 lg:px-16 xl:px-24 pb-48 pt-8 flex flex-col gap-10 z-10 w-full max-w-6xl scroll-smooth">
        <div v-for="(m, idx) in messages" :key="m.id" :class="['relative z-10', m.role === 'user' ? 'flex flex-col items-end w-full max-w-3xl ml-auto gap-2' : 'flex items-start gap-4 w-full max-w-3xl mr-auto']">
          <template v-if="m.role === 'user'">
            <div class="flex items-center gap-2 mb-1 px-1">
              <span v-if="m.cropName" class="text-xs font-medium text-on-surface-variant">{{ m.cropName }}</span>
              <span v-if="m.cropName" class="w-1.5 h-1.5 rounded-full bg-outline-variant/50"></span>
              <span class="text-xs text-on-surface-variant">我</span>
            </div>
            <div class="bg-white rounded-2xl rounded-tr-sm p-5 text-on-surface shadow-[0_4px_20px_rgba(18,31,7,0.03)] flex flex-col gap-4 w-full md:w-auto">
              <p class="text-[16px] leading-relaxed whitespace-pre-wrap">{{ m.text || '（图片诊断）' }}</p>
              <div v-if="m.imageUrl" class="relative w-48 h-32 rounded-lg overflow-hidden border border-outline-variant/15 group">
                <img :alt="m.imageName || '上传图片'" :src="m.imageUrl" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" />
              </div>
            </div>
          </template>

          <template v-else>
            <div class="w-10 h-10 rounded-full bg-primary flex items-center justify-center shrink-0 mt-1 shadow-[0_4px_16px_rgba(18,31,7,0.12)]">
              <span class="material-symbols-outlined text-on-primary text-[20px]" style="font-variation-settings: 'FILL' 1;">psychiatry</span>
            </div>
            <div class="flex-1 flex flex-col gap-1">
              <div class="flex items-center gap-2 mb-1 px-1">
                <span class="text-xs font-medium text-primary">智农大夫 (DeepAgriculture AI)</span>
                <span v-if="m.loading" class="w-2.5 h-4 bg-secondary rounded-[1px] animate-[pulse_1s_ease-in-out_infinite]" style="box-shadow: 0 0 10px rgba(18, 31, 7, 0.25);"></span>
              </div>
              <div class="bg-white p-5 rounded-2xl rounded-tl-sm shadow-[0_4px_20px_rgba(18,31,7,0.03)] text-on-surface text-[16px] leading-relaxed break-words overflow-hidden prose prose-sm md:prose-base !max-w-none prose-p:my-1 prose-headings:my-2 prose-ul:my-1 prose-li:my-0" v-html="m.text"></div>
            </div>
          </template>
        </div>
      </div>

      <div class="absolute bottom-6 left-1/2 -translate-x-1/2 w-full max-w-4xl px-4 z-20">
        <div class="bg-white/90 backdrop-blur-[20px] rounded-[1.5rem] p-3 shadow-[0_8px_40px_rgba(18,31,7,0.06)] border border-outline-variant/10 flex flex-col gap-3 transition-all duration-300 hover:shadow-[0_12px_48px_rgba(18,31,7,0.08)]">
          <div class="flex items-end gap-4 px-2 pt-2">
            <div v-if="selectedFilePreviewUrl" class="relative w-16 h-16 rounded-lg overflow-hidden shadow-sm shrink-0">
              <img :src="selectedFilePreviewUrl" class="w-full h-full object-cover" alt="预览" />
              <button class="absolute top-1 right-1 w-5 h-5 bg-surface/90 rounded-full flex items-center justify-center text-on-surface hover:bg-error hover:text-on-error transition-colors backdrop-blur-sm" type="button" title="移除图片" @click="removeFile">
                <span class="material-symbols-outlined text-[14px]">close</span>
              </button>
            </div>
            <div class="flex-1 max-w-xs relative group">
              <input v-model="cropName" type="text" class="w-full bg-surface-variant text-on-surface text-sm px-4 pt-4 pb-2 rounded-t-md border-none focus:ring-0 focus:outline-none transition-colors group-hover:bg-surface-bright peer placeholder:text-transparent" placeholder="作物种类 (选填)" />
              <label class="absolute left-4 top-1.5 text-[10px] font-medium text-primary transition-all peer-placeholder-shown:text-sm peer-placeholder-shown:top-3 peer-placeholder-shown:text-on-surface-variant peer-focus:top-1.5 peer-focus:text-[10px] peer-focus:text-primary">作物种类 (选填)</label>
              <div class="absolute bottom-0 left-0 w-full h-[2px] bg-primary scale-x-100 transition-transform origin-left"></div>
            </div>
          </div>

          <div class="flex items-end gap-2 bg-white rounded-xl pr-2 pl-1 py-1">
            <div class="flex items-center shrink-0 mb-1">
              <input id="chat-file" type="file" accept="image/*" class="hidden" @change="onPickFile" />
              <label for="chat-file" class="p-2.5 rounded-full text-primary hover:bg-surface-variant transition-colors flex items-center justify-center cursor-pointer" title="上传图片">
                <span class="material-symbols-outlined text-[22px]">image</span>
              </label>
              <button @click="toggleRecording" :class="['p-2.5 rounded-full transition-colors flex items-center justify-center hidden sm:flex', isRecording ? 'bg-primary/20 text-primary shadow-[0_0_12px_rgba(18,31,7,0.15)] animate-pulse' : 'text-on-surface-variant hover:bg-surface-variant hover:text-on-surface']" type="button" :title="isRecording ? '停止语音输入' : '语音输入'">
                <span class="material-symbols-outlined text-[22px]" :style="isRecording ? 'font-variation-settings: \'FILL\' 1;' : ''">mic</span>
              </button>
            </div>
            <textarea v-model="queryText" rows="1" class="flex-1 bg-transparent border-none resize-none outline-none max-h-32 min-h-[44px] text-on-surface placeholder:text-on-surface-variant/60 py-3 px-2 text-[16px] focus:ring-0" placeholder="描述作物症状、土壤情况或询问防治方案..." @keydown.enter="onEnterSend"></textarea>
            <button class="w-11 h-11 mb-0.5 rounded-full bg-gradient-to-br from-primary to-primary-container text-on-primary flex items-center justify-center shrink-0 shadow-[0_4px_12px_rgba(18,31,7,0.12)] hover:shadow-[0_6px_16px_rgba(18,31,7,0.16)] transition-all duration-400 group disabled:opacity-50 disabled:cursor-not-allowed" style="transition-timing-function: cubic-bezier(0.25, 1, 0.5, 1);" :disabled="!canSend || isSending" @click="send" type="button" title="发送">
              <span class="material-symbols-outlined text-[20px] ml-0.5 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform">send</span>
            </button>
          </div>
          <p v-if="errorText" class="text-sm text-error px-2">{{ errorText }}</p>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.damping-spring-effect:active {
  transform: scale(0.97);
  transition: transform 0.1s cubic-bezier(0.25, 1, 0.5, 1);
}

/* Markdown 增强样式 */
/* 优化流式表格抖动 */
:deep(.prose table) {
  width: max-content;
  max-width: 100%;
  overflow-x: auto;
  border-collapse: collapse;
  margin: 1.5rem 0;
  border: 1px solid #e2e8f0;
  display: block;
  /* 🌟 新增：表格布局固定，防止列宽在流输出时疯狂跳动 */
  table-layout: fixed; 
  /* 🌟 新增：增加过渡动画，让流出时更平滑 */
  transition: all 0.3s ease-in-out;
}

:deep(.prose th), :deep(.prose td) {
  border: 1px solid #e2e8f0;
  padding: 12px 16px;
  text-align: left;
  /* 🌟 新增：最小宽度，防止在只有前几个字时表格挤在一起 */
  min-width: 120px; 
}

:deep(.prose th) {
  background-color: #f8fafc;
  font-weight: 700;
  color: #1e293b;
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

:deep(.prose h1) { color: #065f46; border-bottom: 2px solid #065f46; padding-bottom: 0.5rem; }
:deep(.prose h3) { color: #047857; margin-top: 1.5rem; }
:deep(.prose h2) { 
  color: #065f46; 
  border-bottom: 2px solid #065f46; 
  padding-bottom: 0.5rem; 
  margin-top: 0.5rem;
  font-size: 1.5em;
  font-weight: bold;
}

/* 🌟 将默认的引用块爆改为高亮卡片 */
:deep(.prose blockquote) {
  background-color: #f0fdf4; /* 极浅的植保绿色背景 */
  border-left: 4px solid #10b981; /* 鲜艳的翡翠绿侧边栏 */
  padding: 12px 16px;
  margin: 1.2rem 0;
  border-radius: 0 8px 8px 0; /* 右侧圆角 */
  color: #065f46; /* 深绿色文字 */
  font-size: 0.95em;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
}

/* 去除引用块内部段落的默认大边距 */
:deep(.prose blockquote p) {
  margin-top: 0.25rem;
  margin-bottom: 0.25rem;
}

/* 强化引用块内部的加粗标题视觉 */
:deep(.prose blockquote strong) {
  color: #047857; /* 标题颜色更深更醒目 */
  font-size: 1.05em;
}

/* 给 H2 主标题加上底边框 */
:deep(.prose h2) {
  color: #065f46; 
  border-bottom: 2px solid #10b981; 
  padding-bottom: 0.5rem; 
  margin-top: 1rem;
}

</style>