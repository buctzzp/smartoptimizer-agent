# 智解 Agent：通用问题优化与求解智能体

## 1. 项目简介

**智解 Agent** 是一个面向通用问题的智能体应用。用户输入一个自然语言问题后，系统会自动完成问题理解、优化分析、工具调用、答案生成和自我检查，并导出 PDF 报告。

本项目区别于普通聊天机器人的核心在于：**LLM 自主驱动的 Agent 架构**。系统不预设固定的分析流水线，而是让 LLM 根据问题内容自行判断是否调用工具、调用哪些工具，最终生成完整的结构化优化报告。

## 2. 项目定位

本项目是一个 **通用问题求解 Agent**，而不是单一领域的算法优化工具。

系统的输入是一个自然语言问题。Agent 会自主决定如何分析问题、是否调用工具辅助分析，最终输出结构化答案。

"优化"体现在两个方面：

- 对用户输入的问题进行优化，使问题更加清晰、具体、适合求解；
- 对求解过程和最终答案进行优化，使输出结果更加结构化、可执行、可检查。

## 3. 技术栈

| 技术 | 作用 |
|------|------|
| Python | 项目主开发语言 |
| Gradio | 构建单页面 Web 交互界面，支持流式输出 |
| Anthropic SDK | 调用 DeepSeek API 的 streaming 接口 |
| DeepSeek | 大模型推理能力 |
| markdown-pdf | 将 Markdown 直接转换为 PDF 报告 |
| ModelScope 魔搭创空间 | 在线部署并提供公开访问链接 |

## 4. 架构

### Agent 工作流程

```text
用户输入
    ↓
LLM 接收问题（System Prompt + User Message）
    ↓
LLM 流式生成完整的 9 段结构化优化分析
    ↓
网页实时显示流式输出（token-by-token）
    ↓
用户点击「生成 PDF 报告」按钮
    ↓
生成 PDF 并提供下载
```

架构特点：**纯流式架构**，不预设固定流水线，不强制工具调用。LLM 全权负责分析，PDF 生成由用户手动触发。

### 工具列表

| 工具 | 作用 | 触发方式 |
|------|------|----------|
| `generate_pdf` | 将完整报告保存为 PDF 文件 | 用户点击「生成 PDF 报告」按钮 |

PDF 生成作为 UI 功能按钮存在，不由 LLM 自动调用，避免打断流式输出体验。

## 5. 项目结构

```text
smartoptimizer-agent/
├── app.py              # Gradio 网页入口
├── agent.py            # 纯流式 LLM 调用
├── llm_client.py       # DeepSeek API 客户端（Anthropic SDK）
├── prompts.py          # 系统提示词
├── tools.py            # 工具定义：generate_pdf + CJK 字体 CSS
├── setup.sh            # ModelScope 部署系统依赖安装脚本
├── requirements.txt    # 项目依赖（版本锁定）
├── .gitignore          # 排除 .env、__pycache__ 等
├── CLAUDE.md           # Claude Code 项目指引
├── README.md           # 项目说明文档
└── outputs/
    └── reports/        # 生成的 PDF 报告
```

## 6. 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `ANTHROPIC_API_KEY` | DeepSeek API Key（兼容 Anthropic SDK） | 必填，也支持 `DEEPSEEK_API_KEY` 作为后备 |
| `ANTHROPIC_BASE_URL` | API 地址 | `https://api.deepseek.com/anthropic` |
| `ANTHROPIC_MODEL` | 模型名称 | `deepseek-chat` |

## 7. 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量（创建 .env 文件或 export）
export DEEPSEEK_API_KEY="你的 DeepSeek API Key"

# 启动应用
python app.py
```

启动后浏览器访问 Gradio 本地页面（默认 `http://127.0.0.1:7860`）。

## 8. 部署到 ModelScope

1. 注册并登录 ModelScope（魔搭社区）；
2. 创建新的创空间，选择 **Gradio** 应用类型；
3. 上传项目代码（确保 `.env` **不**被上传，已通过 `.gitignore` 排除）；
4. 在 ModelScope 平台后台 → 环境变量 → 配置 `ANTHROPIC_API_KEY`，值为你的 DeepSeek API Key；
5. 平台会自动安装 `requirements.txt` 中的依赖并启动应用；
6. 首次部署建议手动执行 `bash setup.sh`（通过平台的自定义启动命令）以安装 CJK 字体确保 PDF 中文正常渲染。

### ModelScope 部署注意事项

| 项目 | 说明 |
|------|------|
| 字体支持 | Linux 默认无 CJK 字体，需自行安装 `fonts-noto-cjk`（由 `setup.sh` 处理） |
| API Key | 通过平台环境变量配置，**切勿**写在代码或 `.env` 中上传 |
| 启动后 | 平台会提供一个公开可访问的链接 |

## 9. 安全设计

- **API Key 保护**：通过平台环境变量注入，不对最终用户暴露
- 不执行用户提交的代码
- 不开放 Bash 命令执行
- 不开放任意文件读写权限
- 不允许用户直接操作服务器环境
- PDF 生成由后端固定函数完成
- 工具调用范围保持最小化
- 用户输入只作为问题文本处理，不作为可执行指令运行
