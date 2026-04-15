# 📊 AI Data Analysis Assistant

> An intelligent data analysis tool that combines LLM-powered insights with programmatic data processing. Upload your data, ask questions in natural language, and get both AI analysis and executable Python charts.

![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-red?logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-0.3+-green?logo=chainlink)
![DeepSeek](https://img.shields.io/badge/DeepSeek-API-blue)
![pandas](https://img.shields.io/badge/pandas-2.0+-blue?logo=pandas)
![matplotlib](https://img.shields.io/badge/matplotlib-3.8+-orange)

## 🎯 Use Cases

### Business Scenarios
- **Sales Analysis** — Upload monthly/quarterly sales data in Excel, ask "Which product had the highest growth?" or "Show me the regional sales comparison"
- **Financial Reporting** — Load financial statements and ask the AI to identify trends, anomalies, and key metrics
- **KPI Monitoring** — Import team performance data and get instant summaries, highlight outliers, and track progress against targets
- **Survey Analysis** — Upload survey results and ask for sentiment breakdowns, demographic correlations, and actionable insights

### Personal Scenarios
- **Personal Finance Tracking** — Import your expense records (CSV/Excel) and ask the AI to categorize spending, find savings opportunities, or visualize monthly trends
- **Fitness & Health Data** — Analyze workout logs, sleep data, or nutrition records to find patterns and optimization suggestions
- **Academic Research** — Process experiment data, generate statistical summaries, and create publication-quality charts

### Key Differentiator
Unlike traditional BI tools that require writing SQL or learning complex interfaces, this tool lets you **ask questions in plain language** — the AI understands your intent and generates both text analysis and Python code to create charts.

## ✨ Features

### Core Capabilities
- 📁 **Excel/CSV Upload** — Drag and drop your data files (`.xlsx`, `.csv`, `.xls`)
- 📊 **Auto Data Summary** — Instantly see row count, column types, missing values, basic statistics
- 💬 **Natural Language Q&A** — Ask anything about your data in plain English or Chinese
- 🤖 **AI-Powered Analysis** — DeepSeek identifies trends, outliers, and patterns with detailed explanations
- 📈 **Auto Chart Generation** — AI writes Python code to create matplotlib visualizations on the fly
- 💾 **Sample Data Included** — Comes with a sample sales dataset to get started immediately

### Analysis Examples
Ask the AI things like:
- "哪个月份的销售额最高？增长趋势如何？"
- "各个产品类别的销售占比是多少？画个饼图"
- "找出销售额异常的月份，分析可能的原因"
- "对比不同区域的销售表现，生成柱状图"
- "总结这份数据的关键发现和业务建议"

## 🏗️ Architecture

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

## 📁 Project Structure

```
ai-data-analyzer/
├── app.py                    # Streamlit web interface
├── data_engine.py            # Data processing + AI analysis engine
├── generate_sample_data.py   # Script to generate sample dataset
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── sample_data/
│   └── 2025年销售数据.xlsx   # Sample sales dataset
└── screenshots/              # UI screenshots
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- DeepSeek API Key ([Get one here](https://platform.deepseek.com))

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/SsllF8/ai-data-analyzer.git
cd ai-data-analyzer

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and fill in your DEEPSEEK_API_KEY

# 5. Run the application
streamlit run app.py
```

Or simply double-click `启动应用.bat` on Windows.

### Try It Out

1. Launch the app → Click "使用示例数据" to load the included sales dataset
2. In the chat box, try asking:
   - "帮我分析这份数据的整体趋势"
   - "画一个各月销售额的柱状图"
   - "哪个产品类别表现最好？"
   - "找出异常数据并分析原因"

## ⚙️ Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `DEEPSEEK_API_KEY` | ✅ | Your DeepSeek API key |
| `DEEPSEEK_BASE_URL` | ❌ | API base URL (defaults to `https://api.deepseek.com`) |

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Web Framework | Streamlit | Interactive data visualization UI |
| AI Framework | LangChain | Agent orchestration & tool binding |
| LLM | DeepSeek | Natural language understanding & code generation |
| Data Processing | pandas | Data loading, cleaning, aggregation |
| Visualization | matplotlib | Dynamic chart generation |
| File Parsing | openpyxl | Excel file reading |

## 🔧 How It Works

1. **Data Loading** — pandas reads Excel/CSV files and generates a statistical summary
2. **User Query** — User asks a question in natural language via the chat interface
3. **AI Analysis** — LangChain Agent receives the data schema and user query, then:
   - Generates pandas code to analyze the data
   - Executes the code safely in a sandboxed environment
   - Interprets results and writes a human-readable analysis
   - Creates matplotlib charts when visualization is requested
4. **Result Display** — Charts are rendered inline, analysis text appears in the chat

## 📄 License

This project is licensed under the MIT License.
