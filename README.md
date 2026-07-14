# AI 智能简历分析系统

基于阿里通义千问的智能简历解析与岗位匹配平台。上传 PDF 简历，AI 自动提取关键信息，支持岗位匹配度评分。

## 技术栈

| 层 | 技术 |
|---|---|
| 后端 | Python FastAPI |
| AI | 阿里通义千问 DashScope (qwen-plus) |
| PDF 解析 | PyMuPDF |
| 缓存 | Redis (可选) |
| 部署 | 阿里云函数计算 FC (Serverless Devs) |
| 前端 | React + Vite + Tailwind CSS |
| 前端部署 | GitHub Pages |

## 项目结构

```
resume-analyzer/
├── backend/
│   ├── main.py              # FastAPI 入口 + FC handler
│   ├── config.py            # 环境变量配置 (.env 自动加载)
│   ├── s.yaml               # Serverless Devs 部署配置
│   ├── models/schemas.py    # Pydantic 数据模型
│   ├── routers/
│   │   ├── resume.py        # POST /api/resume/upload | analyze | GET
│   │   └── match.py         # POST /api/match
│   └── services/
│       ├── parser.py        # PDF 文本提取 + 清洗分段
│       ├── extractor.py     # AI 关键信息提取 (通义千问)
│       ├── scorer.py        # 双重评分：规则匹配 + AI 智能评分
│       └── cache.py         # Redis 缓存 (MD5 key, TTL 3600s)
└── frontend/
    ├── src/
    │   ├── api/index.ts     # Axios API 封装
    │   ├── components/
    │   │   ├── Uploader.tsx  # 拖拽上传组件
    │   │   ├── ResultCard.tsx # 简历分析结果卡片
    │   │   └── Matcher.tsx   # 岗位匹配 + 可视化评分
    │   └── types/index.ts   # TypeScript 类型定义
    └── .github/workflows/deploy.yml  # GitHub Pages 自动部署
```

## 快速启动

### 1. 后端

```bash
cd backend
cp .env.example .env          # 编辑 .env 填入 DASHSCOPE_API_KEY
pip install -r requirements.txt
python main.py                # 启动 http://localhost:8000
```

不配置 API Key 也能运行，会使用规则降级匹配。

### 2. 前端

```bash
cd frontend
npm install
npm run dev                   # 启动 http://localhost:5173
```

## API 接口

### 上传简历
`POST /api/resume/upload`
- Content-Type: multipart/form-data
- Body: file (PDF)

### AI 分析
`POST /api/resume/{resume_id}/analyze`

### 岗位匹配
`POST /api/match`
```json
{
  "resume_id": "uuid",
  "job_description": "招聘 Java 后端工程师..."
}
```

### 查询简历
`GET /api/resume/{resume_id}`

## 评分机制

采用**双重评分**策略：

1. **规则匹配**（基准分）：JD 与简历的关键词重合率 × 维度权重
   - 技能匹配 35% + 经验相关 30% + 学历匹配 15% + 项目契合 20%

2. **AI 智能评分**（加分项）：通义千问基于 JD 和简历内容生成评语

AI 不可用时自动降级为纯规则评分。

## 缓存策略

- Key 格式：`resume:md5:{简历文本MD5}:{suffix}`
- TTL：3600 秒
- 同一份简历 + 同一 JD 不重复调用 AI
- Redis 不可用时自动降级（不影响功能）

## 部署

### 后端 → 阿里云 FC
```bash
s deploy
```

### 前端 → GitHub Pages
Push 到 main 分支自动部署，访问 `https://{username}.github.io/resume-analyzer/`
