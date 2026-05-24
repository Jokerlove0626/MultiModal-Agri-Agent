# 智农大夫 首页科技风美化计划

## 设计目标

保留绿色农业基调，融入科技蓝 + 活力橙辅助色，叠加粒子/扫描线/数据流等动态效果，将首页从"清新农业风"升级为"智慧农业科技大屏风"。

## 新配色体系

| 色彩角色 | 色值 | 比例 | 应用场景 |
|---|---|---|---|
| 主色（深森林绿） | `#2E7D32` | 60% | 导航栏、标题强调、品牌标识、主按钮 |
| 辅助色（科技蓝） | `#1976D2` | 20% | 数据图表、图标、次要按钮、链接、科技装饰 |
| 辅助色（浅草绿） | `#81C784` | 10% | 背景渐变、卡片边框、进度条、状态提示 |
| 强调色（活力橙） | `#FF9800` | 5% | CTA 按钮、重要通知、数据高亮 |
| 中性色 | `#F5F7FA` / `#E0E0E0` / `#424242` | 5% | 页面背景、分割、正文、次要文字 |

---

## 阶段一：配色地基 + 英雄区改造

**完成后可见**：TopNav 导航栏出现蓝/橙色点缀，英雄区标题渐变发光、图谱动画节点新增蓝色、背景有扫描线效果。

### 任务 1.1：更新 Tailwind 全局色彩配置
- **文件**: `index.html` — `<script id="tailwind-config">`
- **改动**:
  - 新增 `tech-blue` 色阶（`#1976D2` / `#1565C0` / `#42A5F5`）
  - 新增 `tech-cyan`（`#00BCD4` 用于发光）
  - 新增 `accent-orange`（`#FF9800` / `#F57C00`）
  - 新增 `neutral-50/100/200/700` 中性灰色阶
  - 新增 `shadow-glow-blue`、`shadow-glow-orange` box-shadow
  - 新增 `bg-tech-dot` 点阵背景 pattern
- **可见变化**: 新颜色 class 可在浏览器 DevTools 中即时使用

### 任务 1.2：更新全局 CSS 动画库
- **文件**: `src/App.vue` — `<style>` 块
- **改动**:
  - 新增 `.glass-card-blue`（蓝色调玻璃态）
  - 新增 `@keyframes glow-blue-pulse` 蓝色呼吸发光
  - 新增 `@keyframes scan-line` 扫描线（水平光带掠过）
  - 新增 `@keyframes border-glow` 边框呼吸发光
  - 新增 `@keyframes data-flow-dash` 虚线流动
  - 新增 `.tech-dot-bg` 科技点阵背景
- **可见变化**: 页面中使用了这些 class 的元素开始动起来

### 任务 1.3：更新 TopNav 导航栏
- **文件**: `src/components/TopNav.vue`
- **改动**:
  - 活跃链接下划线 `border-tech-blue`（替换纯绿）
  - "进入实验室"按钮改为 `bg-accent-orange` + `hover:shadow-glow-orange`
  - 滚动玻璃态增加蓝色微光（`shadow-[0_0_30px_rgba(25,118,210,0.15)]`）
  - 品牌名 "DeepAgriculture" 中 "Deep" 用科技蓝高亮
- **可见变化**: 导航栏配色明显变化，橙色 CTA 更醒目

### 任务 1.4：拆分并重设计英雄区 HeroSection
- **新建**: `src/components/home/HeroSection.vue`
- **改动**:
  - 标题 `智农大夫` 改为渐变色（绿→蓝 `bg-gradient-to-r from-primary to-tech-blue`）
  - 顶部 badge 增加 `animate-border-glow` 边框呼吸
  - CSS 图谱新增 2 个蓝色节点（带科技蓝发光）+ 蓝色 SVG 连线
  - 中心节点增加旋转光环圈（`animate-spin` 减速版 + blur）
  - 背景增加扫描线动画（`::after` 伪元素，半透明光带从左扫到右）
  - 主 CTA 按钮改为活力橙
- **可见变化**: 英雄区是变化最大的区域，配色/动画全部焕新

### 任务 1.5：更新 home.vue 引用 HeroSection
- **文件**: `src/views/home.vue`
- **改动**: 删除原有 hero 模板代码（L49-L210），替换为 `<HeroSection />`
- **可见变化**: 页面正常渲染，英雄区显示新设计

---

## 阶段二：痛点区 + 设计理念区改造

**完成后可见**：痛点卡片 hover 有蓝色边框发光，设计理念区文字高亮变为科技蓝渐变。

