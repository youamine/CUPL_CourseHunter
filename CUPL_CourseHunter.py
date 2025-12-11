import requests
import time
import random
import re
from bs4 import BeautifulSoup

# ===================== 配置模板（请根据自身抓包结果替换 <> 中的内容） =====================
CONFIG = {
    # 【必替换】从浏览器F12抓包获取最新Cookies（每次运行前更新）
    "cookies": {
        'JSESSIONID': '<你的JSESSIONID>',
        'SecTs': '<你的SecTs>',
        'mpid': '<你的mpid>',
        'GSESSIONID': '<你的GSESSIONID>'
    },
    # 【必替换】抓包得到的选课提交接口URL（非列表页）
    "url": 'http://jwxt.cupl.edu.cn/eams/stdElectCourse!batchOperator.action?profileId=<你的选课批次ID>',
    # 清空冗余参数（如需添加抓包的params，格式：'参数名': '<参数值>'）
    "params": {},
    # 【必替换】选课配置：键=课程ID，值=抓包的operator0值
    "lessons": {
        '<你的课程ID>': '<你的课程ID>:true:0'  # 格式：'课程ID:true:0'=抢课，'课程ID:false:0'=退课
    },
    # 请求头模板（仅替换Referer中的专属参数，其余可保留）
    "headers": {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'jwxt.cupl.edu.cn',
        'Origin': 'http://jwxt.cupl.edu.cn',
        'Referer': 'http://jwxt.cupl.edu.cn/eams/stdElectCourse!defaultPage.action?projectId=<你的projectId>&electionProfile.id=<你的选课批次ID>',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    },
    # 抢课速度配置（数值越小速度越快，风控风险越高）
    "delay_base": 0.4,    # 基础延迟（秒）：推荐0.4~2.0
    "delay_rand": 0.1,    # 随机延迟（秒）：推荐0.1~1.0
    "timeout": 10         # 请求超时时间（秒）
}
# ========================================================================================

def CUPL_CourseHunter():
    """核心选课逻辑：包含会话初始化、请求发送、鲁棒的结果解析"""
    counter = 0
    session = requests.Session()
    session.cookies.update(CONFIG["cookies"])
    session.headers.update(CONFIG["headers"])

    print("🚀 选课脚本启动（按 Ctrl+C 可手动终止）")
    print(f"📌 待选课程ID：{list(CONFIG['lessons'].keys())}")

    # 前置GET请求：初始化选课会话
    try:
        print("\n🔍 初始化选课会话（访问列表页）...")
        # 【需替换】选课列表页URL（和Referer一致）
        list_page_url = 'http://jwxt.cupl.edu.cn/eams/stdElectCourse!defaultPage.action?projectId=<你的projectId>&electionProfile.id=<你的选课批次ID>'
        get_resp = session.get(url=list_page_url, timeout=CONFIG["timeout"])
        if get_resp.status_code != 200:
            print(f"❌ 会话初始化失败 | 状态码：{get_resp.status_code}")
            return
        print("✅ 会话初始化完成")
        time.sleep(1)
    except Exception as e:
        print(f"❌ 会话初始化异常：{str(e)}")
        return

    try:
        while True:
            for lesson_id, operator in CONFIG["lessons"].items():
                data = {
                    'optype': 'true',
                    'operator0': operator,
                    'lesson0': lesson_id,
                    f'schLessonGroup_{lesson_id}': 'undefined',
                }

                resp = session.post(
                    url=CONFIG["url"],
                    params=CONFIG["params"],
                    data=data,
                    timeout=CONFIG["timeout"],
                    allow_redirects=False
                )
                resp.encoding = resp.apparent_encoding
                counter += 1

                if resp.status_code != 200:
                    print(f"\n❌ 第{counter}次请求失败 | 状态码：{resp.status_code}")
                    if resp.status_code == 403:
                        print("⚠️  403拒绝：IP风控/参数不匹配！建议换网络/核对抓包参数")
                    elif resp.status_code in [301, 302]:
                        print("⚠️  重定向：Cookies过期！立即更新Cookies后重启")
                    time.sleep(3)
                    continue

                # 鲁棒解析系统提示
                soup = BeautifulSoup(resp.text, 'html.parser')
                raw_text = soup.get_text(strip=True)
                text_match = re.findall(r'[\u4e00-\u9fa50-9]+', raw_text)
                final_tip = ''.join(text_match) if text_match else resp.text[:300]

                # 结果判断
                if re.search(rf'课程{lesson_id}选课成功|选课申请成功|抢课成功', final_tip):
                    print(f"\n✅ 第{counter}次请求 | 课程{lesson_id}抢课成功！🎉")
                    return
                elif re.search(rf'课程{lesson_id}退课成功', final_tip):
                    print(f"\n✅ 第{counter}次请求 | 课程{lesson_id}退课成功！🎉")
                    return
                elif re.search(r'失败|无剩余|名额已满|时间冲突|学分冲突|课程不存在|无效ID|无权限|未开放|超出上限', final_tip):
                    print(f"\n❌ 第{counter}次请求 | 课程{lesson_id}抢课失败：{final_tip[:200]}")
                elif re.search(r'过快|频繁|请稍后再试|风控|限制', final_tip):
                    print(f"\n⚠️  第{counter}次请求 | 触发系统风控：{final_tip[:100]}")
                    time.sleep(2)
                elif re.search(r'登录失效|请先登录|Session过期|JSESSIONID', final_tip):
                    print(f"\n❌ 第{counter}次请求 | Cookies过期/登录失效！❌")
                    return
                else:
                    print(f"\nℹ️  第{counter}次请求 | 系统返回提示：{final_tip[:200]}")

                # 动态延迟
                delay = CONFIG["delay_base"] + random.random() * CONFIG["delay_rand"]
                time.sleep(delay)

                if counter % 10 == 0:
                    print(f"\n📌 已连续请求{counter}次 | 当前时间：{time.strftime('%H:%M:%S')}")

    except KeyboardInterrupt:
        print("\n\n🛑 你手动终止了脚本")
    except requests.exceptions.RequestException as e:
        print(f"\n\n❌ 网络异常：{str(e)} | 脚本终止")
    except Exception as e:
        print(f"\n\n❌ 未知错误：{str(e)} | 脚本终止")

# ===================== 免责声明 =====================
"""
【免责声明】
1. 本脚本仅用于学习Python网络请求、网页解析等技术，严禁用于任何违规用途；
2. 使用前请务必遵守所在学校的教务系统使用规范，因违规使用导致的账号封禁、法律责任，由使用者自行承担；
3. 作者不对脚本的可用性、稳定性做任何承诺，也不对使用脚本造成的任何损失负责；
4. 请勿将本脚本用于商业用途，二次分发请保留本免责声明。
"""

if __name__ == '__main__':
    CUPL_CourseHunter()
    print("\n📝 脚本已退出")