<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from "vue";
import HeroSection from "@/components/home/HeroSection.vue";
import PainPoints from "@/components/home/PainPoints.vue";
import DesignPhilosophy from "@/components/home/DesignPhilosophy.vue";
import CoreFeatures from "@/components/home/CoreFeatures.vue";
import WorkflowTimeline from "@/components/home/WorkflowTimeline.vue";
import TechStack from "@/components/home/TechStack.vue";
import DataCounters from "@/components/home/DataCounters.vue";
import FaqSection from "@/components/home/FaqSection.vue";
import CtaSection from "@/components/home/CtaSection.vue";
import AppFooter from "@/components/home/AppFooter.vue";
import ParticleBackground from "@/components/effects/ParticleBackground.vue";

// ===== Auto-scroll state =====
const SPEED_MIN = 10;
const SPEED_MAX = 300;
const isScrolling = ref(true);
const scrollSpeed = ref(60);
const controlExpanded = ref(false);
const inputFocused = ref(false);

let rafId = null;
let lastTime = 0;

// Exponential curve: slider 0→1 maps to SPEED_MIN→SPEED_MAX via power curve
// sliderValue is the UI slider's 0-100 position (internal, not displayed)
const sliderValue = ref(Math.round(((scrollSpeed.value / SPEED_MIN) ** (1 / 2.5) / (SPEED_MAX / SPEED_MIN) ** (1 / 2.5)) * 100));

const sliderSpeed = computed(() => {
  // Exponential: speed = min * (max/min)^(slider^power)
  // Using power curve for more resolution at low end
  const t = sliderValue.value / 100;
  return Math.round(SPEED_MIN * Math.pow(SPEED_MAX / SPEED_MIN, Math.pow(t, 2.5)));
});

function autoScroll(timestamp) {
  if (!isScrolling.value) {
    rafId = requestAnimationFrame(autoScroll);
    return;
  }

  if (lastTime === 0) lastTime = timestamp;
  const delta = (timestamp - lastTime) / 1000;
  lastTime = timestamp;

  const px = scrollSpeed.value * delta;
  const current = window.scrollY;
  const maxScroll = document.documentElement.scrollHeight - window.innerHeight;

  if (current >= maxScroll - 1) {
    window.scrollTo({ top: 0, behavior: "instant" });
  } else {
    window.scrollBy({ top: px, behavior: "instant" });
  }

  rafId = requestAnimationFrame(autoScroll);
}

function onUserScroll() {
  if (!isScrolling.value) return;
  isScrolling.value = false;
}

function toggleScroll() {
  isScrolling.value = !isScrolling.value;
  if (isScrolling.value) {
    lastTime = 0;
  }
}

function handleSliderInput(e) {
  sliderValue.value = Number(e.target.value);
  scrollSpeed.value = sliderSpeed.value;
}

function setSpeedPreset(s) {
  scrollSpeed.value = s;
  sliderValue.value = Math.round(((s / SPEED_MIN) ** (1 / 2.5) / (SPEED_MAX / SPEED_MIN) ** (1 / 2.5)) * 100);
}

// ===== Keyboard shortcuts (silent — no UI feedback, for screen recording) =====
function onKeyDown(e) {
  // Ignore when user is typing in an input/textarea
  const tag = document.activeElement?.tagName;
  if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT" || document.activeElement?.isContentEditable) {
    return;
  }

  switch (e.key) {
    case " ":
      e.preventDefault();
      toggleScroll();
      break;
    case "1":
      setSpeedPreset(30);
      break;
    case "2":
      setSpeedPreset(60);
      break;
    case "3":
      setSpeedPreset(120);
      break;
    case "4":
      setSpeedPreset(200);
      break;
    case "5":
      setSpeedPreset(300);
      break;
    case "ArrowUp":
      e.preventDefault();
      scrollSpeed.value = Math.min(SPEED_MAX, scrollSpeed.value + 10);
      sliderValue.value = Math.round(((scrollSpeed.value / SPEED_MIN) ** (1 / 2.5) / (SPEED_MAX / SPEED_MIN) ** (1 / 2.5)) * 100);
      break;
    case "ArrowDown":
      e.preventDefault();
      scrollSpeed.value = Math.max(SPEED_MIN, scrollSpeed.value - 10);
      sliderValue.value = Math.round(((scrollSpeed.value / SPEED_MIN) ** (1 / 2.5) / (SPEED_MAX / SPEED_MIN) ** (1 / 2.5)) * 100);
      break;
  }
}

