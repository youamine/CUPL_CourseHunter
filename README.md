# CUPL_CourseHunter

基于 Python 实现的中国政法大学（CUPL）教务选课系统适配脚本（仅用于 Python 网络请求、网页解析技术学习），支持自定义选课请求间隔、智能解析选课结果，精准适配法大选课系统的表单提交逻辑与返回格式。

Python script for CUPL's course selection system (for Python web request/parsing learning only). Supports custom intervals & intelligent parsing of quota/conflict/risk alerts. For learning/exchange—no unauthorized use.

## 🔧 前置准备（必须先完成！）
### 1. 安装 Python 依赖
脚本依赖 `requests`（网络请求）和 `beautifulsoup4`（网页解析），打开终端/命令行执行以下命令安装：
```bash
pip install requests beautifulsoup4
