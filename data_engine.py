"""
AI 数据分析核心引擎

工作流程：
1. 加载数据文件（Excel/CSV）并展示基本信息
2. 用户用自然语言提问
3. AI 生成 Python 代码来分析数据
4. 执行代码，返回图表和分析结论
"""

import os
import io
import re
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # 无头模式，不弹出窗口
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# 设置中文字体（Windows）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

from langchain_openai import ChatOpenAI

# 加载环境变量
load_dotenv()


def get_llm():
    """获取 DeepSeek 大模型实例"""
    return ChatOpenAI(
        model="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        temperature=0,  # 数据分析需要稳定、准确的输出
    )


def load_data(uploaded_file) -> pd.DataFrame:
    """
    加载上传的数据文件，支持 Excel 和 CSV
    
    Args:
        uploaded_file: Streamlit 上传的文件对象
        
    Returns:
        pandas DataFrame
    """
    file_name = uploaded_file.name.lower()
    
    if file_name.endswith('.csv'):
        # CSV 文件：尝试不同编码
        for encoding in ['utf-8', 'gbk', 'gb2312', 'latin-1']:
            try:
                df = pd.read_csv(io.BytesIO(uploaded_file.read()), encoding=encoding)
                return df
            except (UnicodeDecodeError, Exception):
                uploaded_file.seek(0)
                continue
        raise ValueError("无法解析 CSV 文件，请检查文件格式")
    
    elif file_name.endswith(('.xls', '.xlsx')):
        # Excel 文件
        df = pd.read_excel(io.BytesIO(uploaded_file.read()), engine='openpyxl')
        return df
    
    else:
        raise ValueError(f"不支持的文件格式：{file_name}，请上传 CSV 或 Excel 文件")


def get_data_summary(df: pd.DataFrame) -> str:
    """
    生成数据概览信息，给 AI 理解数据结构用
    
    Args:
        df: pandas DataFrame
        
    Returns:
        数据概览文本
    """
    summary = f"""数据概览：
- 行数：{len(df)}
- 列数：{len(df.columns)}
- 列名和类型：
"""
    for col in df.columns:
        dtype = str(df[col].dtype)
        non_null = df[col].count()
        null_count = df[col].isnull().sum()
        # 如果是分类数据（唯一值较少），列出所有唯一值
        if df[col].nunique() <= 15 and df[col].dtype == 'object':
            unique_vals = ', '.join(str(v) for v in df[col].dropna().unique())
            summary += f"  - {col} ({dtype}): {non_null} 个非空值, {null_count} 个空值, 唯一值: [{unique_vals}]\n"
        else:
            summary += f"  - {col} ({dtype}): {non_null} 个非空值, {null_count} 个空值\n"
    
    # 添加前 5 行样本数据
    summary += f"\n前 5 行数据样本：\n{df.head(5).to_string()}"
    
    return summary


def generate_analysis_code(llm, question: str, data_summary: str, df_columns: list) -> str:
    """
    让 AI 根据用户问题和数据结构生成 Python 分析代码
    
    Args:
        llm: 大模型实例
        question: 用户问题
        data_summary: 数据概览
        df_columns: 列名列表
        
    Returns:
        生成的 Python 代码字符串
    """
    prompt = f"""你是一个专业的数据分析 Python 工程师。用户会提出数据分析问题，你需要生成 Python 代码来分析数据。

当前数据信息：
{data_summary}

可用变量：
- df: pandas DataFrame，已加载的数据

用户问题：{question}

请生成 Python 代码来完成分析。要求：
1. 直接操作变量 df，不要重新读取文件
2. 使用 matplotlib 生成图表（中文需用 SimHei 字体）
3. 如果需要展示结果，使用 print() 输出关键数据
4. 图表要美观：设置标题、标签、适当的大小
5. 将图表保存为变量 chart_path = 'chart.png'（使用 plt.savefig('chart.png', bbox_inches='tight', dpi=100)）
6. 如果问题不需要图表（纯文字分析），就不要生成图表代码
7. 最后用 print() 输出一段简洁的中文分析结论（2-4句话即可，不要冗长）
8. 代码要简洁高效，处理可能的异常情况
9. 【重要】不要 print() 输出原始数据表格、长列表或 DataFrame。只 print() 精炼的统计结果和文字结论
10. 【重要】如果图表已经直观展示了数据，print() 中只需给出简洁的总结性结论即可，不要重复罗列具体数值

只输出 Python 代码，不要任何解释。代码用 ```python 和 ``` 包裹。"""

    response = llm.invoke(prompt)
    content = response.content
    
    # 提取代码块
    code_match = re.search(r'```python\s*(.*?)```', content, re.DOTALL)
    if code_match:
        return code_match.group(1).strip()
    
    # 如果没有代码块标记，尝试直接提取
    return content.strip()


