
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json


class GetCookies(object):
    def __init__(self):
        self.driver = None
        self.browser_path = r"D:\Document\scrapy\chromedriver_win32\chromedriver_win32\chromedriver.exe"
        self.login_url = "https://passport.csdn.net/login?"
        self.start_url = "https://blog.csdn.net/qq_34414530?spm=1011.2415.3001.5343"


    def init_chrome(self):
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        s = Service(executable_path=self.browser_path)
        self.driver = webdriver.Chrome(service=s)
        self.driver.maximize_window()
        self.driver.delete_all_cookies()

    def first_login(self, wait_time):
        '''
        第一次登录，需要人工登录
        :param wait_time:
        :return:
        '''
        # 记得写完整的url 包括http和https
        self.driver.get(self.login_url)
        # 程序打开网页后20秒内 “手动登陆账户”
        time.sleep(wait_time)
        self.driver.get(self.start_url)

    def save_cookies(self):
        '''
        保存浏览器的cookies
        :return:
        '''
        with open("cookies.txt", 'w') as f:
            # 将cookies保存为json格式
            f.write(json.dumps(self.driver.get_cookies()))

    def inject_cookies(self):
        '''
        向浏览器中写入cookies
        :return:
        '''
        with open("cookies.txt", 'r') as f:
            # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
            cookies_list = json.load(f)
            for cookie in cookies_list:
                # 该字段有问题所以删除就可以
                if 'expiry' in cookie:
                    del cookie['expiry']
                self.driver.add_cookie(cookie)

    def main(self):
        self.driver.get(self.start_url)
        self.inject_cookies()
        self.driver.refresh()

if __name__ == '__main__':
    C = GetCookies()
    C.init_chrome()
    C.first_login(200)
    C.save_cookies()
    #C.main()

