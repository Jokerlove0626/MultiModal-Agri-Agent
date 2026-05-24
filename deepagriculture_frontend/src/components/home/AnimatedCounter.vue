<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  target: { type: Number, required: true },
  suffix: { type: String, default: '' },
  prefix: { type: String, default: '' },
  duration: { type: Number, default: 2000 },
});

const displayValue = ref('0');
const isInView = ref(false);
const elementRef = ref(null);

let observer = null;
let animFrame = null;

function easeOutExpo(t) {
  return t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
}

function animate() {
  const startTime = performance.now();
  const startVal = 0;

  function step(now) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / props.duration, 1);
    const easedProgress = easeOutExpo(progress);
    const current = Math.round(startVal + (props.target - startVal) * easedProgress);

    if (props.target >= 10000) {
      displayValue.value = (current / 10000).toFixed(current % 10000 === 0 ? 0 : 1) + '万';
    } else {
      displayValue.value = current.toString();
    }

    if (progress < 1) {
      animFrame = requestAnimationFrame(step);
    } else {
      displayValue.value = props.target >= 10000
        ? (props.target / 10000).toFixed(0) + '万'
        : props.target.toString();
    }
  }

  animFrame = requestAnimationFrame(step);
}

onMounted(() => {
  observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting && !isInView.value) {
        isInView.value = true;
        animate();
      }
    });
  }, { threshold: 0.3 });

  if (elementRef.value) {
    observer.observe(elementRef.value);
  }
});

onUnmounted(() => {
  if (observer) observer.disconnect();
  if (animFrame) cancelAnimationFrame(animFrame);
});
</script>

<template>
  <span ref="elementRef" class="number-counter inline-block">
    {{ prefix }}{{ displayValue }}{{ suffix }}
  </span>
</template>
