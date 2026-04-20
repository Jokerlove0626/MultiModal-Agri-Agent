<script setup>
import { ref, shallowRef, onMounted, onUnmounted, nextTick } from 'vue';
import * as echarts from 'echarts';
import { getGraphData } from '@/services/graphApi';
import DOMPurify from 'dompurify';

const chartRef = ref(null);
const chartInstance = shallowRef(null);

const searchQuery = ref('');
const isLoading = ref(true);
const selectedNode = ref(null);

// 定义高颜值的类别颜色 (提取自主题配色的拓展)
const categoryColors = {
  '农作物': { color: '#16a34a', shadow: '#15803d' },  // 翡翠绿
  '病害': { color: '#ef4444', shadow: '#b91c1c' },     // 珊瑚红
  '症状': { color: '#f59e0b', shadow: '#c2410c' },     // 琥珀金
  '药剂': { color: '#3b82f6', shadow: '#1d4ed8' },     // 琉璃蓝
  '防治手段': { color: '#8b5cf6', shadow: '#4338ca' }, // 靛蓝
  '默认': { color: '#64748b', shadow: '#475569' }      // 苍白紫
};

const getCategoryStyle = (categoryName) => {
  const match = categoryColors[categoryName] || categoryColors['默认'];
  return {
    color: match.color,
    shadowColor: match.shadow,
    shadowBlur: 15,
    borderColor: '#ffffff',
    borderWidth: 2,
  };
};

const initChart = () => {
  if (!chartRef.value) return;
  // Initialize ECharts instance
  const myChart = echarts.init(chartRef.value);
  chartInstance.value = myChart;

  // 监听窗口大小改变调整图表大小
  window.addEventListener('resize', handleResize);

  // 绑定点击事件，展示节点详情
  myChart.on('click', (params) => {
    if (params.dataType === 'node') {
      handleNodeClick(params.data);
    }
  });
};

const handleResize = () => {
  chartInstance.value?.resize();
};

const handleNodeClick = (nodeData) => {
  if (nodeData.category === '病害' && nodeData.detail) {
    selectedNode.value = nodeData;
  } else if (nodeData.detail) {
    selectedNode.value = nodeData;
  } else {
    selectedNode.value = null; // 没详情不弹窗
  }
};

const fetchAndRenderData = async () => {
  isLoading.value = true;
  try {
    const res = await getGraphData(searchQuery.value.trim(), 150);
    const { nodes, links } = res.data;

    // 根据类别对节点进行预处理与着色
    const enhancedNodes = nodes.map(node => {
      // 提取分类，为 Echarts 设置分类和样式
      const catStyle = getCategoryStyle(node.category);
      return {
        ...node,
        value: node.category,
        itemStyle: catStyle,
        label: {
          show: node.symbolSize > 30, // 仅对大节点默认显示文字，避免拥挤
          formatter: '{b}',
          fontSize: Math.max(12, node.symbolSize / 4),
          fontWeight: 'bold',
          color: node.category === '病害' ? '#b91c1c' : '#1f2937',
          textBorderColor: '#ffffff',
          textBorderWidth: 3,
        }
      };
    });

    const enhancedLinks = links.map(link => ({
      ...link,
      lineStyle: {
        width: 2,
        curveness: 0.2, // 曲线
        opacity: 0.6,
        color: 'source', // 跟随起点颜色
      },
      label: {
        show: true,
        formatter: link.label || '',
        fontSize: 10,
        color: '#6b7280',
        textBorderColor: '#ffffff',
        textBorderWidth: 2,
      }
    }));

    // 获取图中全部不重复的 category 名称，用于图例
    const categories = [...new Set(enhancedNodes.map(n => n.category))].map(c => ({
      name: c,
      itemStyle: getCategoryStyle(c)
    }));

    const option = {
      backgroundColor: 'transparent',
      tooltip: {
        trigger: 'item',
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        borderColor: '#e5e7eb',
        textStyle: { color: '#1f2937' },
        formatter: (params) => {
          if (params.dataType === 'node') {
            return `<div class="font-bold text-sm mb-1">${params.data.name}</div>
                    <div class="text-xs text-gray-500 border-t pt-1 border-gray-200">类别: ${params.data.category}</div>`;
          } else if (params.dataType === 'edge') {
            return `<div class="text-xs">${params.data.source} <span class="text-primary mx-1">➜</span> ${params.data.target}</div>
                    <div class="font-medium text-sm mt-1">${params.data.label}</div>`;
          }
        }
      },
      legend: [{
        data: categories.map(c => c.name),
        bottom: '3%',
        left: 'center',
        padding: 10,
        itemGap: 20,
        textStyle: {
          color: '#4b5563',
          fontFamily: 'sans-serif',
          fontWeight: 500
        },
        backgroundColor: 'rgba(255,255,255,0.7)',
        borderRadius: 20,
      }],
      animationDurationUpdate: 1500,
      animationEasingUpdate: 'quinticInOut',
      series: [
        {
          type: 'graph',
          layout: 'force', // 使用力引导布局
          data: enhancedNodes,
          links: enhancedLinks,
          categories: categories,
          roam: true, // 允许缩放和拖拽
          zoom: 1.2,
          emphasis: {
            focus: 'adjacency', // 聚焦时突出相关联的节点
            lineStyle: {
              width: 5,
              opacity: 1
            }
          },
          force: {
            repulsion: 400, // 节点排斥力
            edgeLength: [80, 200], // 边长范围
            gravity: 0.1, // 收拢引力
            friction: 0.05
          }
        }
      ]
    };

    chartInstance.value?.setOption(option, true);
  } catch (error) {
    console.error('获取图谱数据失败:', error);
  } finally {
    isLoading.value = false;
  }
};

