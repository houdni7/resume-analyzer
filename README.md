# AI Resume Analyzer

基于阿里通义千问的智能简历解析与岗位匹配平台。上传 PDF 简历，AI 自动提取关键信息，支持岗位匹配度评分。

**在线体验:** https://houdni7.github.io/resume-analyzer/

## 技术栈

| 层 | 技术 |
|---|---|
| 后端 | Python FastAPI |
| AI | 通义千问 DashScope (qwen-plus) |
| PDF 解析 | pypdf |
| 部署 | 阿里云函数计算 FC3 (Serverless) |
| 前端 | React + Vite + Tailwind CSS |
| 前端部署 | GitHub Pages |

## 项目结构

```
resume-analyzer/
├── backend/
│   ├── main.py              # FastAPI + FC3 handler (ASGI 桥接)
│   ├── config.py            # 环境变量配置
│   ├── requirements.txt     # Python 依赖
│   ├── s.yaml               # FC3 部署配置 (Serverless Devs)
│   ├── Dockerfile           # 容器镜像构建
│   ├── models/schemas.py    # Pydantic 数据模型
│   ├── routers/
│   │   ├── resume.py        # 简历上传 / 分析 / 查询
│   │   └── match.py         # 岗位匹配评分
│   └── services/
│       ├── parser.py        # PDF 文本提取 + 分段
│       ├── extractor.py     # AI 关键信息提取
│       ├── scorer.py        # 规则 + AI 双重评分
│       └── cache.py         # 缓存层 (Redis 可选)
├── frontend/
│   └── src/
│       ├── api/index.ts     # Axios API 封装
│       ├── components/      # React 组件
│       └── types/           # TypeScript 类型
├── build_zip.py             # FC3 部署打包脚本
└── .github/workflows/       # CI/CD
```

## 快速启动

### 1. 后端 (本地开发)

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env          # 编辑 .env 填入 DASHSCOPE_API_KEY
python main.py                # http://localhost:8000
```

不配置 API Key 也能运行，会使用规则降级匹配。

### 2. 前端

```bash
cd frontend
npm install
npm run dev                   # http://localhost:5173
```

## API 接口

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/api/resume/upload` | 上传 PDF 简历 (multipart/form-data, field: `file`) |
| POST | `/api/resume/{id}/analyze` | AI 解析简历关键信息 |
| POST | `/api/match` | 岗位匹配评分 `{"resume_id":"...","job_description":"..."}` |
| GET | `/api/resume/{id}` | 查询简历及分析结果 |
| GET | `/api/health` | 健康检查 |
| GET | `/api/ping` | 连通性测试 |

## 部署

### 后端 → 阿里云 FC3

1. 在 [阿里云 FC3 控制台](https://fc.console.aliyun.com/) 创建函数
   - 运行时: `python3.10`
   - 处理器: `main.handler`
   - 内存: 512 MB+
   - 超时: 120s
2. 配置环境变量 `DASHSCOPE_API_KEY`
3. 创建 HTTP 触发器 (匿名访问)
4. 运行 `python build_zip.py` 打包，上传到控制台
5. 发布版本使函数 URL 生效

### 前端 → GitHub Pages

Push 到 `main` 分支自动部署，需在仓库 Settings > Secrets and variables > Actions 中配置 `VITE_API_BASE_URL` 为 FC3 函数 URL。

## 部署关键问题

FC3 Python 3.10 不会自动 `pip install`。本项目通过 `pip download --platform manylinux2014_x86_64 --python-version 310` 预下载 Linux wheel 并打入部署包。

**核心坑位:**
1. **事件格式:** FC3 HTTP 触发器传入 `bytes` 而非 `dict`，需 `json.loads` 解码
2. **Header 大小写:** ASGI 规范要求 header 名小写，FC3 传入的可能保留原样
3. **打包路径:** Windows `Compress-Archive` 用反斜杠，需用 Python `zipfile` 确保正斜杠
4. **隐式依赖:** anyio 依赖 `sniffio`、`exceptiongroup` 等，pip download 可能遗漏

## 费用

| 服务 | 费用 |
|---|---|
| FC3 函数计算 | 免费额度 100 万次调用/月，个人使用完全免费 |
| 通义千问 API | 新用户 100 万 token 免费额度，qwen-plus ~0.002 元/千 token |
| GitHub Pages | 免费 |

**结论: 零成本运行。**
