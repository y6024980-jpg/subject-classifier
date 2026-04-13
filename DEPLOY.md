# 学科分类器 - 部署指南

## 快速部署到 Streamlit Cloud（免费）

### 步骤 1: 创建 GitHub 仓库

1. 登录 [GitHub](https://github.com)
2. 点击 `New repository` 创建新仓库，命名为 `subject-classifier`
3. 上传以下文件：
   - `subject_classifier_single.py`（主应用）
   - `requirements.txt`（依赖）
   - `.streamlit/config.toml`（可选配置）

### 步骤 2: 部署到 Streamlit Cloud

1. 打开 [Streamlit Cloud](https://share.streamlit.io)
2. 使用 GitHub 账号登录
3. 点击 `New app`
4. 选择刚才创建的 GitHub 仓库
5. 设置：
   - Branch: `main`
   - Main file path: `subject_classifier_single.py`
6. 点击 `Deploy`

### 步骤 3: 使用

部署完成后，Streamlit 会提供一个链接（如 `https://xxx.streamlit.app`），分享给用户即可。

---

## 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 启动
streamlit run subject_classifier_single.py
```

---

## 文件说明

| 文件 | 说明 |
|------|------|
| subject_classifier_single.py | 主应用 |
| requirements.txt | Python 依赖 |
| .streamlit/config.toml | Streamlit 配置 |
| start.bat / start.sh | 本地启动脚本 |