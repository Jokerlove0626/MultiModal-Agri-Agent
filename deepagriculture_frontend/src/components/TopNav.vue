<script setup>
import { onMounted, onUnmounted, ref } from 'vue';

const isScrolled = ref(false);

const handleScroll = () => {
	isScrolled.value = window.scrollY > 50;
};

onMounted(() => {
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
			'backdrop-blur-2xl font-headline tracking-tight sticky top-0 w-full z-50 transition-all duration-300 flex justify-between items-center px-8 py-4 max-w-screen-2xl mx-auto border-b border-transparent',
			isScrolled ? 'glass-card shadow-glow' : 'bg-[#e8f5e9]/70 dark:bg-[#1B5E20]/70',
		]"
	>
		<div
			class="text-2xl font-bold text-primary flex items-center gap-2 cursor-pointer hover:scale-95 active:scale-90 transition-transform cubic-bezier(0.25,1,0.5,1)"
		>
			DeepAgriculture
			<span class="text-sm font-body text-primary/70 font-normal hidden md:inline-block ml-2">智农大夫</span>
		</div>

		<ul class="hidden md:flex items-center gap-8">
			<li>
				<router-link
					to="/"
					class="font-semibold block cursor-pointer transition-colors"
					active-class="text-primary border-b-2 border-primary pb-1"
					exact-active-class="text-primary border-b-2 border-primary pb-1"
					:class="['text-on-surface/60 hover:text-primary']"
				>
					首页
				</router-link>
			</li>
			<li>
				<router-link
					to="/chat"
					class="font-semibold block cursor-pointer transition-colors"
					active-class="text-primary border-b-2 border-primary pb-1"
					:class="['text-on-surface/60 hover:text-primary']"
				>
					问答
				</router-link>
			</li>
			<li>
				<router-link
					to="/graph"
					class="font-semibold block cursor-pointer transition-colors"
					active-class="text-primary border-b-2 border-primary pb-1"
					:class="['text-on-surface/60 hover:text-primary']"
				>
					知识图谱
				</router-link>
			</li>
			<li>
				<router-link
					to="/monitor"
					class="font-semibold block cursor-pointer transition-colors"
					active-class="text-primary border-b-2 border-primary pb-1"
					:class="['text-on-surface/60 hover:text-primary']"
				>
					全国数据监控
				</router-link>
			</li>
			<li>
				<router-link
					to="/knowledge"
					class="font-semibold block cursor-pointer transition-colors"
					active-class="text-primary border-b-2 border-primary pb-1"
					:class="['text-on-surface/60 hover:text-primary']"
				>
					知识库
				</router-link>
			</li>
		</ul>

		<div class="flex items-center gap-4">
			<div class="hidden md:flex gap-2">
				<button
					class="w-10 h-10 flex items-center justify-center text-primary hover:bg-primary/10 rounded-full transition-all duration-400 scale-95 active:scale-90"
				>
					<span class="material-symbols-outlined">account_circle</span>
				</button>
				<button
					class="w-10 h-10 flex items-center justify-center text-primary hover:bg-primary/10 rounded-full transition-all duration-400 scale-95 active:scale-90"
				>
					<span class="material-symbols-outlined">language</span>
				</button>
			</div>
			<router-link
				to="/chat"
				class="bg-primary text-white px-6 py-2.5 rounded-full font-medium hover:shadow-glow hover:scale-105 transition-all duration-400 ease-[cubic-bezier(0.25,1,0.5,1)]"
			>
				进入实验室
			</router-link>
		</div>
	</nav>
</template>
