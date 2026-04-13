@echo off
chcp 65001 >nul
echo ========================================
echo    学科分类器 - 启动中...
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 安装依赖
echo [1/3] 检查并安装依赖...
pip install streamlit pandas openpyxl openai -q

REM 启动应用
echo [2/3] 启动应用...
echo.
echo 应用启动后，请在浏览器中访问 http://localhost:8501
echo.
python -m streamlit run subject_classifier_single.py

pause