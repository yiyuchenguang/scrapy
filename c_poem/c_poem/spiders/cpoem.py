# -*- coding: utf-8 -*-
import scrapy
from c_poem.items import CPoemItem
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
class CpoemSpider(scrapy.Spider):
    name = 'cpoem'
    allowed_domains = ['gushiwen.cn']
    # start_urls = ['https://so.gushiwen.cn/gushi/tangshi.aspx', ]# 唐诗三百首
    start_urls = ['https://so.gushiwen.cn/shiwen/default_1Acde790aa3213A1.aspx', ]  # 宋词三百首
    #https://www.jianshu.com/p/53af85a0ce18
    def __init__(self):
        chrome_options = Options()
        # self.chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_experimental_option('useAutomationExtension', False)
        browser_path = "../chromedriver_win32/chromedriver.exe"
        caps = DesiredCapabilities.CHROME
        # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        caps["pageLoadStrategy"] = "none"

        self.browser = webdriver.Chrome(executable_path=browser_path,options=chrome_options , desired_capabilities=caps)
        self.browser.set_window_size(900, 600)  # 设置浏览器的窗体大小

    def parse(self, response):
        urls = response.xpath('.//div[@class="left"]//div[@class ="sons"]//p[not(@class)]//a//@href').getall()
        for url in urls:
            next_url = response.urljoin(url)
            request = scrapy.Request(next_url, meta={'gus':True}, callback=self.parse_item)
            yield request
        next_page = response.xpath("//a[text()='下一页']/@href").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_item(self, response):
        item = CPoemItem()
        item['poem_type'] = "宋词"
        item['poem_url'] = response.url
        # self.browser.get(response.url)
        # self.browser.implicitly_wait(5)
        son = self.browser.find_element_by_xpath(".//div[@class='left']//div[@class='sons']")
        if son:
            title = son.find_element_by_xpath(".//div[@class = 'cont']//h1").text
            item['poem_title'] = title

            source = son.find_elements_by_xpath(".//div[@class = 'cont']//p[@class = 'source']/a")
            author = [i.text.strip() for i in source]
            item['poem_author'] = '.'.join(author)

            contson = son.find_elements_by_xpath(".//div[@class = 'cont']//div[@class = 'contson']")
            body = [i.text.strip() for i in contson]
            item['poem_body'] = ''.join(body)

            yi_button = son.find_element_by_xpath(
                "//div[@class = 'cont']//div[@class = 'yizhu']//img[contains(@alt,'译')]")
            yi_button.click()
            time.sleep(0.2)

            yi = son.find_elements_by_xpath(".//div[@class = 'cont']//div[@class = 'contson']//p//span")
            yi = [i.text.strip() for i in yi]
            item['poem_yi'] = ''.join(yi)
            yi_button.click()
            time.sleep(0.2)

            zhu_button = son.find_element_by_xpath(
                "//div[@class = 'cont']//div[@class = 'yizhu']//img[contains(@alt,'注')]")
            zhu_button.click()
            time.sleep(0.2)

            zhu = son.find_elements_by_xpath(".//div[@class = 'cont']//div[@class = 'contson']//p//span")
            zhu = [i.text.strip() for i in zhu]
            item['poem_zhu'] = ''.join(zhu)
            zhu_button.click()
            time.sleep(0.2)

            shang_button = son.find_element_by_xpath(
                "//div[@class = 'cont']//div[@class = 'yizhu']//img[contains(@alt,'赏')]")
            shang_button.click()
            time.sleep(0.5)

            shang = son.find_elements_by_xpath(
                ".//div[@class = 'cont']//div[@class = 'contson']//div[@class = 'hr']/following-sibling::p[not(@style)]")
            shang = [i.text.strip() for i in shang]
            item['poem_shang'] = ''.join(shang)
            shang_button.click()
            time.sleep(0.5)
            yield item
