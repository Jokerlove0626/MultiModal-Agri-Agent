# (Agri-Doctor) 全栈 API 交付手册
版本: v1.0.0

基础 URL: http://127.0.0.1:8000

全局前缀: /api

通信协议: HTTP/1.1

数据格式: JSON (除图片上传外)

🛠️ 全局配置说明
跨域支持 (CORS): 后端已开启全域名允许，前端本地开发（如 localhost:5173）可直接调用。

状态维护: 引擎采用全局单例模式挂载在 app.state，首次调用时若模型在加载中，响应时间可能略长（约 1-3s）。

## 1. 🤖 智能诊断模块 (/chat)
### 1.1 纯文本问答接口
基于 GraphRAG 双引擎的专业农业咨询。

URL: /api/chat/

Method: POST

Payload:

JSON
{
  "query": "香蕉叶子发黄且有褐色斑点是什么病？",
  "session_id": "optional_string_for_context"
}
Response:

JSON
{
  "status": "success",
  "answer": "根据您的描述，这可能是**香蕉叶斑病**。推荐防治措施如下：\n\n1. **农业防治**：及时清除病残叶...\n2. **化学防治**：使用XX药剂..."
}
### 1.2 多模态视觉诊断接口
上传病害照片进行智能识别与知识图谱联合诊断。

URL: /api/chat/identify

Method: POST

Content-Type: multipart/form-data

Body (FormData):
| 参数名 | 类型 | 是否必填 | 说明 |
| :--- | :--- | :--- | :--- |
| file | File (Binary) | 是 | 拍摄的病害图片 (jpg/png) |
| crop_name | String | 否 | 农作物名称，有助于提高精度 |
| user_text | String | 否 | 用户补充的文字描述 |
| session_id | String | 否 | 会话 ID |

Response: 返回识别出的病害名称、诊断逻辑及防治方案。

## 2. 🕸️ 知识图谱大屏可视化 (/graph)
### 2.1 大屏专用图谱数据提取
专为 ECharts / D3 / G6 等力引导图组件定制的数据接口。

URL: /api/graph/visualize

Method: GET

Params:

disease_name (String, 可选): 模糊查询特定病害及其关联。

limit (Int, 默认150): 限制返回节点数。

Data Structure:

JSON
{
  "status": "success",
  "data": {
    "nodes": [
      {
        "id": "disease_6",
        "name": "香蕉冠腐病",
        "category": "病害",
        "symbolSize": 50,
        "detail": { "summary": "...", "chemical": "...", "biological": "..." }
      },
      { "id": "crop_香蕉", "name": "香蕉", "category": "农作物", "symbolSize": 80 }
    ],
    "links": [
      { "source": "disease_6", "target": "crop_香蕉", "label": "属于" }
    ]
  }
}
💡 前端渲染建议：

后端已计算好 symbolSize（作物 80，病害 50），请直接绑定。

category 字段建议映射不同的节点颜色。

点击“病害”节点时，请展示 detail 内的富文本内容。

## 3. 📚 知识库管理后台 (/knowledge)
### 3.1 动态知识入库
管理员手动添加新病害知识，系统会自动同步至向量库（模糊检索）和图谱库（精准推理）。

URL: /api/knowledge/add

Method: POST

Payload:

JSON
{
  "disease_name": "草莓炭疽病",
  "symptom": "果实出现黑色凹陷...",
  "treatment": "喷施嘧菌酯...",
  "admin_token": "super_joker_2024"
}
⚠️ 异常处理规范
系统统一使用 FastAPI 异常响应格式，HTTP 状态码如下：

200: 请求成功。

400: 参数校验失败（如图片格式不符）。

403: 管理员 Token 错误。

500: 服务器内部错误（AI 引擎或数据库断联）。

错误响应示例:

JSON
{
  "detail": "AI引擎未就绪"
}
文档维护者: Jokerlove