onMounted(() => {
  nextTick(() => {
    const revealElements = document.querySelectorAll('.reveal-up, .reveal-down');
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('active');
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
    revealElements.forEach((el) => revealObserver.observe(el));

    const narrativeElements = document.querySelectorAll('.narrative-item');
    const narrativeObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('active');
        } else {
          entry.target.classList.remove('active');
        }
      });
    }, { threshold: 0.5 });
    narrativeElements.forEach((el) => narrativeObserver.observe(el));

    const timelineItems = document.querySelectorAll('.timeline-item');
    const timelineObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('timeline-item-active');
        } else {
          entry.target.classList.remove('timeline-item-active');
        }
      });
    }, { threshold: 0.5, rootMargin: '-10% 0px -40% 0px' });
    timelineItems.forEach((el) => timelineObserver.observe(el));
  });

  rafId = requestAnimationFrame(autoScroll);
  window.addEventListener("wheel", onUserScroll, { passive: true });
  window.addEventListener("touchmove", onUserScroll, { passive: true });
  window.addEventListener("keydown", onKeyDown);
});

onUnmounted(() => {
  if (rafId) cancelAnimationFrame(rafId);
  window.removeEventListener("wheel", onUserScroll);
  window.removeEventListener("touchmove", onUserScroll);
  window.removeEventListener("keydown", onKeyDown);
});
</script>

<template>
  <div class="home-page overflow-x-hidden relative bg-surface text-on-surface font-body antialiased selection:bg-primary-container selection:text-on-primary-container">
    <div class="fixed inset-0 bg-tech-grid bg-grid-size opacity-30 pointer-events-none z-[-1]"></div>
    <ParticleBackground />
    <HeroSection />
    <PainPoints />
    <DesignPhilosophy />
    <CoreFeatures />
    <WorkflowTimeline />
    <TechStack />
    <DataCounters />
    <FaqSection />
    <CtaSection />
    <AppFooter />

    <!-- Auto-Scroll Control Panel (mouse only) -->
    <div
      class="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-2"
      @mouseenter="controlExpanded = true"
      @mouseleave="controlExpanded = false"
    >
      <div
        :class="[
          'glass-card bg-[#0d2a1a]/90 border border-primary/20 rounded-2xl px-5 py-4 transition-all duration-400 ease-[cubic-bezier(0.25,1,0.5,1)]',
          controlExpanded ? 'opacity-100 translate-y-0 pointer-events-auto' : 'opacity-0 translate-y-2 pointer-events-none'
        ]"
      >
        <div class="flex flex-col gap-3 min-w-[200px]">
          <div class="flex items-center justify-between">
            <span class="text-white/60 text-xs font-headline tracking-wide">滚动速度</span>
            <span class="text-tech-cyan text-sm font-headline font-bold">{{ scrollSpeed }} px/s</span>
          </div>
          <input
            type="range"
            min="0"
            max="100"
            :value="sliderValue"
            @input="handleSliderInput"
            class="scroll-speed-slider w-full h-1.5 rounded-full appearance-none cursor-pointer"
            style="accent-color: #00bcd4;"
          />
          <div class="flex gap-2">
            <button
              v-for="s in [30, 60, 120, 200]"
              :key="s"
              @click="setSpeedPreset(s)"
              :class="[
                'text-[10px] font-headline px-2 py-1 rounded-md border transition-all duration-200',
                scrollSpeed === s
                  ? 'bg-tech-cyan/20 border-tech-cyan text-tech-cyan'
                  : 'bg-white/5 border-white/10 text-white/40 hover:border-white/25 hover:text-white/60'
              ]"
            >{{ s }}</button>
          </div>
        </div>
      </div>

      <button
        @click="toggleScroll"
        :class="[
          'glass-card border rounded-full w-12 h-12 flex items-center justify-center transition-all duration-300 hover:scale-110 active:scale-95',
          isScrolling
            ? 'bg-tech-cyan/15 border-tech-cyan/40 text-tech-cyan shadow-[0_0_20px_rgba(0,188,212,0.3)]'
            : 'bg-[#0d2a1a]/80 border-primary/20 text-white/50 hover:border-primary/40'
        ]"
        :title="isScrolling ? '暂停滚动' : '开始滚动'"
      >
        <span class="material-symbols-outlined text-xl">
          {{ isScrolling ? 'pause' : 'play_arrow' }}
        </span>
      </button>
    </div>
  </div>
</template>
