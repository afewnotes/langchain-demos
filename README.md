# langchain-demos

> 一套「从入门到实战」的 LangChain / RAG 中文教程与应用脚本，帮助你在本地快速搭建向量检索、Chainlit 应用和 ReAct 智能体。

## 目录
- [项目简介](#项目简介)
- [核心亮点](#核心亮点)
- [技术栈与依赖](#技术栈与依赖)
- [快速开始](#快速开始)
- [学习路径（Jupyter 笔记本）](#学习路径jupyter-笔记本)
- [应用脚本与使用场景](#应用脚本与使用场景)
- [目录导航](#目录导航)
- [系统流程图](#系统流程图)
- [环境变量配置](#环境变量配置)
- [常见问题与故障排除](#常见问题与故障排除)

## 项目简介
`langchain-demos` 通过 5 个循序渐进的 Jupyter 笔记本（01–05）与 2 个可运行脚本（06–07），完整演示了一个 RAG（Retrieval-Augmented Generation）系统从数据加载、向量化、检索优化到产品化落地（Chainlit UI、ReAct Agent）的全过程。适合：

- **初学者**：快速理解 LangChain 与 LangGraph 的核心概念
- **实践者**：直接借鉴向量数据库、混合检索、Chainlit、智能体工具链的落地模板
- **团队共享**：通过 `.env-example`、`uv.lock` 和结构化的 README，复刻一致的开发环境

## 核心亮点
1. 📒 **学习路径清晰**：每个 Notebook 对应 RAG 架构中的一个关键步骤，逐层递进。
2. 🧠 **多模型支持**：内置 DeepSeek、Qwen 等 OpenAI 兼容大模型，可平滑切换供应商。
3. 🧱 **可持久化向量库**：使用 Chroma + Qwen Embeddings，将 PDF 知识库保存到 `./files/pdf_vectordb`。
4. 💬 **即用型应用**：06 提供 Chainlit 对话机器人，07 展示带 Tavily 搜索与 Python REPL 的 ReAct Agent。
5. 🛠️ **现代依赖管理**：基于 `uv`，安装快、锁版本、兼容本仓库的 Python 3.12 环境。

## 技术栈与依赖
- **核心框架**：LangChain (core/community/experimental)、LangGraph、Chainlit
- **模型与服务**：DeepSeek、Qwen、OpenAI 兼容 API、LangSmith 追踪
- **检索相关**：Chroma、Qwen3 Embedding、Rank-BM25、sentence-transformers、metadata filtering
- **工具与集成**：Tavily Search、Python REPL、BeautifulSoup4、PyPDF、LangChain MCP Adapters
- **运行环境**：Python ≥ 3.12、`uv` 包管理、Jupyter Lab

> 完整依赖见 [`pyproject.toml`](./pyproject.toml) 与 `uv.lock`（已锁定版本，方便复现）。

## 快速开始
### 1. 环境准备
1. 安装 [uv](https://docs.astral.sh/uv/getting-started/):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
2. 确认 Python 3.12：`uv python list`，必要时执行 `uv python install 3.12`。
3. 复制环境变量模板并填写：
   ```bash
   cp .env-example .env
   # 编辑 .env，填入 OpenAI/DeepSeek/Tavily/LangSmith 等密钥
   ```

### 2. 安装依赖
```bash
uv sync
```
`uv` 会根据 `pyproject.toml` + `uv.lock` 创建隔离环境并安装所有依赖。

### 3. 运行 Jupyter Lab（适合学习笔记本 01–05）
```bash
uv run jupyter lab
```
- 在浏览器打开的 Jupyter Lab 中按顺序运行 `01`→`05` 笔记本。
- 建议在 `05_rag_pdf_robot.ipynb` 中完成 PDF 向量库的构建，以供 Chainlit 应用复用。

### 4. 运行 Chainlit PDF 问答助手
```bash
uv run chainlit run 06_chainlit.py --host 0.0.0.0 --port 8000
```
- 依赖 `./files/pdf_vectordb` 中的持久化向量库；若目录不存在，请先执行 Notebook 03/05 生成。
- 默认模型：`deepseek-ai/DeepSeek-V3`，可在 `.env` 中切换。
- 欢迎界面文案在 `chainlit.md` 中可随时调整。

### 5. 运行 ReAct 智能体示例
```bash
uv run python 07_react.py
```
- 需在 `.env` 中配置 `OPENAI_API_KEY`、`OPENAI_API_BASE`、`TAVILY_API_KEY`。
- Agent 会演示「联网搜索」「Python 计算」等多轮推理流程，可替换 `question*` 以测试自定义问题。

## 学习路径（Jupyter 笔记本）
| 笔记本 | 主题 | 关键内容 |
| --- | --- | --- |
| `01_langchain_basics.ipynb` | LangChain 入门 | 模型封装、提示词模板、链式调用、LangGraph 简介 |
| `02_document_loading_and_splitting.ipynb` | 数据摄取 | PDF / 网页加载、分段策略、文本清洗、元数据管理 |
| `03_vectorization_and_retrieval.ipynb` | 向量化与检索 | Qwen Embeddings、Chroma 建库、检索评估、Hybrid/BM25 |
| `04_rag_retrieval_optimization.ipynb` | 检索优化 | rerank、metadata filter、top-k 调优、召回对比 |
| `05_rag_pdf_robot.ipynb` | PDF QA 机器人 | ConversationalRetrievalChain、记忆、引用来源、向量库持久化 |

> 建议顺序执行并在每一步保存中间产物（如拆分后的文档、持久化向量库），方便后续应用直接复用。

## 应用脚本与使用场景
- **`06_chainlit.py`｜PDF 问答助手**
  - 调用 Chroma 持久化向量库，构建带记忆的 `ConversationalRetrievalChain`。
  - Chainlit 会话界面自动展示参考文档来源；适合演示企业知识库助手。
- **`07_react.py`｜ReAct 智能体**
  - 集成 Tavily 搜索 + Python REPL 工具，创建具备「思考-行动-观察」循环的 Agent。
  - 可扩展更多工具（数据库、内部 API 等）以应对复杂任务。

## 目录导航
```text
.
├── 01_langchain_basics.ipynb             # LangChain 基础
├── 02_document_loading_and_splitting.ipynb
├── 03_vectorization_and_retrieval.ipynb
├── 04_rag_retrieval_optimization.ipynb
├── 05_rag_pdf_robot.ipynb               # PDF QA 机器人
├── 06_chainlit.py                       # Chainlit 前端
├── 07_react.py                          # ReAct 智能体
├── chainlit.md                          # Chainlit 欢迎页
├── .env-example                         # 环境变量模板
├── pyproject.toml / uv.lock             # 依赖与版本锁
└── README.md
```
> 如需自定义数据或模型，建议在 `files/` 目录下新增对应子目录，便于持久化与版本控制。

## 系统流程图
```mermaid
flowchart LR
    A[PDF / 网页 / 其他数据源] --> B[加载与分割<br>(Notebook 02)]
    B --> C[向量化 + 入库<br>(Notebook 03, Chroma + Qwen)]
    C --> D[检索优化<br>(Notebook 04: Hybrid / Rerank / Filter)]
    D --> E[RAG 生成
(Notebook 05 / Chainlit)]
    E --> F[应用层
Chainlit UI / ReAct Agent]
```

## 环境变量配置
根据 `.env-example`，常用字段如下：
- `OPENAI_API_KEY` / `OPENAI_API_BASE`：DeepSeek、Qwen、OpenAI 等兼容服务的密钥与 Base URL。
- `TAVILY_API_KEY`：ReAct Agent 联网搜索所需。
- `LANGSMITH_*`：如需启用 LangSmith 追踪、链路分析，可保持默认或替换为自有项目。

> 建议使用 `.env` 管理敏感信息，`uv run ...` 会自动加载；如需在 Notebook 中使用，请在首个单元加载 `python-dotenv` 或通过系统环境变量传递。

## 常见问题与故障排除
1. **运行 `uv` 报 "command not found"？** 
   - 确保已执行安装脚本，并将 `$HOME/.local/bin` 加入 `PATH`。
2. **Chainlit 报错找不到 `./files/pdf_vectordb`？**
   - 先执行 Notebook 03 或 05，确认调用 `Chroma(persist_directory="./files/pdf_vectordb")` 后执行 `persist()`。
3. **调用 LLM 返回 401/429？**
   - 检查 `.env` 中密钥是否正确且有额度，可尝试更换模型或在代码中调低并发。
4. **Tavily 搜索失败或 Agent 阻塞？**
   - 确认已设置 `TAVILY_API_KEY`，并检查网络是否可访问 Tavily 服务。
5. **Jupyter 无法启动或内核版本不符？**
   - 使用 `uv run jupyter lab`，确保当前 shell 位于项目根目录并加载了 `uv` 创建的虚拟环境。

---
现在就启动 `uv run jupyter lab`，沿着 Notebook 学习路径完成你的第一个中文 RAG Demo 吧！若对 Chainlit 欢迎页或 Agent 工具链有新的想法，也可以直接修改对应脚本快速验证。祝开发顺利 🚀