### 任务 2.1：拆分并升级痛点区 PainPoints
- **新建**: `src/components/home/PainPoints.vue`
- **改动**:
  - 卡片 hover 效果从纯绿 shadow 升级为绿→蓝过渡（`hover:shadow-[0_10px_30px_rgba(25,118,210,0.2)]`）
  - 图标区域 hover 时背景变为科技蓝（`group-hover:bg-tech-blue/10`）
  - 标题 hover 颜色变为科技蓝（`group-hover:text-tech-blue`）
  - 标题区加入蓝色下划线装饰
- **可见变化**: 痛点卡片 hover 时有蓝绿交织的科技感

### 任务 2.2：拆分并升级设计理念区 DesignPhilosophy
- **新建**: `src/components/home/DesignPhilosophy.vue`
- **改动**:
  - 高亮文字底色从 `primary/10` 改为 `tech-blue/10` + 文字色 `text-tech-blue`
  - 左侧竖线装饰（`border-l-4`）从绿色改为科技蓝渐变
  - 叙事文字中 "GraphRAG"、"AI" 等关键词用科技蓝高亮
- **可见变化**: 设计理念区文字层次更丰富，科技关键词突出

### 任务 2.3：更新 home.vue 引用新组件
- **文件**: `src/views/home.vue`
- **改动**: 删除痛点 + 设计理念模板代码，替换为 `<PainPoints />` + `<DesignPhilosophy />`
- **可见变化**: 页面前 3 个板块全部为新设计

---

## 阶段三：核心特性区 + 技术流程时间线改造

**完成后可见**：特性卡片有数据粒子动画，时间线有光点流动效果，暗色区域新增科技蓝点缀。

### 任务 3.1：拆分并升级核心特性区 CoreFeatures
- **新建**: `src/components/home/CoreFeatures.vue`
- **改动**:
  - "图谱推理"卡片的 +32% 数字增加旋转光环粒子
  - "拍照即诊"代码块终端增加光标闪烁（`animate-cursor-blink`）
  - "动态大屏"卡片增加扫描线 + 实时脉冲点
  - 卡片边框 hover 时从绿色变为科技蓝
  - 背景增加微弱的蓝色径向渐变叠加
- **可见变化**: 三个特性卡片科技感大幅提升

### 任务 3.2：拆分并升级技术流程时间线 WorkflowTimeline
- **新建**: `src/components/home/WorkflowTimeline.vue`
- **改动**:
  - 时间线 SVG 竖线增加流动光点（`animate-flow-dot`，沿 Y 轴移动的发光圆点）
  - 每个步骤图标 hover 时从绿色变为科技蓝脉冲
  - 激活步骤的发光效果改为蓝绿混合
  - 步骤编号用科技蓝小标签标注
- **可见变化**: 时间线不再是静态线，有光点沿线条运动

### 任务 3.3：更新 home.vue 引用新组件
- **文件**: `src/views/home.vue`
- **改动**: 删除核心特性 + 时间线模板，替换为 `<CoreFeatures />` + `<WorkflowTimeline />`
- **可见变化**: 暗色区域 5 个板块全部刷新

---

## 阶段四：技术栈 + 数据统计 + FAQ 改造

**完成后可见**：数据数字从 0 滚动到目标值，FAQ 展开有平滑动画，技术栈卡片有蓝色图标。

### 任务 4.1：拆分并升级技术栈区 TechStack
- **新建**: `src/components/home/TechStack.vue`
- **改动**:
  - 卡片图标区改为科技蓝背景（`bg-tech-blue/20`）
  - 标题 "前端技术层" 描述修正为实际技术栈（Vue/Vite/ECharts/Tailwind）
  - hover 边框过渡到科技蓝
- **可见变化**: 技术栈卡片图标区变蓝，前端技术栈描述更准确

### 任务 4.2：拆分数据统计区 + 数字滚动动画
- **新建**: `src/components/home/AnimatedCounter.vue`（通用数字滚动组件）
  - props: `target` (目标数字), `suffix` (后缀如 "+"), `duration` (动画时长)
  - IntersectionObserver 触发，`easeOutExpo` 缓动
- **新建**: `src/components/home/DataCounters.vue`
  - 4 个统计卡片使用 `<AnimatedCounter />`
  - 数字颜色改为科技蓝 + 白色渐变
  - 卡片 hover 增加蓝色发光边框
- **可见变化**: 滚动到数据区时数字从 0 动态跳到目标值

