# CUPL_CourseHunter

基于 Python 实现的中国政法大学（CUPL）教务选课系统适配脚本（仅用于 Python 网络请求、网页解析技术学习），支持自定义选课请求间隔、智能解析选课结果，精准适配法大选课系统的表单提交逻辑与返回格式。

Python script for CUPL's course selection system (for Python web request/parsing learning only). Supports custom intervals & intelligent parsing of quota/conflict/risk alerts. For learning/exchange—no unauthorized use.

## 🔧 前置准备（必须先完成！）
### 1. 安装 Python 依赖
脚本依赖 `requests`（网络请求）和 `beautifulsoup4`（网页解析），打开终端/命令行执行以下命令安装：
```bash
pip install requests beautifulsoup4
2. 抓包工具
浏览器 F12 开发者工具（Network 面板）
📝 使用步骤
登录法大教务系统，进入选课页面；
F12（或鼠标右键点击"检查"） → Network → 勾选 Preserve log，手动点击「选课」按钮，抓包获取以下参数：
Cookies（JSESSIONID、SecTs、mpid、GSESSIONID）；
选课提交接口 URL（Request URL）；
课程 ID（Form Data → lesson0）；
选课批次 ID（URL 中的 profileId）；
打开 course_selector.py，替换 <> 包裹的所有占位符为抓包参数；
调整 delay_base（基础间隔）和 delay_rand（随机间隔）设置选课速度；
运行脚本：python course_selector.py
✨ 核心功能
自定义请求间隔，平衡速度与风控；
智能解析选课结果（名额已满 / 时间冲突 / 风控提示）；
精准适配法大选课系统接口逻辑。
⚠️ 注意事项
仅用于 Python 技术学习，严禁违规使用；
每次运行前需更新 Cookies（有效期短）；
避免设置过短间隔（≤0.2 秒），防止账号 / IP 封禁；
遵守学校教务系统规定，违规使用后果自负。
📄 免责声明
本项目仅为技术学习示例，作者不对脚本可用性、稳定性做任何承诺，也不对使用脚本造成的任何损失负责。请勿用于商业用途，二次分发需保留本声明。
