# -*- coding: utf-8 -*-
import json
import os.path

import scrapy
from c_poem.items import CPoemItem
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from c_poem.settings import browser_path

class CpoemSpider(scrapy.Spider):
    name = 'cpoem'
    allowed_domains = ['gushiwen.cn']
    # start_urls = ['https://so.gushiwen.cn/gushi/tangshi.aspx', ]# 唐诗三百首
    start_urls = ['https://so.gushiwen.cn/shiwen/default_1Acde790aa3213A1.aspx', ]  # 宋词精选
    def __init__(self):
        super().__init__()
        self.cookies_dict = {}
        self.login_url = "https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx"
        self.start_url = "https://so.gushiwen.cn/shiwen/default_1Acde790aa3213A1.aspx"

        chrome_options = Options()
        # self.chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_experimental_option('useAutomationExtension', False)

        caps = DesiredCapabilities.CHROME
        # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        caps["pageLoadStrategy"] = "none"
        s = Service(executable_path=browser_path)
        print("*******************初始化谷歌浏览器***********************")
        self.browser = webdriver.Chrome(service=s, options=chrome_options, desired_capabilities=caps)
        #self.browser.maximize_window()

    def first_login(self, wait_time):
        '''
        第一次登录，需要人工登录
        :param wait_time:
        :return:
        '''
        # 记得写完整的url 包括http和https
        self.browser.get(self.login_url)
        # 程序打开网页后20秒内 “手动登陆账户”
        time.sleep(wait_time)
        self.browser.get(CpoemSpider.start_urls[0])

        with open("cookies.txt", 'w') as f:
            # 将cookies保存为json格式
            f.write(json.dumps(self.browser.get_cookies()))

    def inject_cookies(self, file):
        '''
        向浏览器中写入cookies
        :return:
        '''
        if not os.path.exists(file):
            self.first_login(20)

        with open(file, 'r') as f:
            # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
            cookies_list = json.load(f)

        for cookie in cookies_list:
            self.cookies_dict[cookie['name']] = cookie["value"]

    def start_requests(self):
        self.browser.get(self.start_url)
        self.inject_cookies("cookies.txt") #获取cookies
        print("*******************cookies***********************")
        print(self.cookies_dict)
        self.browser.refresh()

        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                cookies=self.cookies_dict,
                callback=self.parse,
                dont_filter= True
            )

    def parse(self, response):
        print("****************\n{}".format(response.url))
        print("****************\n{}".format(response.status))

        urls = response.xpath('.//div[@class="left"]//div[@class ="sons"]//p[not(@class)]//a//@href').getall()
        print("****************\n{}".format(urls))
        if urls:
            for url in urls:
                next_url = response.urljoin(url)
                request = scrapy.Request(next_url, meta={'gus':True}, callback=self.parse_item)
                yield request
        else:
            print("****************\n页面元素定位失败！")

        next_page = response.xpath("//a[text()='下一页']/@href").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_item(self, response):
        item = CPoemItem()
        item['poem_type'] = "宋词"
        item['poem_url'] = response.url
        # self.browser.get(response.url)
        # self.browser.implicitly_wait(5)
        son = self.browser.find_element(By.XPATH, ".//div[@class='left']//div[@class='sons']")
        if son:
            title = son.find_element(By.XPATH,".//div[@class = 'cont']//h1").text
            item['poem_title'] = title

            source = son.find_elements(By.XPATH,".//div[@class = 'cont']//p[@class = 'source']/a")
            author = [i.text.strip() for i in source]
            item['poem_author'] = '.'.join(author)

            contson = son.find_elements(By.XPATH,".//div[@class = 'cont']//div[@class = 'contson']")
            body = [i.text.strip() for i in contson]
            item['poem_body'] = ''.join(body)

            yi_button = son.find_element(By.XPATH,".//div[@class = 'cont']//div[@class = 'yizhu']//img[contains(@alt,'译')]")
            ActionChains(self.browser).move_to_element(yi_button).click().perform()
            time.sleep(1)
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, ".//div[@class = 'cont']//div[@class = 'contson']//p//span")))

            yi = son.find_elements(By.XPATH,".//div[@class = 'cont']//div[@class = 'contson']//p//span")
            print("******译文*********\n{}".format(yi))
            yi = [i.text.strip() for i in yi]
            item['poem_yi'] = ''.join(yi)
            ActionChains(self.browser).move_to_element(yi_button).click().perform()
            time.sleep(1)

            zhu_button = son.find_element(By.XPATH, ".//div[@class = 'cont']//div[@class = 'yizhu']//img[contains(@alt,'注')]")
            ActionChains(self.browser).move_to_element(zhu_button).click().perform()
            #zhu_button.click()
            time.sleep(1)

            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, ".//div[@class = 'cont']//div[@class = 'contson']//p//span")))
            zhu = son.find_elements(By.XPATH,".//div[@class = 'cont']//div[@class = 'contson']//p//span")
            print("******注解*********\n{}".format(zhu))
            zhu = [i.text.strip() for i in zhu]
            item['poem_zhu'] = ''.join(zhu)
            ActionChains(self.browser).move_to_element(zhu_button).click().perform()
            time.sleep(1)

            shang_button = son.find_element(By.XPATH,"//div[@class = 'cont']//div[@class = 'yizhu']//img[contains(@alt,'赏')]")
            ActionChains(self.browser).move_to_element(shang_button).click().perform()
            time.sleep(1)

            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, ".//div[@class = 'cont']//div[@class = 'contson']//div[@class = 'hr']/following-sibling::p[not(@style)]")))
            shang = son.find_elements(By.XPATH,".//div[@class = 'cont']//div[@class = 'contson']//div[@class = 'hr']/following-sibling::p[not(@style)]")
            print("******赏析*********\n{}".format(shang))
            shang = [i.text.strip() for i in shang]
            item['poem_shang'] = ''.join(shang)
            ActionChains(self.browser).move_to_element(shang_button).click().perform()
            time.sleep(1)
            yield item


