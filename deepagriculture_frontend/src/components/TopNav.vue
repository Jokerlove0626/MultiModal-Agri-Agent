<script setup>
import { onMounted, onUnmounted, ref, computed, watch } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const isHomePage = computed(() => route.name === 'home');
const isScrolled = ref(false);
const navVisible = ref(false);

// Watcher ensures correct visibility before first paint
watch(() => route.name, (name) => {
  if (!name || name === 'home') {
    navVisible.value = window.scrollY > window.innerHeight * 0.7;
  } else {
    navVisible.value = true;
  }
}, { immediate: true });

const handleScroll = () => {
	const scrollY = window.scrollY;
	isScrolled.value = scrollY > 50;

	if (isHomePage.value) {
		navVisible.value = scrollY > window.innerHeight * 0.7;
	} else {
		navVisible.value = true;
	}
};

onMounted(() => {
	handleScroll();
	window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
	window.removeEventListener('scroll', handleScroll);
});
</script>

<template>
	<nav
		id="main-nav"
		:class="[
			'backdrop-blur-2xl font-headline tracking-tight sticky top-0 w-full z-50 transition-all duration-500 flex justify-between items-center px-8 py-4 max-w-screen-2xl mx-auto border-b border-transparent',
			isScrolled ? 'glass-card shadow-glow' : 'bg-transparent text-white/90',
			navVisible ? 'translate-y-0 opacity-100 h-auto' : '-translate-y-full opacity-0 h-0 !p-0 !min-h-0 overflow-hidden',
		]"
	>
		<div
			class="text-2xl font-bold text-primary flex items-center gap-2 cursor-pointer hover:scale-95 active:scale-90 transition-transform cubic-bezier(0.25,1,0.5,1)"
		>
			<span class="text-tech-blue">Deep</span><span>Agriculture</span>
			<span class="text-sm font-body text-primary/70 font-normal hidden md:inline-block ml-2">智农大夫</span>
		</div>

		<ul class="hidden md:flex items-center gap-8">
			<li>
				<router-link
					to="/"
					class="font-semibold block cursor-pointer transition-colors"
					active-class="text-tech-blue border-b-2 border-tech-blue pb-1"
					exact-active-class="text-tech-blue border-b-2 border-tech-blue pb-1"
					:class="[isScrolled ? 'text-on-surface/60' : 'text-white/70', 'hover:text-tech-blue']"
				>
					首页
				</router-link>
			</li>
			<li>
				<router-link
					to="/chat"
					class="font-semibold block cursor-pointer transition-colors"
					active-class="text-tech-blue border-b-2 border-tech-blue pb-1"
					:class="[isScrolled ? 'text-on-surface/60' : 'text-white/70', 'hover:text-tech-blue']"
				>
					问答
				</router-link>
			</li>
			<li>
				<router-link
					to="/graph"
					class="font-semibold block cursor-pointer transition-colors"
					active-class="text-tech-blue border-b-2 border-tech-blue pb-1"
					:class="[isScrolled ? 'text-on-surface/60' : 'text-white/70', 'hover:text-tech-blue']"
				>
					知识图谱
				</router-link>
			</li>
			<li>
				<router-link
					to="/monitor"
					class="font-semibold block cursor-pointer transition-colors"
					active-class="text-tech-blue border-b-2 border-tech-blue pb-1"
					:class="[isScrolled ? 'text-on-surface/60' : 'text-white/70', 'hover:text-tech-blue']"
				>
					全国数据监控
				</router-link>
			</li>
			<li>
				<router-link
					to="/knowledge"
					class="font-semibold block cursor-pointer transition-colors"
					active-class="text-tech-blue border-b-2 border-tech-blue pb-1"
					:class="[isScrolled ? 'text-on-surface/60' : 'text-white/70', 'hover:text-tech-blue']"
				>
					知识库
				</router-link>
			</li>
		</ul>

		<div class="flex items-center gap-4">
			<div class="hidden md:flex gap-2">
				<button
					:class="['w-10 h-10 flex items-center justify-center rounded-full transition-all duration-400 scale-95 active:scale-90', isScrolled ? 'text-primary hover:bg-primary/10' : 'text-white/70 hover:bg-white/10']"
				>
					<span class="material-symbols-outlined">account_circle</span>
				</button>
				<button
					:class="['w-10 h-10 flex items-center justify-center rounded-full transition-all duration-400 scale-95 active:scale-90', isScrolled ? 'text-primary hover:bg-primary/10' : 'text-white/70 hover:bg-white/10']"
				>
					<span class="material-symbols-outlined">language</span>
				</button>
			</div>
			<router-link
				to="/chat"
				class="bg-accent-orange text-white px-6 py-2.5 rounded-full font-medium hover:shadow-glow-orange hover:scale-105 transition-all duration-400 ease-[cubic-bezier(0.25,1,0.5,1)]"
			>
				进入实验室
			</router-link>
		</div>
	</nav>
</template>
