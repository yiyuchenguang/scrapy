# -*- coding: utf-8 -*-

import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # 使用无头浏览器
from selenium.webdriver.chrome.service import Service
from ik123.settings import browser_path
from ik123.items import Ik123Item

import os

class CoserSpider(scrapy.Spider):
    name = "coser"
    allowed_domains = ["ik123.com"]
    start_urls = (
        #'http://p.ik123.com/bizhi/fengjing/list_6.html',
         'http://p.ik123.com/bizhi/dongwu/list_1.html',
        # 'http://p.ik123.com/bizhi/youxi/list_1.html',
        # 'http://www.ik123.com/q/tuku/weimei/'
    )

    # 实例化一个浏览器对象
    def __init__(self):
        chrome_options = Options()
        # self.chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_experimental_option('useAutomationExtension', False)
        # caps = DesiredCapabilities.CHROME
        # # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        # caps["pageLoadStrategy"] = "none"
        s = Service(executable_path=browser_path)
        print("*******************初始化谷歌浏览器***********************")
        print(browser_path)
        self.browser = webdriver.Chrome(service=s, options=chrome_options)  # , desired_capabilities=caps
        self.browser.maximize_window()
        super().__init__()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )

    def parse(self, response, **kwargs):
        pic_urls = response.xpath("//div[@id='gui_left']//li[@class='img']/a/@href").getall()
        print("***********pic_urls**********\n", pic_urls)
        for link in pic_urls:
            request = scrapy.Request(link, callback=self.parse_item)
            yield request

        # follow pagination links
        next_page = response.xpath("//a[text()='下一页']/@href").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    @staticmethod
    def parse_item(response):
        item = Ik123Item()
        item['info'] = response.xpath(
            "//div[@class='daohang']/following-sibling::h1[1]/text()").get()  # '浩瀚唯美星空壁纸_绝美好看星空
        item['name'] = response.xpath("//div[@id='gui_left']/p/img/@alt").getall()
        item['image_urls'] = response.xpath("//div[@id='gui_left']//img/@src").getall()

        yield item

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
        # pic_root = os.path.abspath(os.path.dirname(os.getcwd()))
        # self.image_file = os.path.join(pic_root, 'D:\Document\素材\古诗文')
        # if not os.path.exists(self.image_file):
        #     os.makedirs(self.image_file)


    def closed(self, spider):
        spider.logger.info('browser colsed!')
        self.browser.quit()

