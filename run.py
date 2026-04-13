#!/usr/bin/env python3
"""
一键启动学科分类器
自动安装依赖并启动应用
"""

import subprocess
import sys
import os

def main():
    print("正在检查并安装依赖...")

    # 检查并安装依赖
    required_packages = ['streamlit', 'pandas', 'openpyxl', 'openai']
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            print(f"安装 {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

    # 启动 Streamlit
    app_file = os.path.join(os.path.dirname(__file__), 'subject_classifier_single.py')
    print(f"启动应用: {app_file}")
    subprocess.run([sys.executable, '-m', 'streamlit', 'run', app_file])

if __name__ == "__main__":
    main()