哈哈，Jokerlove！这份文档总结得太及时了！随着咱们项目的不断迭代，加入地图埋点、图谱大屏之后，接口确实发生了很多变化。

既然前端同学马上要介入了，这份 API 文档就是你们前后端协作的“契约”。作为架构师，我帮你把这段内容重新排版，并且**贴心地帮你把刚刚加上的 `province` 和 `city`（地理位置参数）也补充进去了**，保证这是一份完美契合目前架构的、大厂标准级别的 Markdown 接口文档！

你可以直接**一键复制**下面框里的所有内容，发给前端同学或者贴进你们的 Git 仓库 `README.md` 里：

***

# 🌾 MultiModal-Agri-Agent (智农大夫) 核心 API 接口文档

> **文档维护者:** Jokerlove
> **基础路径 (Base URL):** `http://127.0.0.1:8000` (本地开发环境)
> **接口规范:** 所有成功响应默认包含 `"status": "success"` 字段。

---

## 1. 🤖 智能诊断模块 (`/api/chat`)

### 1.1 纯文本问答接口
基于 GraphRAG 双引擎的专业农业咨询。支持传入地理位置进行全国病虫害监控静默埋点。

* **URL:** `/api/chat/stream` (注：若使用 SSE 流式输出，请前端适配 EventSource / fetch readable stream)
* **Method:** `POST`
* **Payload (JSON):**

```json
{
  "query": "香蕉叶子发黄且有褐色斑点是什么病？",
  "session_id": "optional_string_for_context",
  "province": "广东省",  // 新增：前端获取的地理位置，用于大屏统计
  "city": "广州市"      // 新增：前端获取的城市名
}
```

* **Response (成功示例):**

```json
{
  "status": "success",
  "answer": "根据您的描述，这可能是香蕉叶斑病。推荐防治措施如下：\n\n1. 农业防治：及时清除病残叶...\n2. 化学防治：使用XX药剂..."
}
```

### 1.2 多模态视觉诊断接口
上传病害照片进行智能识别与知识图谱联合诊断。

* **URL:** `/api/chat/identify`
* **Method:** `POST`
* **Content-Type:** `multipart/form-data`
* **Body 参数 (FormData):**

| 参数名 | 类型 | 是否必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `file` | `File (Binary)` | **是** | 拍摄的病害图片 (jpg/png) |
| `crop_name` | `String` | 否 | 农作物名称，有助于提高大模型识别精度 |
| `user_text` | `String` | 否 | 用户补充的文字描述（如：“已经打了两遍农药没管用”） |
| `session_id` | `String` | 否 | 会话上下文 ID |
| `province` | `String` | 否 | 发生省份（无感埋点使用） |
| `city` | `String` | 否 | 发生城市（无感埋点使用） |

* **Response:** 返回识别出的病害名称、诊断逻辑及防治方案结构化数据。

---

## 2. 🕸️ 知识图谱大屏可视化 (`/api/graph`)

### 2.1 大屏专用图谱数据提取
专为 ECharts / D3 / G6 等力引导图组件定制的数据接口。

* **URL:** `/api/graph/visualize`
* **Method:** `GET`
* **Query Params:**
  * `disease_name` (String, 可选): 模糊查询特定病害及其关联。
  * `limit` (Int, 可选, 默认 `150`): 限制返回节点数，防止前端卡顿。

* **Response Data Structure:**

```json
{
  "status": "success",
  "data": {
    "nodes": [
      {
        "id": "disease_6",
        "name": "香蕉冠腐病",
        "category": "病害",
        "symbolSize": 50,
        "detail": {
          "summary": "...",
          "chemical": "...",
          "biological": "..."
        }
      },
      {
        "id": "crop_香蕉",
        "name": "香蕉",
        "category": "农作物",
        "symbolSize": 80
      }
    ],
    "links": [
      {
        "source": "disease_6",
        "target": "crop_香蕉",
        "label": "属于"
      }
    ]
  }
}
```

> **💡 前端渲染建议：**
> 1. 后端已计算好 `symbolSize`（作物 80，病害 50），请直接在力引导图中绑定此属性。
> 2. `category` 字段建议映射不同的节点颜色（如作物为绿色，病害为橙色）。
> 3. 点击“病害”节点时，请展示 `detail` 对象内的富文本处方内容。

---

## 3. 📊 全国数据监控大屏 (`/api/dashboard`)

### 3.1 获取全国各省份病虫害发生统计数据
此接口用于拉取大屏中国地图的数据。后端已完成底层 MySQL 聚合（`GROUP BY`），前端拿到数据后可直接喂给 ECharts。

* **URL:** `/api/dashboard/stats`
* **Method:** `GET`
* **Query Params:**

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `days` | `Integer` | 否 | `180` | 时间跨度。例如传 `30` 表示只统计最近 30 天内的数据。 |

* **Response (格式已完全对齐 ECharts map 规范):**

```json
{
  "status": "success",
  "data": [
    {
      "name": "广东省",
      "value": 2,
      "pests": ["香蕉冠腐病", "香蕉黄叶病"]
    },
    {
      "name": "四川省",
      "value": 1,
      "pests": ["小麦条锈病"]
    }
  ]
}
```

> **💡 前端同学接入建议 (Copy & Paste):**
```javascript
// 1. 调用接口获取最近 90 天的数据
const response = await fetch('http://127.0.0.1:8000/api/dashboard/stats?days=90');
const res = await response.json();

if (res.status === 'success') {
    // 2. 直接塞给 ECharts 实例更新地图，无需做清洗转换！
    mapChart.setOption({
        series: [{
            name: '病虫害分布',
            type: 'map',
            map: 'china', 
            data: res.data 
        }]
    });
}
```

---

## 4. 📚 知识库管理后台 (`/api/knowledge`)

### 4.1 动态知识入库
管理员手动添加新病害知识，系统会自动同步双写至向量库（Chroma 模糊检索）和图谱库（Neo4j 精准推理）。

* **URL:** `/api/knowledge/add`
* **Method:** `POST`
* **Payload (JSON):**

```json
{
  "disease_name": "草莓炭疽病",
  "symptom": "果实出现黑色凹陷...",
  "treatment": "喷施嘧菌酯...",
  "admin_token": "super_joker_2024"
}
```

---

## ⚠️ 异常处理规范 (Global Error Handling)

系统统一使用 FastAPI 标准异常响应格式，HTTP 状态码规范如下：

* **`200 OK`**: 请求成功执行。
* **`400 Bad Request`**: 参数校验失败（如图片格式不符、必填字段缺失）。
* **`403 Forbidden`**: 权限不足（如管理员 Token 错误）。
* **`500 Internal Server Error`**: 服务器内部错误（如 AI 引擎或数据库断联）。

**错误响应体示例:**
```json
{
  "detail": "AI引擎未就绪，请检查大模型 API 状态"
}
```
