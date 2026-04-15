# 🤖 AI 数据分析助手

一个基于 **LangChain + DeepSeek + Pandas** 构建的智能数据分析工具。用户只需上传 Excel/CSV 数据文件，用自然语言提出分析需求，AI 会自动生成 Python 代码、执行分析并生成可视化图表。

## ✨ 功能特点

- 📁 **多格式支持**：支持 CSV、Excel（.xlsx/.xls）文件上传
- 🗣️ **自然语言交互**：用中文描述你的分析需求即可，无需编写代码
- 🤖 **AI 自动编程**：基于 LangChain + DeepSeek 大模型，自动生成分析代码
- 📊 **自动可视化**：自动生成折线图、柱状图、饼图、散点图等多种图表
- 🧠 **智能洞察**：一键生成数据整体洞察报告
- 💻 **代码可追溯**：可展开查看 AI 生成的 Python 代码

## 🎯 支持的分析类型

| 类型 | 示例 |
|------|------|
| 数据统计 | "各产品的平均单价？" "上个月的总销售额？" |
| 趋势分析 | "画一个各月销售额的折线图" |
| 对比分析 | "按区域分组统计销售额并画柱状图" |
| 分布分析 | "用饼图展示各产品销量占比" |
| 相关性分析 | "数量和利润的关系？" |
| 数据洞察 | "帮我总结这份数据的关键趋势" |

## 🛠️ 技术栈

| 组件 | 技术 |
|------|------|
| LLM 大模型 | DeepSeek（通过 LangChain 调用） |
| AI 编排框架 | LangChain |
| 数据处理 | Pandas + NumPy |
| 数据可视化 | Matplotlib |
| Web 界面 | Streamlit |
| 运行环境 | Python 3.13+ |

## 📁 项目结构

```
ai-data-analyzer/
├── app.py                    # Streamlit Web 前端界面
├── data_engine.py            # 核心引擎（AI 代码生成、执行、图表渲染）
├── generate_sample_data.py   # 示例数据生成脚本
├── requirements.txt          # Python 依赖
├── .env.example              # 环境变量模板
├── 启动应用.bat              # Windows 一键启动脚本
├── sample_data/              # 示例数据目录
│   └── 2025年销售数据.xlsx
└── README.md
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 API Key

复制 `.env.example` 为 `.env`，填入你的 DeepSeek API Key：

```env
DEEPSEEK_API_KEY=sk-your-api-key-here
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

> 💡 前往 [DeepSeek 开放平台](https://platform.deepseek.com/) 注册并获取 API Key

### 3. 运行

```bash
streamlit run app.py
```

或者直接双击 `启动应用.bat`（Windows）。

浏览器会自动打开 `http://localhost:8501`。

## 🔄 工作流程

```
用户上传数据文件 → AI 理解数据结构 → 用户自然语言提问
       ↓
AI 生成 Python 分析代码 → 安全沙箱执行代码 → 返回图表 + 文字结论
```

### 核心流程说明

1. **数据加载**：用户上传文件后，系统自动解析并生成数据概览（列名、类型、统计信息）
2. **代码生成**：将数据概览和用户问题一起发送给 DeepSeek，AI 生成完整的 Python 分析代码
3. **代码执行**：在隔离环境中执行生成的代码，捕获 print 输出和生成的图表
4. **结果展示**：在 Web 界面展示图表、分析结论，并可展开查看生成的代码

## 📄 License

MIT License
