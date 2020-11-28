# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time
import random
from c_poem.settings import USER_AGENTS

class CPoemSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or c_item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or c_item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not c_items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class CPoemDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self, ):
        pass

        # self.chrome_options = Options()
        # # self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument('--no-sandbox')
        # self.chrome_options.add_argument('--disable-dev-shm-usage')
        # self.chrome_options.add_argument('--disable-gpu')
        # self.chrome_options.add_experimental_option('useAutomationExtension', False)
        # # desired_capabilities = DesiredCapabilities.CHROME
        # # # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        # # desired_capabilities["pageLoadStrategy"] = "none"
        # self.browser = webdriver.Chrome(
        #     executable_path=r"C:\MKSProjects\Vision Test Environment\CANoe\Geely_GEEA2\Tools\myPython\chromedriver.exe",
        #     options=self.chrome_options)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s
    def process_reqeust(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        self.browser = spider.browser
        if request.meta.get('gus'):
            while (True):
                try:
                    self.browser.get(request.url)
                    #element = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "sons")))
                    self.browser.implicitly_wait(3)
                    print("##################")
                    return HtmlResponse(url=request.url, body=self.browser.page_source, request=request,encoding='utf-8')
                    break
                except TimeoutException:
                    self.browser.refresh()
                    K = K + 1
                    if (K > 2):
                        return HtmlResponse(url=request.url, status=500, request=request)
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.
        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def closed(self, spider):
        self.browser.quit()



class RandomUserAgent(object):
    def process_request(self, request, spider):
        useragent = random.choice(USER_AGENTS)
        request.headers.setdefault("User-Agent", useragent)

class RandomProxy(object):
    def process_request(self, request, spider):
        pass
        #proxy = random.choice(PROXIES)

        # if proxy['user_passwd'] is None:
        #     # 没有代理账户验证的代理使用方式
        #     request.meta['proxy'] = "http://" + proxy['ip_port']
        #
        # else:
        #     # 对账户密码进行base64编码转换
        #     base64_userpasswd = str(base64.b64encode(proxy['user_passwd']))
        #     # 对应到代理服务器的信令格式里
        #     request.headers['Proxy-Authorization'] = 'Basic ' + base64_userpasswd
        #
        #     request.meta['proxy'] = "http://" + proxy['ip_port']
