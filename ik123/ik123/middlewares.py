# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

import pyperclip
import pyautogui
import time
import traceback
import re
import os
import random
from ik123.settings import USER_AGENTS,image_path

# from gushi.settings import PROXIES
# import base64
class GuShiSpiderMiddleware(object):
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

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class Ik123DownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    # http: // p.ik123.com / bizhi / fengjing / list_224.html http://p.ik123.com/bizhi/2466.html

    def process_reqeust(self,request,spider):
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        if 'list' not in request.url:
            print("*************************" + request.url)
            try:
                K = 0
                while(True):
                    try:
                        spider.browser.get(request.url)
                        #self.browser.implicitly_wait(10)
                        element = WebDriverWait(spider.browser, 30).until(EC.presence_of_element_located((By.ID, "gui_left")))
                        # print("##################")
                        # print(element)
                        break
                    except TimeoutException:
                            print("图片内容元素定位失败\n{}".format(request.url))
                            spider.browser.refresh()
                            K = K + 1
                            if( K >2 ):
                                return HtmlResponse(url=request.url, status=500, request=request)
                pic = spider.browser.find_elements(By.XPATH, r"//div[@id='gui_left']//img")
                pic_urls = [i.get_attribute('src') for i in pic]
                pic_names = [i.split('/')[-1:][0] for i in pic_urls]
                pic_rejoin_path = [os.path.join(image_path, i) for i in pic_names]
                print(pic_rejoin_path)
                for i in range(len(pic)):
                    actions = ActionChains(spider.browser)
                    # 找到图片后右键单击图片
                    actions.move_to_element(pic[i])  # 定位到元素
                    actions.context_click(pic[i])  # 点击右键
                    actions.perform()  # 执行
                    time.sleep(1)  # 等待一秒
                    pyautogui.press('v')  # v 是保存的快捷键
                    #pyautogui.typewrite(['V'])  # v 是保存的快捷键
                    time.sleep(1)  # 等待一秒
                    pyperclip.copy(pic_rejoin_path[i])  # 把 指定的路径拷贝到过来
                    time.sleep(1)  # 等待一秒
                    pyautogui.hotkey('ctrlleft', 'v')  # 粘贴
                    time.sleep(0.5)  # 等待一秒
                    pyautogui.press('enter')
                    time.sleep(0.5)  # 等待一秒
                    print("图片下载完成:%s"%pic_urls[i])
                              
                return HtmlResponse(url=request.url, body=spider.browser.page_source, request=request, encoding='utf-8')
            except TimeoutException:
                return HtmlResponse(url=request.url,  status=500, request=request)
        else:
            print("主页**************主页**************")
            spider.browser.get(request.url)
            try:
                WebDriverWait(spider.browser, 60).until(EC.presence_of_element_located((By.ID, "gui_left")))
            except:
                print("翻页内容元素定位失败\n{}".format(request.url))
            return HtmlResponse(url=request.url, body=spider.browser.page_source, request=request, encoding='utf-8')  #
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


# 随机的User-Agent
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
