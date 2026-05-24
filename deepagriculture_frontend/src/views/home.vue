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
    <HeroSection />
		<PainPoints />
			<DesignPhilosophy />
			<CoreFeatures />
			<WorkflowTimeline />
			<TechStack />
			<DataCounters />
			<FaqSection />
			<!-- CTA Section -->
		<section
			class="min-h-[80vh] flex items-center justify-center relative overflow-hidden bg-gradient-to-br from-tech-dark via-primary/90 to-tech-dark transition-all duration-1000 py-20"
		>
			<div
				class="absolute inset-0 bg-tech-grid bg-grid-size opacity-20 pointer-events-none"
			></div>
			<div
				class="relative z-10 text-center px-8 max-w-4xl mx-auto flex flex-col items-center justify-center h-full space-y-10 reveal-up"
			>
				<h2
					class="font-headline text-4xl md:text-6xl font-bold text-white leading-tight drop-shadow-lg"
				>
					准备好体验你的随身 AI 植保专家了吗？
				</h2>
				<p class="font-body text-xl text-white/80 max-w-2xl">
					无需注册，无需下载，打开就能用，田间难题一键解决
				</p>
				<button
					class="bg-white text-primary px-10 py-5 rounded-full font-headline font-bold text-lg hover:shadow-glow hover:scale-105 transition-all duration-400 ease-[cubic-bezier(0.25,1,0.5,1)] group"
				>
					立即免费体验 AI 问诊
					<span
						class="material-symbols-outlined ml-2 align-middle group-hover:translate-x-1 transition-transform"
						>arrow_forward</span
					>
				</button>
				<div
					class="pt-16 flex flex-col md:flex-row items-center justify-center gap-12 text-white/70"
				>
					<div class="flex items-center gap-4">
						<div
							class="w-16 h-16 bg-white/10 backdrop-blur border border-white/20 rounded-lg flex items-center justify-center p-2"
						>
							<span
								class="material-symbols-outlined text-3xl text-white/80"
								>qr_code_2</span
							>
						</div>
						<div class="text-left">
							<div class="text-sm font-bold text-white">
								扫码即可手机端使用
							</div>
							<div class="text-xs">随时随地，拍照问诊</div>
						</div>
					</div>
					<div class="w-px h-12 bg-white/20 hidden md:block"></div>
					<div class="flex flex-col gap-2 text-sm text-left">
						<a
							class="hover:text-white transition-colors flex items-center gap-2"
							href="#"
						>
							<span class="material-symbols-outlined text-base"
								>code</span
							>
							开源仓库 GitHub
						</a>
						<a
							class="hover:text-white transition-colors flex items-center gap-2"
							href="#"
						>
							<span class="material-symbols-outlined text-base"
								>mail</span
							>
							contact@deepagri.com
						</a>
					</div>
				</div>
			</div>
		</section>
		<!-- Compliance Footer -->
		<footer
			class="bg-tech-darker text-surface/70 py-16 font-body text-sm border-t border-white/10"
		>
			<div class="max-w-screen-2xl mx-auto px-8 space-y-12">
				<div class="grid grid-cols-2 md:grid-cols-4 gap-8">
					<div class="space-y-4">
						<h4
							class="font-headline font-semibold text-white text-base mb-6"
						>
							平台介绍
						</h4>
						<ul class="space-y-3">
							<li>
								<a
									class="hover:text-primary-fixed transition-colors"
									href="#"
									>关于智农大夫</a
								>
							</li>
							<li>
								<a
									class="hover:text-primary-fixed transition-colors"
									href="#"
									>实验室团队</a
								>
							</li>
							<li>
								<a
									class="hover:text-primary-fixed transition-colors"
									href="#"
									>最新动态</a
								>
							</li>
						</ul>
					</div>
					<div class="space-y-4">
						<h4
							class="font-headline font-semibold text-white text-base mb-6"
						>
							核心功能
						</h4>
						<ul class="space-y-3">
							<li>
								<a
									class="hover:text-primary-fixed transition-colors"
									href="#"
									>图像诊断</a
								>
							</li>
							<li>
								<a
									class="hover:text-primary-fixed transition-colors"
									href="#"
									>知识问答</a
								>
							</li>
							<li>
								<a
									class="hover:text-primary-fixed transition-colors"
									href="#"
									>农业知识图谱</a
								>
							</li>
						</ul>
					</div>
					<div class="space-y-4">
						<h4
							class="font-headline font-semibold text-white text-base mb-6"
						>
							帮助中心
						</h4>
						<ul class="space-y-3">
							<li>
								<a
									class="hover:text-primary-fixed transition-colors"
									href="#"
									>使用指南</a
								>
							</li>
							<li>
								<a
									class="hover:text-primary-fixed transition-colors"
									href="#"
									>常见问题</a
								>
							</li>
							<li>
								<a
									class="hover:text-primary-fixed transition-colors"
									href="#"
									>意见反馈</a
								>
							</li>
						</ul>
					</div>
					<div class="space-y-4">
						<h4
							class="font-headline font-semibold text-white text-base mb-6"
						>
							合规相关
						</h4>
						<ul class="space-y-3">
							<li>
								<a
									class="hover:text-primary-fixed transition-colors"
									href="#"
									>服务协议</a
								>
							</li>
							<li>
								<a
									class="hover:text-primary-fixed transition-colors"
									href="#"
									>隐私政策</a
								>
							</li>
							<li>
								<a
									class="hover:text-primary-fixed transition-colors"
									href="#"
									>免责声明</a
								>
							</li>
						</ul>
					</div>
				</div>
				<div
					class="border-t border-white/10 pt-8 flex flex-col gap-4 text-xs"
				>
					<div
						class="flex flex-col md:flex-row justify-between gap-4"
					>
						<p>
							版权所有 © 2024 DeepAgriculture 智农大夫研发团队 |
							主办单位：XXX 大学 | 指导单位：XXX 农学院
						</p>
						<div class="flex gap-4">
							<span>备案号：京ICP备XXXXXXXX号-1</span>
						</div>
					</div>
					<div
						class="bg-black/30 p-4 rounded-lg border border-white/5 text-surface/60"
					>
						<span class="font-semibold text-primary-fixed"
							>免责声明：</span
						>平台内容仅供参考，不构成农事操作唯一指导建议，具体防治请结合当地实际情况与农技人员专业指导。
					</div>
				</div>
			</div>
		</footer>
	
  </div>
</template>
