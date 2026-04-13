#!/bin/bash
# 学科分类器启动脚本 (Mac/Linux)

echo "========================================"
echo "   学科分类器 - 启动中..."
echo "========================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到 Python，请先安装 Python 3.8+"
    echo "macOS: brew install python3"
    echo "Ubuntu: sudo apt install python3"
    exit 1
fi

# 安装依赖
echo "[1/3] 检查并安装依赖..."
pip3 install streamlit pandas openpyxl openai -q 2>/dev/null

# 启动应用
echo "[2/3] 启动应用..."
echo ""
echo "应用启动后，请在浏览器中访问 http://localhost:8501"
echo ""
python3 -m streamlit run subject_classifier_single.py