const handleSearch = () => {
  fetchAndRenderData();
};

onMounted(async () => {
  await nextTick();
  initChart();
  await fetchAndRenderData();
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
  chartInstance.value?.dispose();
});

// 清理富文本
const sanitizeHtml = (html) => {
  return DOMPurify.sanitize(html || '');
};
</script>

<template>
  <div class="relative w-full h-screen bg-surface overflow-hidden text-on-surface font-body selection:bg-primary/20">
    <!-- 专属科技农业背景网格底图 -->
    <div class="absolute inset-0 pointer-events-none opacity-[0.25]"
      style="background-image: radial-gradient(circle at 2px 2px, rgba(18,31,7,0.2) 1px, transparent 0); background-size: 36px 36px;">
    </div>
    <!-- 背景环境光晕 -->
    <div
      class="absolute top-[-10%] right-[-10%] w-[40vw] h-[40vw] bg-primary/20 rounded-full blur-[120px] pointer-events-none">
    </div>
    <div
      class="absolute bottom-[-10%] left-[-10%] w-[50vw] h-[50vw] bg-tertiary/10 rounded-full blur-[140px] pointer-events-none">
    </div>

    <!-- 顶部极简导航与搜索 -->
    <header class="absolute top-0 left-0 w-full z-20 px-6 py-5 flex items-center justify-between pointer-events-none">
      <div
        class="flex items-center gap-3 backdrop-blur-xl bg-white/60 p-2 pr-6 rounded-full shadow-[0_4px_24px_rgba(18,31,7,0.06)] border border-white/40 pointer-events-auto transition-transform hover:scale-[1.02]">
        <div
          class="w-10 h-10 rounded-full bg-primary flex items-center justify-center shrink-0 shadow-lg shadow-primary/30">
          <span class="material-symbols-outlined text-white text-[20px]"
            style="font-variation-settings: 'FILL' 1;">hub</span>
        </div>
        <div>
          <h1 class="font-headline font-bold text-on-surface text-sm tracking-wide leading-tight">病害知识图谱</h1>
          <p class="text-[10px] text-on-surface-variant font-medium mt-0.5">Living Laboratory Graph</p>
        </div>
      </div>

      <div
        class="flex items-center backdrop-blur-xl bg-white/70 rounded-full shadow-[0_8px_32px_rgba(18,31,7,0.08)] border border-white/50 p-1.5 focus-within:ring-2 focus-within:ring-primary/20 transition-all pointer-events-auto w-[320px] max-w-full">
        <span class="material-symbols-outlined text-on-surface-variant ml-3 shrink-0 text-[20px]">search</span>
        <input v-model="searchQuery" @keydown.enter="handleSearch" type="text"
          class="flex-1 bg-transparent border-none text-sm outline-none px-3 py-1.5 text-on-surface placeholder:text-on-surface-variant/50 w-full"
          placeholder="检索特定病害 (如：香蕉叶斑病)" />
        <button @click="handleSearch"
          class="bg-on-surface text-white hover:bg-primary px-4 py-1.5 rounded-full text-xs font-medium transition-colors shadow-md my-auto">
          探索
        </button>
      </div>
    </header>

    <!-- 加载态遮罩 -->
    <transition name="fade">
      <div v-if="isLoading"
        class="absolute inset-0 z-30 flex items-center justify-center bg-surface/50 backdrop-blur-sm">
        <div class="flex flex-col items-center gap-4">
          <div class="relative w-16 h-16 flex items-center justify-center">
            <div class="absolute inset-0 border-4 border-primary/20 rounded-full"></div>
            <div class="absolute inset-0 border-4 border-primary rounded-full border-t-transparent animate-spin"></div>
            <span class="material-symbols-outlined text-primary text-xl animate-pulse">spa</span>
          </div>
          <p class="text-on-surface-variant font-medium text-sm tracking-widest animate-pulse">正在重组知识脉络...</p>
        </div>
      </div>
    </transition>

    <!-- ECharts 图谱层画布 -->
    <div ref="chartRef" class="w-full h-full z-10"></div>

    <!-- 玻璃态详情悬浮面板 面向对象：病害节点详述 -->
    <transition name="slide-card">
      <div v-if="selectedNode"
        class="absolute right-6 top-24 bottom-6 w-[380px] z-20 flex flex-col pointer-events-none">
        <div
          class="bg-white/85 backdrop-blur-[24px] h-full rounded-[24px] shadow-[0_16px_60px_rgba(18,31,7,0.12)] border border-white flex flex-col overflow-hidden pointer-events-auto">
          <!-- 面板头部 -->
          <div
            class="p-6 pb-4 bg-gradient-to-b from-primary/5 to-transparent relative border-b border-outline-variant/15 shrink-0">
            <button @click="selectedNode = null"
              class="absolute top-5 right-5 w-8 h-8 rounded-full bg-white shadow-sm flex items-center justify-center text-on-surface-variant hover:text-error hover:bg-error/10 transition-colors">
              <span class="material-symbols-outlined text-[18px]">close</span>
            </button>
            <div class="inline-flex content-center gap-2 mb-3">
              <span
                class="px-2.5 py-1 bg-primary/10 text-primary text-[10px] font-bold rounded-lg uppercase tracking-widest border border-primary/20">
                {{ selectedNode.category }}
              </span>
            </div>
            <h2 class="text-2xl font-headline font-bold text-on-surface leading-tight mb-2">{{ selectedNode.name }}</h2>
            <p class="text-xs text-on-surface-variant leading-relaxed opacity-80 font-medium">知识脉络识别完毕，点击详情查看应对方案。</p>
          </div>

          <!-- 面板内容滚动区 -->
          <div class="flex-1 overflow-y-auto p-6 pt-2 pb-10 custom-scrollbar relative">
            <div v-if="selectedNode.detail" class="flex flex-col gap-6 pt-4">

              <!-- 摘要 / 简介 -->
              <div v-if="selectedNode.detail.summary" class="group">
                <h3 class="flex items-center gap-2 text-sm font-bold text-primary mb-2">
                  <span class="material-symbols-outlined text-[16px]">menu_book</span>
                  <span>病害摘要</span>
                </h3>
                <div
                  class="prose prose-sm prose-p:leading-relaxed prose-p:text-on-surface/80 prose-headings:text-on-surface"
                  v-html="sanitizeHtml(selectedNode.detail.summary)">
                </div>
              </div>

              <!-- 防治分隔线 -->
              <div v-if="selectedNode.detail.chemical || selectedNode.detail.biological"
                class="w-full h-[1px] bg-gradient-to-r from-transparent via-outline-variant/30 to-transparent my-1">
              </div>

              <!-- 物理/生物防治 -->
              <div v-if="selectedNode.detail.biological" class="group">
                <h3 class="flex items-center gap-2 text-sm font-bold text-secondary mb-2">
                  <span class="material-symbols-outlined text-[16px]">psychiatry</span>
                  <span>生境及综合防治</span>
                </h3>
                <div
                  class="prose prose-sm prose-p:leading-relaxed bg-secondary/5 rounded-xl p-4 border border-secondary/10 text-on-surface/80"
                  v-html="sanitizeHtml(selectedNode.detail.biological)">
                </div>
              </div>

              <!-- 化学防治 -->
              <div v-if="selectedNode.detail.chemical" class="group">
                <h3 class="flex items-center gap-2 text-sm font-bold text-tertiary mb-2">
                  <span class="material-symbols-outlined text-[16px]">science</span>
                  <span>化学药剂防治</span>
                </h3>
                <div
                  class="prose prose-sm prose-p:leading-relaxed bg-tertiary/5 rounded-xl p-4 border border-tertiary/10 text-on-surface/80"
                  v-html="sanitizeHtml(selectedNode.detail.chemical)">
                </div>
              </div>

            </div>

            <div v-else class="h-40 flex flex-col items-center justify-center opacity-50">
              <span class="material-symbols-outlined text-4xl mb-2 text-on-surface-variant">hourglass_empty</span>
              <span class="text-sm">该节点暂无深度解析信息</span>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
/* 骨架级入场动画与过渡 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-card-enter-active {
  transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.slide-card-leave-active {
  transition: all 0.4s cubic-bezier(0.5, 0, 0, 0.2);
}

.slide-card-enter-from,
.slide-card-leave-to {
  opacity: 0;
  transform: translateX(40px) scale(0.98);
}

/* 优美滚动条 */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(18, 31, 7, 0.1);
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: rgba(18, 31, 7, 0.2);
}
</style>