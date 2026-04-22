<script setup>
import { onMounted, onUnmounted, ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const isScrolled = ref(false);
const isDarkBackground = ref(false);

const handleScroll = () => {
	isScrolled.value = window.scrollY > 50;

	// Only apply on home page where dark sections exist
	if (route.path === '/') {
		// Get element under the middle of the navbar (approx 30px from top)
		const elements = document.elementsFromPoint(window.innerWidth / 2, 30);

		// Check if any element has dark background classes
		let darkBg = false;
		for (const el of elements) {
			if (el.classList && (
				el.classList.contains('bg-tech-dark') ||
				el.classList.contains('bg-[#0d1f11]') ||
				el.classList.contains('bg-tech-darker') ||
				(el.classList.contains('bg-gradient-to-br') && el.classList.contains('from-tech-dark')) // CTA section
			)) {
				darkBg = true;
				break;
			}
		}
		isDarkBackground.value = darkBg;
	} else {
		isDarkBackground.value = false;
	}
};

onMounted(() => {
	window.addEventListener('scroll', handleScroll, { passive: true });
});

onUnmounted(() => {
	window.removeEventListener('scroll', handleScroll);
});
</script>

<template>
	<nav id="main-nav" :class="[
		'backdrop-blur-2xl font-headline tracking-tight sticky top-0 w-full z-50 transition-all duration-300 border-b border-transparent',
		isScrolled ? 'glass-card shadow-glow' : 'bg-[#e8f5e9]/70 dark:bg-[#1B5E20]/70',
		isDarkBackground ? 'dark-nav-mode' : ''
	]">
		<div class="max-w-screen-2xl mx-auto w-full flex justify-between items-center px-8 py-4">
			<div
				:class="['text-2xl font-bold flex items-center gap-2 cursor-pointer hover:scale-95 active:scale-90 transition-all duration-300', isDarkBackground ? 'text-white' : 'text-primary']">
				DeepAgriculture
				<span
					:class="['text-sm font-body font-normal hidden md:inline-block ml-2 transition-colors duration-300', isDarkBackground ? 'text-white/70' : 'text-primary/70']">智农大夫</span>
			</div>

			<ul class="hidden md:flex items-center gap-8">
				<li>
					<router-link to="/" class="font-semibold block cursor-pointer transition-colors"
						:active-class="isDarkBackground ? 'text-primary-fixed border-b-2 border-primary-fixed pb-1' : 'text-primary border-b-2 border-primary pb-1'"
						:exact-active-class="isDarkBackground ? 'text-primary-fixed border-b-2 border-primary-fixed pb-1' : 'text-primary border-b-2 border-primary pb-1'"
						:class="[isDarkBackground ? 'text-white/60 hover:text-white' : 'text-on-surface/60 hover:text-primary']">
						首页
					</router-link>
				</li>
				<li>
					<router-link to="/chat" class="font-semibold block cursor-pointer transition-colors"
						:active-class="isDarkBackground ? 'text-primary-fixed border-b-2 border-primary-fixed pb-1' : 'text-primary border-b-2 border-primary pb-1'"
						:class="[isDarkBackground ? 'text-white/60 hover:text-white' : 'text-on-surface/60 hover:text-primary']">
						问答
					</router-link>
				</li>
				<li>
					<router-link to="/graph" class="font-semibold block cursor-pointer transition-colors"
						:active-class="isDarkBackground ? 'text-primary-fixed border-b-2 border-primary-fixed pb-1' : 'text-primary border-b-2 border-primary pb-1'"
						:class="[isDarkBackground ? 'text-white/60 hover:text-white' : 'text-on-surface/60 hover:text-primary']">
						知识图谱
					</router-link>
				</li>
				<li>
					<router-link to="/monitor" class="font-semibold block cursor-pointer transition-colors"
						:active-class="isDarkBackground ? 'text-primary-fixed border-b-2 border-primary-fixed pb-1' : 'text-primary border-b-2 border-primary pb-1'"
						:class="[isDarkBackground ? 'text-white/60 hover:text-white' : 'text-on-surface/60 hover:text-primary']">
						全国数据监控
					</router-link>
				</li>
				<li>
					<router-link to="/knowledge" class="font-semibold block cursor-pointer transition-colors"
						:active-class="isDarkBackground ? 'text-primary-fixed border-b-2 border-primary-fixed pb-1' : 'text-primary border-b-2 border-primary pb-1'"
						:class="[isDarkBackground ? 'text-white/60 hover:text-white' : 'text-on-surface/60 hover:text-primary']">
						知识库
					</router-link>
				</li>
			</ul>

			<div class="flex items-center gap-4">
				<div class="hidden md:flex gap-2">
					<button
						:class="['w-10 h-10 flex items-center justify-center rounded-full transition-all duration-400 scale-95 active:scale-90', isDarkBackground ? 'text-white hover:bg-white/10' : 'text-primary hover:bg-primary/10']">
						<span class="material-symbols-outlined">account_circle</span>
					</button>
					<button
						:class="['w-10 h-10 flex items-center justify-center rounded-full transition-all duration-400 scale-95 active:scale-90', isDarkBackground ? 'text-white hover:bg-white/10' : 'text-primary hover:bg-primary/10']">
						<span class="material-symbols-outlined">language</span>
					</button>
				</div>
				<router-link to="/chat"
					:class="['px-6 py-2.5 rounded-full font-medium transition-all duration-400 ease-[cubic-bezier(0.25,1,0.5,1)]', isDarkBackground ? 'bg-white text-[#112614] hover:shadow-[0_0_15px_rgba(255,255,255,0.3)] hover:scale-105' : 'bg-primary text-white hover:shadow-glow hover:scale-105']">
					进入实验室
				</router-link>
			</div>
		</div>
	</nav>
</template>

<style scoped>
.dark-nav-mode.glass-card {
	background: rgba(17, 38, 20, 0.7);
	border-bottom: 1px solid rgba(255, 255, 255, 0.1);
	box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
}
</style>