### 任务 4.3：拆分并升级 FAQ 区
- **新建**: `src/components/home/FaqSection.vue`
- **改动**:
  - `<details>` 展开/收起用 CSS `interpolate-size: allow-keywords` + `max-height` 过渡实现平滑动画
  - 展开图标用科技蓝旋转
  - 展开时左侧出现蓝色指示条
- **可见变化**: FAQ 折叠不再是生硬的开合

### 任务 4.4：更新 home.vue 引用新组件
- **文件**: `src/views/home.vue`
- **改动**: 删除技术栈 + 数据统计 + FAQ 模板，替换为组件引用
- **可见变化**: 下半部分页面全部刷新

---

## 阶段五：CTA 区 + 页脚 + 粒子背景 + 收尾

**完成后可见**：全页面有粒子网络背景，CTA 按钮脉冲发光，整页完整呈现科技农业风格。

### 任务 5.1：拆分并升级 CTA 区
- **新建**: `src/components/home/CtaSection.vue`
- **改动**:
  - 按钮改为活力橙 + `animate-pulse` 慢速呼吸发光
  - 背景渐变从纯绿改为绿→科技蓝对角线渐变
  - 增加悬浮的科技图标微粒子装饰
- **可见变化**: CTA 区更醒目，橙色按钮脉冲吸引点击

### 任务 5.2：拆分页脚 AppFooter
- **新建**: `src/components/home/AppFooter.vue`
- **改动**:
  - 链接 hover 改为科技蓝 + 下滑线动画
  - 底部 ICP 备案用中性色弱化
- **可见变化**: 页脚配色与整体统一

### 任务 5.3：创建全局粒子背景
- **新建**: `src/components/effects/ParticleBackground.vue`
- **改动**:
  - Canvas 粒子网络动画（节点 + 近距连线）
  - 粒子颜色：科技蓝 60% + 浅草绿 40%
  - 仅在 `lg` 屏幕启用，移动端降级为静态网格
  - `requestAnimationFrame` 驱动，标签页隐藏时暂停
  - 挂载到 home.vue 背景层，`pointer-events-none`
- **可见变化**: 首页背景有缓慢漂浮的粒子网络，科技感质变

### 任务 5.4：home.vue 最终整合
- **文件**: `src/views/home.vue`
- **改动**:
  - 删除 CTA + 页脚模板，替换为组件引用
  - 引入 `<ParticleBackground />`
  - 清理残留的旧代码
  - home.vue 从 1377 行缩减到约 60 行
- **可见变化**: 首页完整呈现，从导航栏到页脚全部焕新

### 任务 5.5：移动端响应式 + 性能收尾
- **改动**:
  - 检查 375px / 768px / 1024px / 1440px 断点
  - `prefers-reduced-motion` 时禁用所有动画
  - Canvas 粒子在非激活标签页暂停
  - IntersectionObserver 确保 disconnect
- **可见变化**: 手机端也能正常浏览，动画不卡顿

---

## 执行顺序

```
阶段一 → 阶段二 → 阶段三 → 阶段四 → 阶段五
  ↓         ↓         ↓         ↓         ↓
导航+英雄   痛点+理念   特性+流程   数据+FAQ   CTA+粒子+收尾
```

**每个阶段结束时，启动 `npm run dev` 可在浏览器看到该阶段的完整成果。**

## 文件变更清单

| 操作 | 文件 | 所属阶段 |
|---|---|---|
| 修改 | `index.html` | 阶段一 |
| 修改 | `src/App.vue` | 阶段一 |
| 修改 | `src/components/TopNav.vue` | 阶段一 |
| 新建 | `src/components/home/HeroSection.vue` | 阶段一 |
| 新建 | `src/components/home/PainPoints.vue` | 阶段二 |
| 新建 | `src/components/home/DesignPhilosophy.vue` | 阶段二 |
| 新建 | `src/components/home/CoreFeatures.vue` | 阶段三 |
| 新建 | `src/components/home/WorkflowTimeline.vue` | 阶段三 |
| 新建 | `src/components/home/TechStack.vue` | 阶段四 |
| 新建 | `src/components/home/AnimatedCounter.vue` | 阶段四 |
| 新建 | `src/components/home/DataCounters.vue` | 阶段四 |
| 新建 | `src/components/home/FaqSection.vue` | 阶段四 |
| 新建 | `src/components/home/CtaSection.vue` | 阶段五 |
| 新建 | `src/components/home/AppFooter.vue` | 阶段五 |
| 新建 | `src/components/effects/ParticleBackground.vue` | 阶段五 |
| 修改 | `src/views/home.vue` | 阶段一~五（逐步替换） |

共 **5 个阶段、18 个任务、16 个文件变更**。
