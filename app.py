"""
AI 数据分析助手 - Web 前端界面

运行方式：streamlit run app.py
"""

import os
import time
import pandas as pd
import streamlit as st
from data_engine import (
    load_data,
    get_data_summary,
    analyze_data,
    generate_data_insights,
    get_llm,
)

# ============================================================
# 页面配置
# ============================================================

st.set_page_config(
    page_title="AI 数据分析助手",
    page_icon="📊",
    layout="wide",
)

# ============================================================
# 自定义样式
# ============================================================

st.markdown("""
<style>
    .main-title {
        text-align: center;
        padding: 20px 0;
    }
    .main-title h1 {
        font-size: 2.2em;
        margin-bottom: 8px;
    }
    .stChatMessage {
        border-radius: 12px;
    }
    .data-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        margin-bottom: 10px;
    }
    .example-btn {
        display: inline-block;
        padding: 6px 14px;
        margin: 3px;
        border-radius: 16px;
        background: #f0f2f6;
        color: #333;
        font-size: 13px;
        cursor: pointer;
    }
    .example-btn:hover {
        background: #e2e6ee;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 初始化 session state
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []
if "df" not in st.session_state:
    st.session_state.df = None
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False
if "analysis_count" not in st.session_state:
    st.session_state.analysis_count = 0

# ============================================================
# 侧边栏：数据上传和管理
# ============================================================

with st.sidebar:
    st.markdown("## 📁 数据管理")
    st.markdown("---")
    
    # 文件上传
    uploaded_file = st.file_uploader(
        "上传数据文件",
        type=["csv", "xlsx", "xls"],
        help="支持 CSV 和 Excel (.xlsx) 格式",
    )
    
    # 加载数据
    if uploaded_file is not None:
        try:
            with st.spinner("正在加载数据..."):
                df = load_data(uploaded_file)
                st.session_state.df = df
                st.session_state.data_loaded = True
                st.session_state.messages = []  # 清空历史
            st.success(f"✅ 数据加载成功！{len(df)} 行 × {len(df.columns)} 列")
        except Exception as e:
            st.error(f"❌ 数据加载失败：{str(e)}")
    
    # 数据概览（加载后显示）
    if st.session_state.data_loaded and st.session_state.df is not None:
        st.markdown("---")
        st.markdown("### 📋 数据概览")
        
        df = st.session_state.df
        st.metric("行数", len(df))
        st.metric("列数", len(df.columns))
        st.metric("已分析", f"{st.session_state.analysis_count} 次")
        
        # 列信息
        with st.expander("查看列信息"):
            for col in df.columns:
                st.markdown(f"- **{col}** ({df[col].dtype})")
    
    # 快速洞察按钮
    if st.session_state.data_loaded:
        st.markdown("---")
        if st.button("🔍 AI 快速洞察", use_container_width=True, type="primary"):
            with st.spinner("AI 正在分析数据..."):
                llm = get_llm()
                insights = generate_data_insights(llm, st.session_state.df)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"## 📊 数据洞察报告\n\n{insights}",
                    "type": "insight",
                })
                st.session_state.analysis_count += 1
                st.rerun()
    
    # 使用说明
    st.markdown("---")
    with st.expander("💡 使用说明"):
        st.markdown("""
        1. 上传 CSV 或 Excel 文件
        2. 在右侧对话框输入分析需求
        3. AI 自动生成代码并分析
        4. 查看图表和文字结论
        
        **支持的分析类型：**
        - 数据统计（最大值、平均值、总和等）
        - 趋势分析（折线图、柱状图）
        - 对比分析（分组对比）
        - 分布分析（饼图、直方图）
        - 相关性分析
        """)

# ============================================================
# 主页面
# ============================================================

st.markdown("""
<div class="main-title">
    <h1>📊 AI 数据分析助手</h1>
    <p style="color: #6c757d; font-size: 16px;">
        上传数据 → 自然语言提问 → AI 自动分析并生成图表 | 基于 LangChain + DeepSeek + Pandas
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# 如果没有加载数据，显示欢迎页
if not st.session_state.data_loaded:
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px;">
        <h2 style="color: #666;">👋 欢迎！请在左侧上传数据文件开始分析</h2>
        <p style="color: #999; font-size: 15px;">支持 CSV、Excel 格式，AI 会自动理解数据结构并帮你分析</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 示例演示区域
    st.markdown("---")
    st.markdown("### 🎯 能做什么？举几个例子")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📈 数据统计**
        - "上个月的总销售额是多少？"
        - "各产品的平均单价？"
        - "哪个区域的业绩最好？"
        
        **📊 图表生成**
        - "画一个各月销售额的折线图"
        - "用饼图展示产品销量占比"
        - "画一个各区域的销售排名柱状图"
        """)
    
    with col2:
        st.markdown("""
        **🔍 深度分析**
        - "同比去年，增长最快的是哪个季度？"
        - "哪个客户贡献了最多的收入？"
        - "帮我总结这份销售数据的关键趋势"
        
        **📋 数据清理**
        - "数据中有缺失值吗？"
        - "有哪些异常数据？"
        - "帮我按日期排序数据"
        """)

else:
    # 数据已加载，显示数据预览
    df = st.session_state.df
    
    # 数据预览
    with st.expander("📋 数据预览（点击展开）", expanded=False):
        st.dataframe(df.head(10), use_container_width=True)
    
    # 示例问题按钮
    st.markdown("**💡 试试这些问题：**")
    
    # 根据数据列智能生成示例问题
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    text_cols = df.select_dtypes(include='object').columns.tolist()
    date_cols = [c for c in df.columns if 'date' in c.lower() or '日期' in c or '时间' in c]
    
    example_questions = []
    if numeric_cols:
        example_questions.append(f"计算 {numeric_cols[0]} 的总和和平均值")
    if len(numeric_cols) >= 2:
        example_questions.append(f"{numeric_cols[0]} 和 {numeric_cols[1]} 的关系")
    if text_cols:
        example_questions.append(f"按 {text_cols[0]} 分组统计")
    if len(numeric_cols) >= 1 and text_cols:
        example_questions.append(f"画一个按 {text_cols[0]} 分组的 {numeric_cols[0]} 柱状图")
    if len(numeric_cols) >= 2:
        example_questions.append(f"用散点图展示 {numeric_cols[0]} 和 {numeric_cols[1]} 的关系")
    example_questions.append("帮我总结这份数据的关键洞察")
    
    # 限制显示数量
    example_questions = example_questions[:5]
    
    cols = st.columns(len(example_questions))
    for i, q in enumerate(example_questions):
        with cols[i]:
            if st.button(q, key=f"example_{i}", use_container_width=True):
                st.session_state.messages.append({
                    "role": "user",
                    "content": q,
                    "type": "question",
                })
                st.rerun()
    
    # 对话历史
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(msg["content"])
                # 如果有图表，显示图表
                if "chart_path" in msg and msg["chart_path"] and os.path.exists(msg["chart_path"]):
                    st.image(msg["chart_path"])
                # 如果有代码，可展开查看
                if "code" in msg and msg["code"]:
                    with st.expander("🔧 查看生成的代码"):
                        st.code(msg["code"], language="python")
    
    # 对话输入框
    if prompt := st.chat_input("输入你的数据分析需求..."):
        # 显示用户问题
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "type": "question",
        })
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 执行分析
        with st.chat_message("assistant"):
            with st.spinner("🤔 AI 正在思考并生成分析代码..."):
                result = analyze_data(df, prompt)
                
                # 构建回复
                reply_parts = []
                
                # 文字结论
                if result.get("text"):
                    reply_parts.append(result["text"])
                
                # 显示图表
                chart_path = None
                if result.get("chart"):
                    chart_path = result["chart"]
                    st.image(chart_path)
                
                # 显示错误
                if result.get("error"):
                    st.error(result["error"])
                    reply_parts.append(f"\n⚠️ {result['error']}")
                
                # 显示回复文本
                if reply_parts:
                    st.markdown("\n".join(reply_parts))
                
                # 显示代码
                if result.get("code"):
                    with st.expander("🔧 查看生成的代码"):
                        st.code(result["code"], language="python")
                
                # 保存到消息历史
                assistant_msg = {
                    "role": "assistant",
                    "content": "\n".join(reply_parts) if reply_parts else "分析完成",
                    "type": "analysis",
                }
                if chart_path:
                    assistant_msg["chart_path"] = chart_path
                if result.get("code"):
                    assistant_msg["code"] = result["code"]
                
                st.session_state.messages.append(assistant_msg)
                st.session_state.analysis_count += 1
