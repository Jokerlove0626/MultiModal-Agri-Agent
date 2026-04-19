<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';

import TopNav from './components/TopNav.vue';

const route = useRoute();
const showTopNav = computed(() => route.name !== 'chat');
</script>

<template>
  <TopNav v-if="showTopNav" />
  <router-view />
</template>

<style>
.material-symbols-outlined {
  font-variation-settings:
    "FILL" 0,
    "wght" 400,
    "GRAD" 0,
    "opsz" 24;
}

/* Reveal Animations */
.reveal-up {
  opacity: 0;
  transform: translateY(40px);
  transition: all 0.8s cubic-bezier(0.5, 0, 0, 1);
}
.reveal-up.active {
  opacity: 1;
  transform: translateY(0);
}

.reveal-down {
  opacity: 0;
  transform: translateY(-40px);
  transition: all 0.8s cubic-bezier(0.5, 0, 0, 1);
}
.reveal-down.active {
  opacity: 1;
  transform: translateY(0);
}

.delay-100 {
  transition-delay: 100ms;
}
.delay-200 {
  transition-delay: 200ms;
}
.delay-300 {
  transition-delay: 300ms;
}
.delay-400 {
  transition-delay: 400ms;
}
.delay-500 {
  transition-delay: 500ms;
}

/* Narrative Scroll Active State */
.narrative-item {
  opacity: 0.4;
  transform: scale(0.95);
  transition: all 0.5s ease;
}
.narrative-item.active {
  opacity: 1;
  transform: scale(1);
}

/* Glassmorphism */
.glass-card {
  background: rgba(232, 245, 233, 0.4);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(46, 125, 50, 0.2);
}
.dark .glass-card {
  background: rgba(27, 94, 32, 0.4);
  border: 1px solid rgba(46, 125, 50, 0.3);
}

/* Graph Animations */
.pulse-node {
  animation: pulse-node-anim 3s infinite alternate;
}
@keyframes pulse-node-anim {
  0% {
    box-shadow: 0 0 10px rgba(46, 125, 50, 0.4);
  }
  100% {
    box-shadow: 0 0 30px rgba(46, 125, 50, 0.8);
  }
}
.glow-line {
  stroke-dasharray: 10;
  animation: dash-anim 20s linear infinite;
  filter: drop-shadow(0 0 4px rgba(46, 125, 50, 0.6));
}
@keyframes dash-anim {
  to {
    stroke-dashoffset: 1000;
  }
}

/* Staggered Text Reveal */
.stagger-line {
  display: block;
  overflow: hidden;
}
.stagger-line > span {
  display: block;
  opacity: 0;
  transform: translateY(100%);
  transition:
    opacity 0.8s cubic-bezier(0.25, 1, 0.5, 1),
    transform 0.8s cubic-bezier(0.25, 1, 0.5, 1);
}
.narrative-item.active .stagger-line > span {
  opacity: 1;
  transform: translateY(0);
}

/* Timeline Animations */
.timeline-line {
  stroke-dasharray: 20;
  animation: timeline-dash-anim 20s linear infinite;
  transition: all 0.5s ease;
}
.timeline-item-active .timeline-line {
  stroke: rgba(129, 199, 132, 0.8);
  filter: drop-shadow(0 0 4px rgba(129, 199, 132, 0.6));
}
.timeline-icon-container {
  transition: all 0.5s cubic-bezier(0.25, 1, 0.5, 1);
}
.timeline-item-active .timeline-icon-container {
  box-shadow: 0 0 20px rgba(129, 199, 132, 0.6);
  border-color: #81c784;
  transform: scale(1.1);
}
.timeline-item-active .timeline-icon {
  color: #81c784;
}
.timeline-content {
  transition: all 0.5s ease;
  opacity: 0.5;
  transform: translateX(20px);
}
.timeline-item-active .timeline-content {
  opacity: 1;
  transform: translateX(0);
}
@keyframes timeline-dash-anim {
  to {
    stroke-dashoffset: -1000;
  }
}
</style>
