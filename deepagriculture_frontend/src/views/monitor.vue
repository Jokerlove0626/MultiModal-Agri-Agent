<template>
  <div class="relative w-screen h-screen bg-[#f4fbf7] overflow-hidden">
    <!-- 网格背景装饰 -->
    <div class="absolute inset-0 pointer-events-none z-0">
      <svg width="100%" height="100%">
        <defs>
          <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
            <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#e0f2f1" stroke-width="1"/>
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />
      </svg>
    </div>
    <!-- 地图主体 -->
    <div ref="chartRef" class="w-full h-full z-10"></div>
    <!-- 右侧详情面板 -->
    <transition name="slide-fade">
      <div
        v-if="selectedProvince"
        class="fixed top-0 right-0 h-full w-[350px] max-w-full z-20 flex flex-col
               bg-white/60 backdrop-blur-lg shadow-2xl border-l border-[#a7f3d0] 
               transition-all duration-300"
      >
        <div class="flex items-center justify-between px-6 py-5 border-b border-[#a7f3d0]">
          <h2 class="text-2xl font-bold text-[#059669] tracking-wide">
            {{ selectedProvince.name }}
          </h2>
          <button
            @click="selectedProvince = null"
            class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-[#d1fae5] transition"
            aria-label="关闭"
          >
            <svg class="w-5 h-5 text-[#059669]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="flex-1 px-6 py-6 overflow-y-auto">
          <div v-if="selectedProvince.value !== undefined">
            <div class="mb-4">
              <div class="text-lg text-gray-600">病害爆发总频次</div>
              <div class="text-4xl font-extrabold text-[#34d399] drop-shadow-lg mb-2">
                {{ selectedProvince.value }}
              </div>
            </div>
            <div>
              <div class="text-lg text-gray-600 mb-2">主要病害</div>
              <div v-if="selectedProvince.pests && selectedProvince.pests.length > 0" class="flex flex-wrap gap-2">
                <span
                  v-for="(pest, idx) in selectedProvince.pests"
                  :key="pest"
                  :class="[
                    'px-3 py-1 rounded-full text-sm font-medium shadow',
                    idx % 2 === 0
                      ? 'bg-[#fbbf24]/80 text-[#b45309]'
                      : 'bg-[#ef4444]/80 text-white'
                  ]"
                >
                  {{ pest }}
                </span>
              </div>
              <div v-else class="text-gray-400 italic mt-2">暂无主要病害</div>
            </div>
          </div>
          <div v-else class="flex flex-col items-center justify-center h-40 text-gray-400">
            <svg class="w-12 h-12 mb-2" fill="none" stroke="#a7f3d0" stroke-width="2" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10" />
              <path stroke-linecap="round" stroke-linejoin="round" d="M8 12h8M12 8v8"/>
            </svg>
            <div>该地区暂无近期病虫害上报</div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import chinaJson from '../../public/map/china.json?raw'

const chartRef = ref(null)
let chartInstance = null

// 右侧详情面板选中省份
const selectedProvince = ref(null)

// Mock 数据兜底
const fallbackData = [
  { name: '广东省', value: 12, pests: ['香蕉冠腐病', '柑橘黄龙病'] },
  { name: '江苏省', value: 8, pests: ['水稻纹枯病', '小麦赤霉病'] },
  { name: '四川省', value: 15, pests: ['水稻稻瘟病', '柑橘溃疡病'] },
  { name: '山东省', value: 6, pests: ['苹果轮纹病'] },
  { name: '云南省', value: 10, pests: ['香蕉冠腐病', '水稻稻瘟病'] }
]

// 注册中国地图
echarts.registerMap('china', JSON.parse(chinaJson))

// 生态淡绿风 ECharts 配置
function getOption(data) {
  return {
    backgroundColor: 'rgba(0,0,0,0)', // 透明，由父容器控制背景
    tooltip: {
      trigger: 'item',
      backgroundColor: '#f4fbf7ee',
      borderColor: '#a7f3d0',
      textStyle: { color: '#059669' },
      formatter: params => {
        const { name, value, data } = params
        const pests = data && data.pests ? data.pests.join('、') : '无'
        return `
          <div style="font-size:16px;font-weight:bold;color:#059669;">${name}</div>
          <div>爆发总次数：<span style="color:#34d399">${value ?? 0}</span></div>
          <div>主要病害：<span style="color:#ef4444">${pests}</span></div>
        `
      }
    },
    visualMap: {
      left: 30,
      bottom: 30,
      min: 0,
      max: Math.max(...data.map(d => d.value), 20),
      text: ['高', '低'],
      inRange: {
        color: ['#d1fae5', '#34d399', '#fbbf24', '#ef4444'] // 生态绿到警示红
      },
      calculable: true,
      textStyle: {
        color: '#059669'
      },
      itemWidth: 20,
      itemHeight: 120
    },
    geo: {
      map: 'china',
      roam: true,
      zoom: 1.2,
      label: { show: false },
      itemStyle: {
        areaColor: '#ecfdf5', // 极淡绿
        borderColor: '#6ee7b7',
        shadowColor: '#a7f3d0',
        shadowBlur: 10
      },
      emphasis: {
        label: { show: true, color: '#059669', fontWeight: 'bold' },
        itemStyle: {
          areaColor: '#a7f3d0', // 薄荷绿
          shadowColor: '#6ee7b7',
          shadowBlur: 30,
          borderColor: '#059669',
          borderWidth: 2
        }
      }
    },
    series: [
      {
        type: 'map',
        map: 'china',
        geoIndex: 0,
        roam: true,
        data,
        emphasis: { label: { show: true } }
      }
    ]
  }
}

// 拉取后端数据并渲染地图
async function fetchAndRender() {
  let mapData = []
  try {
    const resp = await fetch('http://localhost:8000/api/dashboard/stats')
    const json = await resp.json()
    if (json.status === 'success' && Array.isArray(json.data)) {
      mapData = json.data
    } else {
      throw new Error('接口返回异常')
    }
  } catch (e) {
    mapData = fallbackData
    console.error('接口请求失败，使用 Mock 数据', e)
  }
  await nextTick()
  if (!chartInstance) {
    chartInstance = echarts.init(chartRef.value)
  }
  chartInstance.setOption(getOption(mapData))
  // 响应式自适应
  window.addEventListener('resize', () => {
    chartInstance && chartInstance.resize()
  })
  // 地图点击事件：下钻详情
  chartInstance.on('click', params => {
    if (params && params.data) {
      selectedProvince.value = {
        name: params.data.name,
        value: params.data.value,
        pests: params.data.pests
      }
    } else {
      // 没有数据的省份
      selectedProvince.value = { name: params.name }
    }
  })
}

onMounted(() => {
  fetchAndRender()
})
</script>

<style scoped>
/* 右侧面板动画 */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.35s cubic-bezier(.4,0,.2,1);
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
.slide-fade-enter-to,
.slide-fade-leave-from {
  transform: translateX(0);
  opacity: 1;
}
</style>