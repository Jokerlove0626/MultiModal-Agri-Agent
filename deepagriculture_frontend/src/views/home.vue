<script setup>
import { onMounted, nextTick } from "vue";
import HeroSection from "@/components/home/HeroSection.vue";
import PainPoints from "@/components/home/PainPoints.vue";
import DesignPhilosophy from "@/components/home/DesignPhilosophy.vue";
import CoreFeatures from "@/components/home/CoreFeatures.vue";
import WorkflowTimeline from "@/components/home/WorkflowTimeline.vue";

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
			<!-- Tech Stack Section -->
		<section
			class="py-24 bg-tech-darker relative overflow-hidden border-t border-primary/10"
		>
			<div
				class="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-primary/5 via-transparent to-transparent pointer-events-none"
			></div>
			<div class="max-w-[1200px] mx-auto px-8 relative z-10">
				<div class="text-center mb-16 reveal-down">
					<h2
						class="font-headline text-3xl md:text-4xl font-bold text-white mb-4 drop-shadow-[0_0_10px_rgba(129,199,132,0.2)]"
					>
						全栈技术体系，筑牢平台核心能力
					</h2>
					<p
						class="text-white/60 font-body text-lg max-w-2xl mx-auto"
					>
						采用现代化 AI 微服务架构，以高性能和高可扩展性为核心驱动
					</p>
				</div>
				<div
					class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
				>
					<!-- Tech Card 1 -->
					<div
						class="glass-card bg-[#112614]/80 rounded-2xl p-6 border border-primary/20 hover:-translate-y-1 hover:shadow-glow hover:border-primary/50 transition-all duration-300 reveal-up group"
					>
						<div
							class="w-10 h-10 rounded-lg bg-primary/20 flex items-center justify-center mb-4 text-primary-fixed group-hover:scale-110 transition-transform"
						>
							<span class="material-symbols-outlined"
								>memory</span
							>
						</div>
						<h3
							class="text-lg font-bold text-white mb-3 font-headline"
						>
							AI 核心层
						</h3>
						<p class="text-white/60 text-sm leading-relaxed">
							GraphRAG 双引擎 (知识图谱 +
							RAG)、多模态视觉大模型、Python
						</p>
					</div>
					<!-- Tech Card 2 -->
					<div
						class="glass-card bg-[#112614]/80 rounded-2xl p-6 border border-primary/20 hover:-translate-y-1 hover:shadow-glow hover:border-primary/50 transition-all duration-300 reveal-up delay-100 group"
					>
						<div
							class="w-10 h-10 rounded-lg bg-primary/20 flex items-center justify-center mb-4 text-primary-fixed group-hover:scale-110 transition-transform"
						>
							<span class="material-symbols-outlined">dns</span>
						</div>
						<h3
							class="text-lg font-bold text-white mb-3 font-headline"
						>
							后端框架层
						</h3>
						<p class="text-white/60 text-sm leading-relaxed">
							FastAPI、Uvicorn ASGI 服务器、Docker 容器化部署
						</p>
					</div>
					<!-- Tech Card 3 -->
					<div
						class="glass-card bg-[#112614]/80 rounded-2xl p-6 border border-primary/20 hover:-translate-y-1 hover:shadow-glow hover:border-primary/50 transition-all duration-300 reveal-up delay-200 group"
					>
						<div
							class="w-10 h-10 rounded-lg bg-primary/20 flex items-center justify-center mb-4 text-primary-fixed group-hover:scale-110 transition-transform"
						>
							<span class="material-symbols-outlined">speed</span>
						</div>
						<h3
							class="text-lg font-bold text-white mb-3 font-headline"
						>
							架构优化
						</h3>
						<p class="text-white/60 text-sm leading-relaxed">
							全异步 RESTful API、全局单例模式挂载 AI 引擎、CORS
							跨域支持、全网段 0.0.0.0 访问
						</p>
					</div>
					<!-- Tech Card 4 -->
					<div
						class="glass-card bg-[#112614]/80 rounded-2xl p-6 border border-primary/20 hover:-translate-y-1 hover:shadow-glow hover:border-primary/50 transition-all duration-300 reveal-up group"
					>
						<div
							class="w-10 h-10 rounded-lg bg-primary/20 flex items-center justify-center mb-4 text-primary-fixed group-hover:scale-110 transition-transform"
						>
							<span class="material-symbols-outlined">web</span>
						</div>
						<h3
							class="text-lg font-bold text-white mb-3 font-headline"
						>
							前端技术层
						</h3>
						<p class="text-white/60 text-sm leading-relaxed">
							React/Next.js、ECharts/G6 可视化、Ant
							Design、响应式布局
						</p>
					</div>
					<!-- Tech Card 5 -->
					<div
						class="glass-card bg-[#112614]/80 rounded-2xl p-6 border border-primary/20 hover:-translate-y-1 hover:shadow-glow hover:border-primary/50 transition-all duration-300 reveal-up delay-100 group"
					>
						<div
							class="w-10 h-10 rounded-lg bg-primary/20 flex items-center justify-center mb-4 text-primary-fixed group-hover:scale-110 transition-transform"
						>
							<span class="material-symbols-outlined"
								>database</span
							>
						</div>
						<h3
							class="text-lg font-bold text-white mb-3 font-headline"
						>
							数据存储层
						</h3>
						<p class="text-white/60 text-sm leading-relaxed">
							向量数据库、Neo4j 图数据库、关系型数据库
						</p>
					</div>
					<!-- Tech Card 6 -->
					<div
						class="glass-card bg-[#112614]/80 rounded-2xl p-6 border border-primary/20 hover:-translate-y-1 hover:shadow-glow hover:border-primary/50 transition-all duration-300 reveal-up delay-200 group"
					>
						<div
							class="w-10 h-10 rounded-lg bg-primary/20 flex items-center justify-center mb-4 text-primary-fixed group-hover:scale-110 transition-transform"
						>
							<span class="material-symbols-outlined"
								>security</span
							>
						</div>
						<h3
							class="text-lg font-bold text-white mb-3 font-headline"
						>
							安全管控
						</h3>
						<p class="text-white/60 text-sm leading-relaxed">
							管理员 Token 鉴权、403 防护、标准化 FastAPI
							异常状态码响应
						</p>
					</div>
				</div>
			</div>
		</section>
		<!-- Data Counters -->

		<!-- Module 8: Core Data Support (Adapted for Dark Theme) -->
		<section
			class="w-full bg-tech-darker py-24 relative overflow-hidden border-t border-primary/10"
		>
			<div
				class="absolute inset-0 bg-tech-grid bg-grid-size opacity-10 pointer-events-none"
			></div>
			<div
				class="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 w-full relative z-10"
			>
				<div class="text-center mb-16 reveal-down active">
					<h2
						class="text-[1.75rem] font-bold font-headline text-white drop-shadow-[0_0_10px_rgba(129,199,132,0.2)] mb-4"
					>
						权威数据支撑，保障内容专业可靠
					</h2>
					<p
						class="text-[1rem] text-white/60 font-body max-w-2xl mx-auto"
					>
						整合多源权威植保数据，构建动态更新的农业知识库
					</p>
				</div>
				<div
					class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12"
				>
					<!-- Counter Card 1 -->
					<div
						class="glass-card bg-[#112614]/80 border border-primary/20 rounded-2xl p-8 flex flex-col items-center justify-center hover:-translate-y-1 hover:shadow-glow hover:border-primary/50 transition-all duration-400 ease-[cubic-bezier(0.25,1,0.5,1)] reveal-up active group"
					>
						<span
							class="material-symbols-outlined text-primary-fixed text-4xl mb-4 group-hover:scale-110 transition-transform"
							style="font-variation-settings: &quot;FILL&quot; 1"
							>eco</span
						>
						<div
							class="text-[2.5rem] font-bold font-headline text-white mb-2"
						>
							120+
						</div>
						<div class="text-[0.875rem] text-white/60 font-medium">
							覆盖作物 (种)
						</div>
					</div>
					<!-- Counter Card 2 -->
					<div
						class="glass-card bg-[#112614]/80 border border-primary/20 rounded-2xl p-8 flex flex-col items-center justify-center hover:-translate-y-1 hover:shadow-glow hover:border-primary/50 transition-all duration-400 ease-[cubic-bezier(0.25,1,0.5,1)] reveal-up delay-100 active group"
					>
						<span
							class="material-symbols-outlined text-primary-fixed text-4xl mb-4 group-hover:scale-110 transition-transform"
							style="font-variation-settings: &quot;FILL&quot; 1"
							>bug_report</span
						>
						<div
							class="text-[2.5rem] font-bold font-headline text-white mb-2"
						>
							2000+
						</div>
						<div class="text-[0.875rem] text-white/60 font-medium">
							覆盖病虫害 (种)
						</div>
					</div>
					<!-- Counter Card 3 -->
					<div
						class="glass-card bg-[#112614]/80 border border-primary/20 rounded-2xl p-8 flex flex-col items-center justify-center hover:-translate-y-1 hover:shadow-glow hover:border-primary/50 transition-all duration-400 ease-[cubic-bezier(0.25,1,0.5,1)] reveal-up delay-200 active group"
					>
						<span
							class="material-symbols-outlined text-primary-fixed text-4xl mb-4 group-hover:scale-110 transition-transform"
							style="font-variation-settings: &quot;FILL&quot; 1"
							>menu_book</span
						>
						<div
							class="text-[2.5rem] font-bold font-headline text-white mb-2"
						>
							18000+
						</div>
						<div class="text-[0.875rem] text-white/60 font-medium">
							专业知识库 (篇)
						</div>
					</div>
					<!-- Counter Card 4 -->
					<div
						class="glass-card bg-[#112614]/80 border border-primary/20 rounded-2xl p-8 flex flex-col items-center justify-center hover:-translate-y-1 hover:shadow-glow hover:border-primary/50 transition-all duration-400 ease-[cubic-bezier(0.25,1,0.5,1)] reveal-up delay-300 active group"
					>
						<span
							class="material-symbols-outlined text-primary-fixed text-4xl mb-4 group-hover:scale-110 transition-transform"
							style="font-variation-settings: &quot;FILL&quot; 1"
							>image</span
						>
						<div
							class="text-[2.5rem] font-bold font-headline text-white mb-2"
						>
							1200万+
						</div>
						<div class="text-[0.875rem] text-white/60 font-medium">
							标注训练图片 (张)
						</div>
					</div>
				</div>
				<div
					class="text-center text-[0.75rem] text-white/40 font-label mt-8 max-w-4xl mx-auto reveal-up delay-400 active"
				>
					数据来源为中国农业科学院植保所公开数据集、国家农业农村部全国病虫害监测数据、《中国主要农业有害生物》权威工具书、核心农业期刊文献、植保专家知识库
				</div>
			</div>
		</section>
		<!-- Module 9: FAQ Module (Adapted for Dark Theme) -->
		<section
			class="w-full bg-tech-darker py-24 relative overflow-hidden border-t border-primary/10"
		>
			<div
				class="absolute inset-0 bg-tech-grid bg-grid-size opacity-10 pointer-events-none"
			></div>
			<div
				class="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 w-full relative z-10 reveal-up active"
			>
				<div class="mb-12 text-center md:text-left">
					<h2
						class="text-[1.75rem] font-bold font-headline text-white mb-4 drop-shadow-[0_0_10px_rgba(129,199,132,0.2)]"
					>
						常见问题解答
					</h2>
					<p class="text-[1rem] text-white/60 font-body">
						你关心的问题，这里都有答案
					</p>
				</div>
				<div
					class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4 items-start"
				>
					<!-- FAQ Item 1 -->
					<div
						class="glass-card bg-[#112614]/60 rounded-xl p-6 group border border-primary/10 hover:border-primary/30 hover:shadow-[0_0_20px_rgba(46,125,50,0.1)] transition-all"
					>
						<details class="w-full cursor-pointer">
							<summary
								class="flex justify-between items-center text-[1rem] font-semibold text-white list-none"
							>
								平台使用需要收费吗?
								<span
									class="material-symbols-outlined text-primary-fixed transition-transform group-open:rotate-180"
									>expand_more</span
								>
							</summary>
							<p
								class="mt-4 text-[0.875rem] text-white/70 leading-relaxed"
							>
								平台核心功能完全免费，旨在为广大农业工作者提供普惠的AI技术支持。未来部分高级专家定制服务可能会采取灵活的订阅模式，但基础识别与知识库将始终开放。
							</p>
						</details>
					</div>
					<!-- FAQ Item 2 -->
					<div
						class="glass-card bg-[#112614]/60 rounded-xl p-6 group border border-primary/10 hover:border-primary/30 hover:shadow-[0_0_20px_rgba(46,125,50,0.1)] transition-all"
					>
						<details class="w-full cursor-pointer">
							<summary
								class="flex justify-between items-center text-[1rem] font-semibold text-white list-none"
							>
								平台支持哪些作物的病虫害识别?
								<span
									class="material-symbols-outlined text-primary-fixed transition-transform group-open:rotate-180"
									>expand_more</span
								>
							</summary>
							<p
								class="mt-4 text-[0.875rem] text-white/70 leading-relaxed"
							>
								覆盖120+种常见作物，包括水稻、小麦、玉米等大宗粮食作物，以及苹果、柑橘、番茄等主要经济作物和蔬菜。系统模型正在持续迭代扩展中。
							</p>
						</details>
					</div>
					<!-- FAQ Item 3 -->
					<div
						class="glass-card bg-[#112614]/60 rounded-xl p-6 group border border-primary/10 hover:border-primary/30 hover:shadow-[0_0_20px_rgba(46,125,50,0.1)] transition-all"
					>
						<details class="w-full cursor-pointer">
							<summary
								class="flex justify-between items-center text-[1rem] font-semibold text-white list-none"
							>
								上传的图片有什么要求?
								<span
									class="material-symbols-outlined text-primary-fixed transition-transform group-open:rotate-180"
									>expand_more</span
								>
							</summary>
							<p
								class="mt-4 text-[0.875rem] text-white/70 leading-relaxed"
							>
								建议拍摄特写，确保病变部位清晰可见且光照充足。支持JPG/PNG格式，单张图片大小不超过10MB。避免过度模糊或逆光拍摄。
							</p>
						</details>
					</div>
					<!-- FAQ Item 4 -->
					<div
						class="glass-card bg-[#112614]/60 rounded-xl p-6 group border border-primary/10 hover:border-primary/30 hover:shadow-[0_0_20px_rgba(46,125,50,0.1)] transition-all"
					>
						<details class="w-full cursor-pointer">
							<summary
								class="flex justify-between items-center text-[1rem] font-semibold text-white list-none"
							>
								手机上可以使用这个平台吗?
								<span
									class="material-symbols-outlined text-primary-fixed transition-transform group-open:rotate-180"
									>expand_more</span
								>
							</summary>
							<p
								class="mt-4 text-[0.875rem] text-white/70 leading-relaxed"
							>
								做了全移动端适配。您可以通过手机浏览器直接访问，或者关注我们的微信小程序，随时随地在田间地头进行拍照识别。
							</p>
						</details>
					</div>
					<!-- FAQ Item 5 -->
					<div
						class="glass-card bg-[#112614]/60 rounded-xl p-6 group border border-primary/10 hover:border-primary/30 hover:shadow-[0_0_20px_rgba(46,125,50,0.1)] transition-all"
					>
						<details class="w-full cursor-pointer">
							<summary
								class="flex justify-between items-center text-[1rem] font-semibold text-white list-none"
							>
								AI给出的防治方案靠谱吗?
								<span
									class="material-symbols-outlined text-primary-fixed transition-transform group-open:rotate-180"
									>expand_more</span
								>
							</summary>
							<p
								class="mt-4 text-[0.875rem] text-white/70 leading-relaxed"
							>
								基于GraphRAG双引擎检索架构，所有防治方案均溯源至权威农技文献和专家知识库。生成内容经过严格的专家审核校验机制过滤，确保科学性和实用性。
							</p>
						</details>
					</div>
					<!-- FAQ Item 6 -->
					<div
						class="glass-card bg-[#112614]/60 rounded-xl p-6 group border border-primary/10 hover:border-primary/30 hover:shadow-[0_0_20px_rgba(46,125,50,0.1)] transition-all"
					>
						<details class="w-full cursor-pointer">
							<summary
								class="flex justify-between items-center text-[1rem] font-semibold text-white list-none"
							>
								什么是GraphRAG?
								<span
									class="material-symbols-outlined text-primary-fixed transition-transform group-open:rotate-180"
									>expand_more</span
								>
							</summary>
							<p
								class="mt-4 text-[0.875rem] text-white/70 leading-relaxed"
							>
								知识图谱+检索增强生成架构。它结合了知识图谱的结构化逻辑和大型语言模型的生成能力，有效降低了AI的"幻觉"问题，提供逻辑性更强、更精准的解答。
							</p>
						</details>
					</div>
				</div>
			</div>
		</section>
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
