<script setup>
import { computed, nextTick, onBeforeUnmount, ref } from "vue";
import { postChatStream, postIdentify } from "@/services/chatApi";

function getOrCreateSessionId() {
  const key = "deepagriculture.session_id";
  const existing = localStorage.getItem(key);
  if (existing) return existing;
  const id = crypto?.randomUUID ? crypto.randomUUID() : String(Date.now());
  localStorage.setItem(key, id);
  return id;
}

const sessionId = ref(getOrCreateSessionId());

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
  if (selectedFilePreviewUrl.value) URL.revokeObjectURL(selectedFilePreviewUrl.value);
  selectedFile.value = file || null;
  selectedFilePreviewUrl.value = file ? URL.createObjectURL(file) : "";
}

function onPickFile(e) {
  const file = e.target.files?.[0];
  setFile(file);
  e.target.value = "";
}

function removeFile() {
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
  setFile(null);

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
      const payload = await postIdentify({
        file,
        cropName: cropNameSnapshot || undefined,
        userText: userText || undefined,
        sessionId: sessionId.value,
      });

      const answer =
        payload == null
          ? ""
          : typeof payload === "string"
            ? payload
            : typeof payload.answer === "string"
              ? payload.answer
              : typeof payload.data?.answer === "string"
                ? payload.data.answer
                : typeof payload.message === "string"
                  ? payload.message
                  : typeof payload.detail === "string"
                    ? payload.detail
                    : JSON.stringify(payload, null, 2);
      messages.value = messages.value.filter((m) => m.id !== loadingId);
      messages.value.push({
        id: crypto?.randomUUID ? crypto.randomUUID() : String(Date.now() + 1),
        role: "assistant",
        text: answer,
      });
    } else {
      const controller = new AbortController();
      activeStreamController.value = controller;

      let pendingScroll = false;
      const scheduleScroll = () => {
        if (pendingScroll) return;
        pendingScroll = true;
        requestAnimationFrame(() => {
          pendingScroll = false;
          scrollToBottom();
        });
      };

      await postChatStream({
        query: userText,
        sessionId: sessionId.value,
        signal: controller.signal,
        onChunk: (chunk) => {
          const msg = messages.value.find((m) => m.id === loadingId);
          if (!msg) return;
          msg.text = (msg.text || "") + chunk;
          scheduleScroll();
        },
      });

      const msg = messages.value.find((m) => m.id === loadingId);
      if (msg) msg.loading = false;
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
      class="bg-white/70 text-on-surface font-body text-sm antialiased h-screen w-72 flex-col hidden md:flex fixed left-0 top-0 p-4 gap-2 z-20"
    >
      <div class="px-4 py-6 mb-4">
        <div class="flex items-center gap-3">
          <div
            class="w-10 h-10 rounded-full bg-primary-container flex items-center justify-center shrink-0 shadow-[0_4px_20px_rgba(18,31,7,0.08)]"
          >
            <span
              class="material-symbols-outlined text-on-primary-container text-xl"
              style="font-variation-settings: 'FILL' 1;"
              >eco</span
            >
          </div>
          <div>
            <h1 class="font-headline font-bold text-on-surface text-base leading-tight">
              Living Laboratory
            </h1>
            <p class="text-xs text-on-surface-variant/70 mt-0.5">AI Diagnostic Engine</p>
          </div>
        </div>
      </div>

      <div class="flex-1 flex flex-col gap-1 overflow-y-auto pr-2" style="scrollbar-width: thin;">
        <button
          class="w-full flex items-center gap-3 px-4 py-3 bg-primary/10 text-on-surface rounded-xl font-medium hover:translate-x-1 transition-all duration-200 damping-spring-effect"
          type="button"
          @click="resetChat"
        >
          <span class="material-symbols-outlined text-[20px]">add_box</span>
          <span>新建诊断</span>
        </button>
      </div>

      <div class="flex flex-col gap-1 pt-4 px-2">
        <button
          class="w-full flex items-center gap-3 px-4 py-2 text-on-surface-variant/80 hover:bg-primary/5 rounded-xl hover:translate-x-1 transition-all duration-200 damping-spring-effect text-xs"
          type="button"
        >
          <span class="material-symbols-outlined text-[18px]">description</span>
          <span>文档中心</span>
        </button>
        <button
          class="w-full flex items-center gap-3 px-4 py-2 text-on-surface-variant/80 hover:bg-primary/5 rounded-xl hover:translate-x-1 transition-all duration-200 damping-spring-effect text-xs"
          type="button"
        >
          <span class="material-symbols-outlined text-[18px]">help_outline</span>
          <span>技术支持</span>
        </button>
      </div>
    </nav>

    <main class="flex-1 ml-0 md:ml-72 flex flex-col relative bg-surface">
      <div
        class="absolute inset-0 pointer-events-none opacity-20"
        style="background-image: radial-gradient(circle at 2px 2px, rgba(18,31,7,0.18) 1px, transparent 0); background-size: 40px 40px;"
      ></div>

      <header class="px-6 md:px-8 py-5 flex items-center justify-between z-10 sticky top-0 bg-surface/80 backdrop-blur-md">
        <div>
          <h2 class="font-headline font-medium text-[22px] text-on-surface">开启新诊断</h2>
          <p class="text-sm text-on-surface-variant mt-1">上传病害照片或描述作物受灾情况</p>
        </div>
        <div class="flex items-center gap-4">
          <button
            class="p-2 rounded-full hover:bg-surface-container-low transition-colors text-on-surface-variant"
            type="button"
            title="更多"
          >
            <span class="material-symbols-outlined">more_vert</span>
          </button>
        </div>
      </header>

      <div
        ref="streamRef"
        class="flex-1 overflow-y-auto px-4 md:px-12 lg:px-24 pb-48 pt-8 flex flex-col gap-10 z-10 w-full max-w-5xl mx-auto scroll-smooth"
      >
        <div
          v-for="(m, idx) in messages"
          :key="m.id"
          :class="[
            'relative z-10 opacity-0 animate-[fadeIn_0.5s_ease-out_forwards]',
            m.role === 'user'
              ? 'flex flex-col items-end w-full max-w-3xl ml-auto gap-2'
              : 'flex items-start gap-4 w-full max-w-3xl mr-auto',
          ]"
          :style="{ animationDelay: `${Math.min(idx * 0.06, 0.3)}s` }"
        >
          <template v-if="m.role === 'user'">
            <div class="flex items-center gap-2 mb-1 px-1">
              <span v-if="m.cropName" class="text-xs font-medium text-on-surface-variant">{{ m.cropName }}</span>
              <span v-if="m.cropName" class="w-1.5 h-1.5 rounded-full bg-outline-variant/50"></span>
              <span class="text-xs text-on-surface-variant">我</span>
            </div>
            <div class="bg-white rounded-2xl rounded-tr-sm p-5 text-on-surface shadow-[0_4px_20px_rgba(18,31,7,0.03)] flex flex-col gap-4 w-full md:w-auto">
              <p class="text-[16px] leading-relaxed whitespace-pre-wrap">{{ m.text || '（图片诊断）' }}</p>
              <div v-if="m.imageUrl" class="relative w-48 h-32 rounded-lg overflow-hidden border border-outline-variant/15 group">
                <img
                  :alt="m.imageName || '上传图片'"
                  :src="m.imageUrl"
                  class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                />
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
                <span
                  v-if="m.loading"
                  class="w-2.5 h-4 bg-secondary rounded-[1px] animate-[pulse_1s_ease-in-out_infinite]"
                  style="box-shadow: 0 0 10px rgba(18, 31, 7, 0.25);"
                ></span>
              </div>
              <div class="bg-white p-5 rounded-2xl rounded-tl-sm shadow-[0_4px_20px_rgba(18,31,7,0.03)] text-on-surface text-[16px] leading-relaxed whitespace-pre-wrap">
                {{ m.text }}
              </div>
            </div>
          </template>
        </div>
      </div>

      <div class="absolute bottom-6 left-1/2 -translate-x-1/2 w-full max-w-4xl px-4 z-20">
        <div class="bg-white/90 backdrop-blur-[20px] rounded-[1.5rem] p-3 shadow-[0_8px_40px_rgba(18,31,7,0.06)] border border-outline-variant/10 flex flex-col gap-3 transition-all duration-300 hover:shadow-[0_12px_48px_rgba(18,31,7,0.08)]">
          <div class="flex items-end gap-4 px-2 pt-2">
            <div v-if="selectedFilePreviewUrl" class="relative w-16 h-16 rounded-lg overflow-hidden shadow-sm shrink-0">
              <img :src="selectedFilePreviewUrl" class="w-full h-full object-cover" alt="预览" />
              <button
                class="absolute top-1 right-1 w-5 h-5 bg-surface/90 rounded-full flex items-center justify-center text-on-surface hover:bg-error hover:text-on-error transition-colors backdrop-blur-sm"
                type="button"
                title="移除图片"
                @click="removeFile"
              >
                <span class="material-symbols-outlined text-[14px]">close</span>
              </button>
            </div>

            <div class="flex-1 max-w-xs relative group">
              <input
                v-model="cropName"
                type="text"
                class="w-full bg-surface-variant text-on-surface text-sm px-4 pt-4 pb-2 rounded-t-md border-none focus:ring-0 focus:outline-none transition-colors group-hover:bg-surface-bright peer placeholder:text-transparent"
                placeholder="作物种类 (选填)"
              />
              <label
                class="absolute left-4 top-1.5 text-[10px] font-medium text-primary transition-all peer-placeholder-shown:text-sm peer-placeholder-shown:top-3 peer-placeholder-shown:text-on-surface-variant peer-focus:top-1.5 peer-focus:text-[10px] peer-focus:text-primary"
                >作物种类 (选填)</label
              >
              <div class="absolute bottom-0 left-0 w-full h-[2px] bg-primary scale-x-100 transition-transform origin-left"></div>
            </div>
          </div>

          <div class="flex items-end gap-2 bg-white rounded-xl pr-2 pl-1 py-1">
            <div class="flex items-center shrink-0 mb-1">
              <input id="chat-file" type="file" accept="image/*" class="hidden" @change="onPickFile" />
              <label
                for="chat-file"
                class="p-2.5 rounded-full text-primary hover:bg-surface-variant transition-colors flex items-center justify-center cursor-pointer"
                title="上传图片"
              >
                <span class="material-symbols-outlined text-[22px]">image</span>
              </label>
              <button
                class="p-2.5 rounded-full text-on-surface-variant hover:bg-surface-variant hover:text-on-surface transition-colors flex items-center justify-center hidden sm:flex"
                type="button"
                disabled
                title="语音输入（暂未接入）"
              >
                <span class="material-symbols-outlined text-[22px]">mic</span>
              </button>
            </div>

            <textarea
              v-model="queryText"
              rows="1"
              class="flex-1 bg-transparent border-none resize-none outline-none max-h-32 min-h-[44px] text-on-surface placeholder:text-on-surface-variant/60 py-3 px-2 text-[16px] focus:ring-0"
              placeholder="描述作物症状、土壤情况或询问防治方案..."
              @keydown.enter="onEnterSend"
            ></textarea>

            <button
              class="w-11 h-11 mb-0.5 rounded-full bg-gradient-to-br from-primary to-primary-container text-on-primary flex items-center justify-center shrink-0 shadow-[0_4px_12px_rgba(18,31,7,0.12)] hover:shadow-[0_6px_16px_rgba(18,31,7,0.16)] transition-all duration-400 group disabled:opacity-50 disabled:cursor-not-allowed"
              style="transition-timing-function: cubic-bezier(0.25, 1, 0.5, 1);"
              :disabled="!canSend || isSending"
              @click="send"
              type="button"
              title="发送"
            >
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
</style>