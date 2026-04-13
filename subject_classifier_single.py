#!/usr/bin/env python3
"""
学科分类器 - 单模型版
使用1个大模型对题目进行学科分类
"""

import streamlit as st
import pandas as pd
from openai import OpenAI
import io
import re

# ========== 页面配置 ==========
st.set_page_config(
    page_title="学科分类器(单模型)",
    page_icon="📚",
    layout="centered"
)

# ========== CSS样式 ==========
st.markdown("""
<style>
    .main { padding: 2rem; }
    .stButton > button { width: 100%; padding: 0.8rem; font-size: 1.1rem; }
    .success-box { padding: 1rem; border-radius: 0.5rem; background-color: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
    .info-box { padding: 1rem; border-radius: 0.5rem; background-color: #d1ecf1; border: 1px solid #bee5eb; color: #0c5460; }
</style>
""", unsafe_allow_html=True)

# ========== API配置 ==========
# 从 Streamlit Secrets 读取 API 密钥（部署到云端时使用）
# 本地运行时可通过环境变量或 .streamlit/secrets.toml 设置
try:
    API_KEY = st.secrets["API_KEY"]
except:
    # 本地开发 fallback
    API_KEY = "sk-azwbstdwfdwlyisldlfbdmymszjcdkfhoojksozzugcarzec"

# 单个模型配置
MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"

# 学科列表
SUBJECTS = [
    "数学", "物理", "电气", "化学", "生物", "能源", "机械", "计算机",
    "通讯", "金融", "统计", "文科", "土木", "天文", "医学", "管理学", "其他学科"
]

# 提示词
CLASSIFICATION_PROMPT = """题目：{question}
学科：{subjects_list}
判断这道题属于哪个学科，只回答学科名称。"""


def extract_subject(result):
    """从LLM输出中提取学科名称"""
    match = re.search(r'学科[：:]\s*([^\n]+)', result)
    if match:
        subject = match.group(1).strip()
    else:
        subject = None
        for subj in SUBJECTS:
            if subj in result:
                subject = subj
                break
        if subject is None:
            subject = "其他学科"

    subject = subject.strip().rstrip('。').rstrip('.')
    for subj in SUBJECTS:
        if subj in subject:
            return subj

    return subject


def classify_question(client, question):
    """使用单个模型分类"""
    question_short = str(question)[:300]
    prompt = CLASSIFICATION_PROMPT.format(
        question=question_short,
        subjects_list=','.join(SUBJECTS)
    )
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=10,
            timeout=30
        )
        result = response.choices[0].message.content.strip()
        return extract_subject(result)
    except Exception as e:
        print(f"分类出错: {e}")
        return "其他学科"


def main():
    st.title("📚 学科分类器(单模型)")
    st.markdown(f"使用 **{MODEL_NAME}** 进行学科分类")

    st.markdown("---")

    # 文件上传
    st.subheader("📁 上传文件")
    uploaded_file = st.file_uploader(
        "请上传Excel文件（.xlsx格式）",
        type=['xlsx'],
        help="文件需包含 'src' 或 'query' 列（只需其一）"
    )

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)

            # 检查必要列
            question_col = None
            if 'src' in df.columns:
                question_col = 'src'
            elif 'query' in df.columns:
                question_col = 'query'
            else:
                st.error("❌ 错误：上传的文件中没有 'src' 或 'query' 列")
                return

            if '学科_新' not in df.columns:
                df['学科_新'] = ''

            total = len(df)
            to_classify = df[df['学科_新'].isna() | (df['学科_新'] == '')]
            to_classify_count = len(to_classify)

            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.markdown(f"**文件信息：**")
            st.markdown(f"- 题目列：{question_col}")
            st.markdown(f"- 总题目数：{total}")
            st.markdown(f"- 待分类数：{to_classify_count}")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("---")

            if to_classify_count > 0:
                if st.button("🚀 开始分类", type="primary"):
                    client = OpenAI(
                        api_key=API_KEY,
                        base_url="https://api.siliconflow.cn/v1"
                    )

                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    for i, (idx, row) in enumerate(to_classify.iterrows()):
                        question = row[question_col]
                        subject = classify_question(client, question)
                        df.loc[idx, '学科_新'] = subject

                        progress = (i + 1) / to_classify_count
                        progress_bar.progress(progress)
                        status_text.text(f"正在分类：{i+1}/{to_classify_count} → {subject}")

                    status_text.text("分类完成！")

                    st.markdown("---")
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.markdown("✅ **分类完成！**")
                    st.markdown('</div>', unsafe_allow_html=True)

                    # 统计分布
                    st.subheader("📊 学科分布")
                    subject_counts = df['学科_新'].value_counts()
                    st.bar_chart(subject_counts)

                    # 下载按钮
                    st.subheader("📥 下载结果")
                    output_buffer = io.BytesIO()
                    df.to_excel(output_buffer, index=False)
                    output_buffer.seek(0)

                    st.download_button(
                        label="下载分类后的Excel文件",
                        data=output_buffer,
                        file_name="已分类结果.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        type="primary"
                    )

                    # 预览
                    st.subheader("👀 分类结果预览")
                    st.dataframe(df[[question_col, '学科_新']].head(10), use_container_width=True)

            else:
                st.info("所有题目已完成分类！")
                st.subheader("📥 下载结果")
                output_buffer = io.BytesIO()
                df.to_excel(output_buffer, index=False)
                output_buffer.seek(0)
                st.download_button(
                    label="下载分类后的Excel文件",
                    data=output_buffer,
                    file_name="已分类结果.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type="primary"
                )

        except Exception as e:
            st.error(f"❌ 处理文件时出错：{str(e)}")

    # 使用说明
    st.markdown("---")
    with st.expander("📋 使用说明"):
        st.markdown("""
        1. 上传Excel文件（需包含 'src' 或 'query' 列）
        2. 点击"开始分类"
        3. 下载分类结果
        """)

    # 学科列表
    with st.expander("📚 学科分类列表"):
        st.write(", ".join(SUBJECTS))


if __name__ == "__main__":
    main()
