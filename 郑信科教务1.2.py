import os
import sys
import time
import requests
from selenium import webdriver  # 操作浏览器
from selenium.webdriver.edge.options import Options  # 设置浏览器
from selenium.webdriver.edge.service import Service  # 管理驱动
from webdriver_manager.microsoft import EdgeChromiumDriverManager  # 自动下载匹配的edge驱动
from selenium.webdriver.common.by import By  # 用于元素定位
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime  # 用于计算周几
from selenium.common.exceptions import NoSuchElementException  # 获取不到元素时exce：NoSuchElementException
from tqdm import tqdm  # 增加进度条
from lxml import etree  #解析网页
from threading import Thread    #多线程
ver = 1.2
one_inform = '    此版本重构启动逻辑，优化启动速度。\n    新增登录失败提示并重试功能'
# 自动下载匹配的驱动
def QuDong():
    # 自动下载驱动，创建驱动实例
    # print('正在下载驱动（约5秒）...')
    driver = EdgeChromiumDriverManager().install()
    # 创建服务对象
    all_service = Service(driver)

    return all_service
# 设置、启动浏览器
def llq(all_service):
    # 创建设置对象
    options = Options()
    # 禁用沙盒模式
    options.add_argument("--no-sandbox")
    # 无窗口
    options.add_argument("--headless=new")
    # 保持浏览器打开状态
    # options.add_experimental_option("detach", True)
    # 禁用驱动日志
    options.add_argument('--log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # 创建启动和浏览器
    a1 = webdriver.Edge(service=all_service, options=options)
    a1.implicitly_wait(5)  # 全局隐式等待5秒

    return a1
#登录函数
def login():
    errorlogin = ''
    while True:
        # 登录
        print(errorlogin)
        errorlogin = '\n！！！您提供的用户名或者密码有误！！！\n！！！！！！！请重新输入！！！！！！！\n'
        user = input('请输入：\n  学号：')
        passwd = input('  密码：')
        clear()
        print('\n正在登录教务系统...')
        q1.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[2]/div/div[3]/div/form/p[1]/input').send_keys(f'{user}')
        q1.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[2]/div/div[3]/div/form/p[2]/input[1]').send_keys(f'{passwd}')
        login = q1.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[2]/div/div[3]/div/form/p[5]/button').click()
        trylogin = q1.find_element(By.XPATH,'//*[@id="msg"]').text
        if trylogin == '您提供的用户名或者密码有误':
            errorlogin = '\n！！！您提供的用户名或者密码有误！！！\n！！！！！！！请重新输入！！！！！！！\n'
            clear()
            continue
        time.sleep(2)
        WebDriverWait(q1, 15).until(  # 最长等待15秒
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div/div[2]/div[2]/div/div[1]/div/i/img'))
        )
        print('登录成功！')
        break
#次线程，下驱动，登录
def runover():
    global all_service,q1
    # 创建浏览器实例
    all_service = QuDong()
    q1 = llq(all_service)
    q1.get('https://jwxt.haou.edu.cn/app-ws/ws/app-service/jasig/cas/index')
    # 登录
    login()
#清空控制台
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
#远程更新，公告
def get_version():
    # 获取版本，更新，作者，通知
    def getpy():
        url = 'https://sharechain.qq.com/5430c542fdce29bc7054751aa2d7ab98'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36 Edg/138.0.0.0',
        }
        response = requests.get(url, headers=headers)
        html = etree.HTML(response.text)
        res = html.xpath('/html/body/div/div/section/article/div/text()')
        version = float(res[0].split('///')[0])
        updata = str(res[0].split('///')[1])
        author = str(res[0].split('///')[2])
        notice = str(res[0].split('///')[3])
        notices = notice.split('。。')

        return version, updata, author, notice, notices

    # 输出远程获取的
    def main0(ver):
        version, updata, author, notice, notices = getpy()

        # 检测更新
        if ver < version:
            print(f'请更新后使用！\n更新链接：{updata}')
            time.sleep(3600)
            sys.exit(f'\n请更新后使用！\n更新链接：{updata}')
        print(f'当前版本{ver},已是最新版！')

        # 公告
        print('\n公告：')
        # 专属固定公告
        print(one_inform)
        # 远程公告
        for i, tz in enumerate(notices, start=1):
            print(f'    {i}.{tz}')
        time.sleep(2)
        # 作者
        print(f'作者：{author} 信工学院的一名准大二小白\n')

    getpy()
    main0(ver)
#查课表
def KeBiao():
    # 计算当前周几，返回整数数字
    def get_weekday():
        # 获取当前日期的星期几（0=周一，6=周日）
        weekday = datetime.now().weekday()
        # 转换为中文习惯（1=周一，7=周日）
        weekday_chinese = (weekday + 1) % 7
        if weekday_chinese == 0:
            weekday_chinese = 7

        return weekday_chinese
    # 计算第几节课，函数调用前循环外i应初始化为整数-1,for最后加i = i + 2
    def course_node(i):
        if i == 1:
            ii = '上午第一节：'
        elif i == 3:
            ii = '上午第二节：'
        elif i == 5:
            ii = '下午第一节：'
        elif i == 7:
            ii = '下午第二节：'
        elif i == 9:
            ii = '晚上第一节：'
        else:
            ii = '未知课节数(请反馈给作者)：'

        return str(ii)

    # 获取当天课表和课程时间
    def GetCourse():
        print('获取课表中，请等待5秒...')
        list_course = []
        list_course_time = []
        # 获取当前周几，传入xpath时要+1
        day = get_weekday()  # 当前周几
        weekday = str(day + 1)
        try:
            # 一次性获取当天所有课程元素
            course_elements = q1.find_elements(By.XPATH,
                                               f'/html/body/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div[position() mod 2 = 1]/div[{weekday}]/div')
            i = 1
            for element in tqdm(course_elements, desc="获取课表进度", colour="green", unit="节"):
                ii = course_node(i)
                try:
                    # 获取课名
                    course = element.find_element(By.XPATH, './div/div/div/p').text
                    course = ii + course
                    list_course.append(course)

                    # 获取课时长
                    style = element.get_attribute('style')
                    if style == 'height: 2.34rem;':
                        course_time = '90分钟(2小节)'
                    elif style == 'height: 4.74rem;':
                        course_time = '180分钟(4小节)'
                    else:
                        course_time = '未知时长'
                    list_course_time.append(course_time)
                except NoSuchElementException:
                    continue  # 未找到元素时跳过当前循环，不添加任何内容
                i = i + 2
        except NoSuchElementException:
            pass
        print('获取课表成功！')
        return list_course, list_course_time, day
    #输出结果
    def get_course_print():
        # 进入“课表”
        q1.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/div[2]/div[2]/div/div[1]/div/span').click()
        print('进入课表模块成功！')
        # 获取返回的课名，课时间，今天周几
        list_course, list_course_time, day = GetCourse()
        # 输出当天课程和时长
        all_list = list(zip(list_course, list_course_time))  # 两列表合为一个
        if day == 7:
            day = '日'
            print(f'\n今天周{day}课表：')
        else:
            print(f'\n今天周{day}课表：')
        if not all_list:
            print("  今天没有课程，好好休息哦！")
        else:
            for course, time in all_list:
                print(f'  {course}, 时长: {time}')

    get_course_print()


#启动时后台下驱动
t = Thread(target=runover)
t.start()
#远程更新，公告
get_version()
t.join()    #等待次线程加载完毕

##########主程序功能########
KeBiao()


















# 关闭浏览器
q1.quit()
out = input()