def _clean_output_text(text: str) -> str:
    """
    清理 AI 生成代码的 print 输出，过滤掉冗长的原始数据
    
    规则：
    1. 逐行判断，如果连续出现超过 10 行"纯数据行"（大量数字/日期），截断并折叠
    2. 只保留开头和结尾各 3 行，中间用省略号替代
    """
    if not text:
        return text
    
    lines = text.split('\n')
    
    # 识别"数据行"：包含大量数字、日期、但不含中文总结性语句
    data_line_pattern = re.compile(
        r'^[\s]*(\d{4}[-/]\d{1,2}[-/]\d{1,2}|'  # 日期开头
        r'\d+\s+[\d.,]+\s*|'                       # 数字开头（如 2025  100.5）
        r'\d{1,2}[\s|,]\d{1,2}[\s|,]\d{1,2}|'     # 索引格式（如 0  1  2）
        r'Name:\s|dtype:|Length:)'                   # pandas 输出尾部的元信息
    )
    
    # 识别"结论行"：包含中文或分析性描述
    conclusion_pattern = re.compile(r'[\u4e00-\u9fff]|[结论|分析|总计|平均|最大|最小|趋势|增长]')
    
    MAX_CONSECUTIVE_DATA_LINES = 8
    
    # 找出连续数据行超过阈值的区间，进行折叠
    result_lines = []
    i = 0
    while i < len(lines):
        # 检测连续数据行段
        consecutive_data = []
        start = i
        while i < len(lines):
            line = lines[i]
            is_data = bool(data_line_pattern.search(line)) and not bool(conclusion_pattern.search(line))
            if is_data:
                consecutive_data.append(line)
                i += 1
            else:
                break
        
        if len(consecutive_data) > MAX_CONSECUTIVE_DATA_LINES:
            # 截断：保留前 3 行 + 后 3 行
            keep = 3
            truncated = consecutive_data[:keep] + [f'  ... 共 {len(consecutive_data)} 行数据已省略 ...'] + consecutive_data[-keep:]
            result_lines.extend(truncated)
        elif consecutive_data:
            result_lines.extend(consecutive_data)
        # 如果不是数据行，也加入（即包含中文的分析行）
        if i < len(lines) and not (bool(data_line_pattern.search(lines[i])) and not bool(conclusion_pattern.search(lines[i]))):
            result_lines.append(lines[i])
            i += 1
    
    cleaned = '\n'.join(result_lines)
    
    # 最终安全检查：如果输出总行数仍然超过 30 行，做整体截断
    final_lines = cleaned.split('\n')
    if len(final_lines) > 30:
        cleaned = '\n'.join(final_lines[:20]) + f'\n\n... (共 {len(final_lines)} 行，已省略中间部分)'
    
    return cleaned


def execute_analysis_code(code: str, df: pd.DataFrame) -> dict:
    """
    在安全环境中执行 AI 生成的分析代码
    
    Args:
        code: Python 代码字符串
        df: pandas DataFrame
        
    Returns:
        dict: {
            "text": 分析结论文本,
            "chart": 图表文件路径（如果有）,
            "error": 错误信息（如果有）
        }
    """
    result = {
        "text": "",
        "chart": None,
        "error": None,
    }
    
    # 准备执行环境
    local_vars = {
        'df': df.copy(),
        'pd': pd,
        'plt': plt,
    }
    
    # 捕获 print 输出
    output_buffer = io.StringIO()
    
    # 重定向 print 和保存图表路径
    chart_path = os.path.join(os.path.dirname(__file__), 'chart.png')
    local_vars['chart_path'] = chart_path
    
    try:
        # 创建自定义执行环境
        import sys
        
        # 执行代码
        exec(code, {
            '__builtins__': __builtins__,
            'pd': pd,
            'plt': plt,
            'print': lambda *args, **kwargs: print(*args, file=output_buffer, **kwargs),
            'df': df.copy(),
        })
        
        # 获取输出文本
        raw_text = output_buffer.getvalue().strip()
        # 智能过滤：截断过长的原始数据输出，保留精炼结论
        result["text"] = _clean_output_text(raw_text)
        
        # 检查是否生成了图表
        if os.path.exists(chart_path):
            result["chart"] = chart_path
        
        # 关闭所有图表，释放内存
        plt.close('all')
        
    except Exception as e:
        result["error"] = f"代码执行出错：{str(e)}"
        plt.close('all')
    
    return result


def analyze_data(df: pd.DataFrame, question: str) -> dict:
    """
    完整的数据分析流程：
    1. 生成数据概览
    2. 让 AI 生成分析代码
    3. 执行代码获取结果
    
    Args:
        df: pandas DataFrame
        question: 用户问题
        
    Returns:
        分析结果字典
    """
    # 1. 生成数据概览
    data_summary = get_data_summary(df)
    
    # 2. AI 生成分析代码
    llm = get_llm()
    code = generate_analysis_code(llm, question, data_summary, list(df.columns))
    
    # 3. 执行代码
    result = execute_analysis_code(code, df)
    
    # 保存生成的代码（调试用）
    result["code"] = code
    
    return result


def generate_data_insights(llm, df: pd.DataFrame) -> str:
    """
    AI 自动分析数据，生成整体洞察报告
    
    Args:
        df: pandas DataFrame
        llm: 大模型实例
        
    Returns:
        洞察报告文本
    """
    data_summary = get_data_summary(df)
    
    # 计算一些基本统计信息
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    stats_text = ""
    if numeric_cols:
        stats_df = df[numeric_cols].describe()
        stats_text = f"\n数值列统计信息：\n{stats_df.to_string()}"
    
    prompt = f"""你是一个专业的数据分析师。请根据以下数据概览，给出一份简洁的数据洞察报告。

{data_summary}
{stats_text}

请从以下几个方面分析（如果数据支持的话）：
1. 数据整体情况概述
2. 关键指标和趋势
3. 值得注意的异常或亮点
4. 建议关注的方向

用简洁的中文回答，使用项目符号，每个要点一句话。不要太长。"""

    response = llm.invoke(prompt)
    return response.content
