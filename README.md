# 📊 AI 数据分析助手 | AI Data Analysis Assistant

> [中文](#中文) | [English](#english)

---

<a id="中文"></a>
## 🇨🇳 中文

> 智能数据分析工具，将 LLM 驱动的分析洞察与程序化数据处理结合。上传数据，用自然语言提问，同时获得 AI 分析和可执行的 Python 图表。

![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-red?logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-0.3+-green?logo=chainlink)
![DeepSeek](https://img.shields.io/badge/DeepSeek-API-blue)
![pandas](https://img.shields.io/badge/pandas-2.0+-blue?logo=pandas)
![matplotlib](https://img.shields.io/badge/matplotlib-3.8+-orange)

### 🎯 应用场景

**业务场景：**
- **销售分析** — 上传月度/季度销售 Excel，问"哪个产品增长最高？"或"各区域销售对比"
- **财务报表** — 加载财务数据，让 AI 识别趋势、异常和关键指标
- **KPI 监控** — 导入团队绩效数据，即时获取汇总、异常值和目标进度
- **调查问卷分析** — 上传调查结果，获取情感分布、人群相关性分析

**个人场景：**
- **个人记账** — 导入消费记录，AI 自动分类、找省钱机会、可视化月度趋势
- **健身健康数据** — 分析运动日志、睡眠数据，找规律和优化建议
- **学术研究** — 处理实验数据，生成统计摘要和发表级图表

### ✨ 功能特性

- 📁 **Excel/CSV 上传** — 拖拽上传数据文件（`.xlsx`、`.csv`、`.xls`）
- 📊 **自动数据概览** — 即时展示行数、列类型、缺失值、基础统计
- 💬 **自然语言问答** — 用中文或英文问任何关于数据的问题
- 🤖 **AI 驱动分析** — DeepSeek 识别趋势、异常值和规律，并详细解释
- 📈 **自动生成图表** — AI 自动写 Python 代码，用 matplotlib 生成可视化
- 💾 **内置示例数据** — 自带销售数据集，开箱即用

### 💬 你可以这样问

- "哪个月份的销售额最高？增长趋势如何？"
- "各个产品类别的销售占比是多少？画个饼图"
- "找出销售额异常的月份，分析可能的原因"
- "对比不同区域的销售表现，生成柱状图"
- "总结这份数据的关键发现和业务建议"

### 🏗️ 系统架构

```
┌─────────────────────────────────────────────────┐
│              Streamlit Web UI                    │
│  ┌──────────┐  ┌───────────┐  ┌─────────────┐  │
│  │  上传数据 │  │   对话问答 │  │  图表展示    │  │
│  └────┬─────┘  └─────┬─────┘  └──────┬──────┘  │
└───────┼──────────────┼────────────────┼─────────┘
        │              │                │
┌───────▼──────────────▼────────────────▼─────────┐
│                 数据引擎                           │
│  ┌──────────────┐  ┌──────────────────────────┐ │
│  │  pandas      │  │  LangChain + DeepSeek    │ │
│  │  (数据处理)  │  │  (分析 Agent)            │ │
│  └──────────────┘  └──────────────────────────┘ │
└─────────────────────────────────────────────────┘
        │                          │
        ▼                          ▼
┌──────────────┐        ┌──────────────────────┐
│  Excel/CSV   │        │  DeepSeek API        │
│  数据文件     │        │  (代码生成 + 洞察)    │
└──────────────┘        └──────────────────────┘
```

### 📁 项目结构

```
ai-data-analyzer/
├── app.py                    # Streamlit Web 界面
├── data_engine.py            # 数据处理 + AI 分析引擎
├── generate_sample_data.py   # 生成示例数据集的脚本
├── requirements.txt          # Python 依赖
├── .env.example              # 环境变量模板
├── sample_data/
│   └── 2025年销售数据.xlsx   # 示例销售数据集
└── screenshots/              # UI 截图
```

### 🚀 快速开始

```bash
git clone https://github.com/SsllF8/ai-data-analyzer.git
cd ai-data-analyzer
python -m venv .venv && .venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp .env.example .env  # 填入 DEEPSEEK_API_KEY
streamlit run app.py
```

Windows 用户也可以直接双击 `启动应用.bat`。

### ⚙️ 环境变量配置

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `DEEPSEEK_API_KEY` | ✅ | DeepSeek API 密钥 |
| `DEEPSEEK_BASE_URL` | ❌ | API 地址（默认 `https://api.deepseek.com`） |

### 🛠️ 技术栈

| 组件 | 技术 | 用途 |
|------|------|------|
| Web 框架 | Streamlit | 数据可视化交互 UI |
| AI 框架 | LangChain | Agent 编排与工具绑定 |
| 大模型 | DeepSeek | 自然语言理解与代码生成 |
| 数据处理 | pandas | 数据加载、清洗、聚合 |
| 可视化 | matplotlib | 动态图表生成 |
| 文件解析 | openpyxl | Excel 文件读取 |

### 📖 工作原理

1. **数据加载** — pandas 读取 Excel/CSV 文件，生成统计概览
2. **用户提问** — 通过聊天界面用自然语言提问
3. **AI 分析** — LangChain Agent 接收数据 schema 和用户问题：
   - 生成 pandas 代码分析数据
   - 在沙箱环境中安全执行代码
   - 解释结果并生成可读的分析报告
   - 当用户要求可视化时，创建 matplotlib 图表
4. **结果展示** — 图表内嵌渲染，分析文字显示在聊天中

### 💡 项目亮点 / Project Highlights

**1. 为什么用 Agent 模式而不是写死分析逻辑？**
- Agent 模式下，AI 可以根据用户提问**动态生成**分析代码，不需要预先定义所有分析场景
- 用户可以问任何问题，不用受限于预设的"分析模板"
- 体现了 AI 的泛化能力——同一个工具处理无限种分析需求

**2. 代码执行安全性怎么保证？**
- 只允许 pandas 和 matplotlib 等安全库
- 可以通过 `exec()` 的沙箱化（限制 `__import__`、`os` 等危险模块）增强安全
- 生产环境中应使用容器隔离（如 Docker）执行生成的代码

**3. 为什么选 pandas 而不是直接让 AI 算？**
- AI 直接计算数值容易出错（浮点精度、大数溢出）
- pandas 是成熟的数据处理库，AI 生成 pandas 代码更可靠
- pandas 可以处理百万级数据，纯 LLM 无法做到

**4. 和传统 BI 工具（Tableau、Power BI）的区别？**
- 传统 BI 需要学习拖拽操作和 DAX/SQL 语法
- 本工具用自然语言交互，**零学习成本**
- 传统 BI 适合固定报表，本工具适合探索性分析（ad-hoc analysis）

### ⚠️ 搭建中可能遇到的问题 / Troubleshooting

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| AI 回答太长/太冗余 | LLM 未限制输出长度 | 在 prompt 中明确要求"简洁回答，不超过 200 字" |
| AI 生成的代码报错 | 模型生成了不存在的函数 | 增加错误重试机制，将错误信息反馈给 LLM 修正 |
| Excel 中文列名乱码 | pandas 默认编码检测不准 | 指定 `encoding='utf-8'` 或 `gbk` |
| 图表不显示 | matplotlib 中文字体缺失 | 设置 `plt.rcParams['font.sans-serif'] = ['SimHei']` |
| 大文件加载慢 | pandas 全量读入内存 | 对大文件用 `chunksize` 分块读取，或采样展示 |
| streamlit 上传后数据丢失 | Streamlit rerun 机制 | 用 `st.session_state` 缓存 DataFrame |

### 🚀 扩展方向 / Future Enhancements

- **支持更多数据源** — 接入数据库（MySQL、PostgreSQL）、API 接口
- **交互式图表** — 换用 Plotly 或 pyecharts，支持缩放、悬停提示
- **自然语言生成 SQL** — 接入 Text-to-SQL，直接查询数据库
- **自动报告生成** — 分析结果一键导出为 PDF/Word 报告
- **数据清洗助手** — AI 自动识别异常值、缺失值，建议清洗方案
- **定时分析任务** — 每天自动分析指定数据，推送变化趋势
- **多表关联** — 支持上传多个文件，AI 自动识别关联关系并 Join

---

<a id="english"></a>
## 🇬🇧 English

> An intelligent data analysis tool that combines LLM-powered insights with programmatic data processing. Upload your data, ask questions in natural language, and get both AI analysis and executable Python charts.

### Use Cases

**Business:**
- **Sales Analysis** — Upload sales data and ask "Which product had the highest growth?"
- **Financial Reporting** — Load financial statements and let AI identify trends and anomalies
- **KPI Monitoring** — Import performance data and get instant summaries and outlier detection
- **Survey Analysis** — Upload survey results for sentiment breakdowns and demographic correlations

**Personal:**
- **Personal Finance** — Import expense records and find savings opportunities
- **Fitness Data** — Analyze workout logs and sleep patterns
- **Academic Research** — Process experiment data and generate publication-quality charts

### Features

- 📁 **Excel/CSV Upload** — Drag and drop data files (`.xlsx`, `.csv`, `.xls`)
- 📊 **Auto Data Summary** — Instantly see row count, column types, missing values, basic statistics
- 💬 **Natural Language Q&A** — Ask anything about your data in plain English or Chinese
- 🤖 **AI-Powered Analysis** — DeepSeek identifies trends, outliers, and patterns
- 📈 **Auto Chart Generation** — AI writes Python code to create matplotlib visualizations
- 💾 **Sample Data Included** — Comes with a sample sales dataset

### Architecture

```
┌─────────────────────────────────────────────────┐
│              Streamlit Web UI                    │
│  ┌──────────┐  ┌───────────┐  ┌─────────────┐  │
│  │  Upload  │  │   Chat    │  │  Chart View │  │
│  │  Data    │  │  Q&A      │  │  (matplot)  │  │
│  └────┬─────┘  └─────┬─────┘  └──────┬──────┘  │
└───────┼──────────────┼────────────────┼─────────┘
        │              │                │
┌───────▼──────────────▼────────────────▼─────────┐
│                 Data Engine                       │
│  ┌──────────────┐  ┌──────────────────────────┐ │
│  │  pandas      │  │  LangChain + DeepSeek    │ │
│  │  (Data I/O)  │  │  (Analysis Agent)        │ │
│  └──────────────┘  └──────────────────────────┘ │
└─────────────────────────────────────────────────┘
        │                          │
        ▼                          ▼
┌──────────────┐        ┌──────────────────────┐
│  Excel/CSV   │        │  DeepSeek API        │
│  Files       │        │  (Code + Insights)   │
└──────────────┘        └──────────────────────┘
```

### Quick Start

```bash
git clone https://github.com/SsllF8/ai-data-analyzer.git
cd ai-data-analyzer
python -m venv .venv && .venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp .env.example .env  # Fill in your DEEPSEEK_API_KEY
streamlit run app.py
```

### Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `DEEPSEEK_API_KEY` | ✅ | Your DeepSeek API key |
| `DEEPSEEK_BASE_URL` | ❌ | API base URL (defaults to `https://api.deepseek.com`) |

### Project Highlights

**1. Why Agent mode instead of hardcoded analysis?**
- AI dynamically generates analysis code for any question — no need to pre-define scenarios
- Demonstrates AI generalization — one tool handles infinite analysis needs

**2. Code execution safety?**
- Only safe libraries allowed (pandas, matplotlib)
- Can sandbox `exec()` to restrict dangerous imports
- Production should use Docker container isolation

**3. Why pandas instead of letting AI calculate directly?**
- AI numerical computation is unreliable (precision issues, overflow)
- pandas is battle-tested; AI generating pandas code is more reliable
- pandas handles millions of rows; pure LLM cannot

**4. Difference from traditional BI tools?**
- Zero learning curve — natural language instead of drag-and-drop or SQL
- Better for exploratory/ad-hoc analysis; BI is better for fixed dashboards

### Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Verbose AI responses | LLM not constrained on output length | Add "keep under 200 words" to system prompt |
| Generated code errors | LLM hallucinated non-existent functions | Add retry mechanism with error feedback |
| Chinese column names garbled | pandas encoding detection | Specify `encoding='utf-8'` or `'gbk'` |
| Charts not displaying | Missing Chinese fonts in matplotlib | Set `plt.rcParams['font.sans-serif'] = ['SimHei']` |
| Large file slow to load | Full pandas in-memory read | Use `chunksize` or sample data for preview |
| Data lost after upload | Streamlit rerun | Cache DataFrame in `st.session_state` |

### Future Enhancements

- **More data sources** — MySQL, PostgreSQL, API endpoints
- **Interactive charts** — Switch to Plotly/pyecharts for zoom and hover
- **Text-to-SQL** — Query databases using natural language
- **Auto report export** — One-click PDF/Word report generation
- **Data cleaning assistant** — AI detects anomalies and suggests fixes
- **Scheduled analysis** — Automated daily analysis with trend push notifications
- **Multi-table joins** — Upload multiple files, AI auto-detects relationships

## 📄 License

This project is licensed under the MIT License.
