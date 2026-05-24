<script setup>
import { onMounted, nextTick } from "vue";
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
	  </div>
	</template>
