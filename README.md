CUPL_CourseHunter
基于 Python 实现的中国政法大学（CUPL）教务选课系统适配脚本（仅用于 Python 网络请求、网页解析技术学习），支持自定义选课请求间隔、智能解析选课结果，精准适配法大选课系统的表单提交逻辑与返回格式。

Python script for CUPL's course selection system (for Python web request/parsing learning only). Supports custom intervals & intelligent parsing of quota/conflict/risk alerts. For learning/exchange—no unauthorized use.

🔧 前置准备（必须先完成！）
1. 安装 Python 依赖
脚本依赖 requests（网络请求）和 beautifulsoup4（网页解析），打开终端/命令行执行以下命令安装：

bash
pip install requests beautifulsoup4
2. 抓包工具
浏览器 F12 开发者工具（Network 面板）

📝 使用步骤
登录法大教务系统，进入选课页面。

按 F12（或鼠标右键点击“检查”）打开开发者工具，切换到 Network 面板。

勾选 Preserve log，然后手动点击页面的「选课」按钮。

在抓到的网络请求中，获取以下参数：

Cookies（JSESSIONID、SecTs、mpid、GSESSIONID）。

选课提交接口 URL（Request URL）。

课程 ID（Form Data → lesson0）。

选课批次 ID（URL 中的 profileId）。

打开 course_selector.py 文件，将所有由 <> 包裹的占位符替换为步骤4中抓取到的实际参数。

根据需要调整 delay_base（基础间隔）和 delay_rand（随机间隔）参数，以控制选课请求的速度。

运行脚本：python course_selector.py

✨ 核心功能
自定义请求间隔，平衡速度与风控。

智能解析选课结果（名额已满 / 时间冲突 / 风控提示）。

精准适配法大选课系统接口逻辑。

⚠️ 注意事项
本项目仅用于 Python 技术学习，严禁违规使用。

每次运行脚本前，需更新 Cookies（因其有效期较短）。

避免设置过短的请求间隔（如 ≤0.2 秒），以防账号或 IP 被封禁。

请遵守学校教务系统规定，违规使用产生的后果需自行承担。

📄 免责声明
本项目仅为技术学习示例，作者不对脚本可用性、稳定性做任何承诺，也不对使用脚本造成的任何损失负责。请勿用于商业用途，二次分发需保留本声明。
